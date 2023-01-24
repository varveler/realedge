from celery.decorators import task
from django.utils import timezone

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from yahooquery import Ticker

import datetime
import time
import requests
from urllib.parse import unquote
import re
import pandas as pd
import numpy as np
from decimal import Decimal
import logging
import traceback


from gappers.models import UpGapper
from news.tasks import stockNewsApi_get_resent_news, scrape_finviz_news
from common.utils import ( wait_random_seconds,
                          ghost_driver, next_available_row_to_update,
                          str_date, get_sheet, update_cell_and_wait, atr,
                          convert_amount_benzinga, convert_percentage_to_decimal,
                          fix_percentage_barchart_api)



# frontier values
MIN_PREMARKET_VOLUME = 50000  # int
MAX_PRICE = 101.0  # float
MAX_GAP_PERCENTAGE = 9.0  # float
MIN_GAP_PERCENTAGE = -9.0  # float
GAP_UP_MIN_GAP = 0.05  # 5%
GAP_DOWN_MIN_GAP = -0.05

# home_folder_name = get_env_variable('HOME_FOLDER_NAME')
# FIREFOX_PROFILE = '/home/%s/.mozilla/firefox/r8abwwfd.default' % home_folder_name

logger = logging.getLogger(__name__)

AVOID_STOCKS = ['Direxion Daily',
                'Direxiondaily',
                'Velocityshares',
                'VelocityShares',
                'Velocity Shares',
                '3x',
                '-3x',
                '2x',
                '-2x',
                'Direxion',
                'Velocity',
                'Inverse',
                'Index',
                'Leveraged',
                'ProShares',
                'Pro Shares',
                'Shares',
                'SPDR',
                'ETF',
                'iShares',
                'Futures',
                'VIX',
                'ETN',
                'IPath',
                'S&P',
                'S&P500',
                'Dow 30',
                'Dow30',
                'QQQ',
                'Fund',
                'fund']


# def parse_gappers():
#     """Search for stocks in market cameleon and return stocks given the criteria."""
#     url = 'https://marketchameleon.com/Reports/PremarketTrading'
#     #display = Display(visible=0, size=(1200, 800))
#     #display.start()
#     driver = ghost_driver()
#     driver.get(url)
#     time.sleep(10)
#     try:
#         wait = WebDriverWait(driver, timeout=15, poll_frequency=0.1)
#         wait.until(EC.presence_of_element_located((By.ID, "gainers_tbl")))
#     except Exception as e:
#         driver.save_screenshot('WebsiteScreenShot.png')
#         print('Waited and "gainers_tbl" id was not found on market chameleon')
#         print(e)
#         time.sleep(100)
#         return None
#     html_source = driver.page_source
#     soup = BeautifulSoup(html_source, "html.parser")
#     parent_div_ids = ['gainers_tbl', 'decliners_tbl']
#     stocks = []
#     for id in parent_div_ids:
#         table = soup.find(id=id).tbody
#         rows = table.find_all('tr')
#         for row in rows:
#             cells = row.find_all('td')
#             stock = Stock()
#             stock.ticker = cells[0].text
#             stock.price = cells[1].text
#             stock.percentage = cells[3].text.split('%')[0]
#             stock.volume = convert_amount(cells[4].text)
#             stock.market_cap = cells[5].text
#             if float(stock.percentage) >= MAX_GAP_PERCENTAGE or float(stock.percentage) <= MIN_GAP_PERCENTAGE:
#                 if float(stock.price) < MAX_PRICE:
#                     if stock.volume > MIN_PREMARKET_VOLUME:
#                         stocks.append(stock)
#     wait_random_seconds()
#     driver.close()
#     driver.quit()
#     print(stocks)
#     return stocks


@task(name='parse_gappers_barchart_and_filter')
def parse_gappers_barchart_and_filter():
    """Get all gappers in the morning and return list of Stock objects."""
    geturl = r'https://www.barchart.com/stocks/performance/gap/gap-up'
    apiurl = r'https://www.barchart.com/proxies/core-api/v1/quotes/get?lists=stocks.gaps.up.us&orderDir=desc&fields=symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2CgapUp%2CgapUpPercent%2ChighPrice%2ClowPrice%2Cvolume%2CtradeTime%2CsymbolCode%2CsymbolType%2ChasOptions%2Cexchange%2CmarketCap%2CmarketCap%2CsharesOutstanding%2Cfloat%2CpercentInsider%2CpercentInstitutional%2Cindustry&orderBy=gapUpPercent&meta=field.shortName%2Cfield.type%2Cfield.description&page=1&limit=100&raw=1'
    getheaders = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    getpay = {'page': 'all'}
    session = requests.Session()
    response_s = session.get(geturl, params=getpay, headers=getheaders)
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.barchart.com/futures/quotes/CLJ19/all-futures?page=all',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'x-xsrf-token': unquote(unquote(session.cookies.get_dict()['XSRF-TOKEN']))
    }
    response = session.get(apiurl, headers=headers)
    json_gappers = response.json()
    data = json_gappers['data']
    stoncks = []
    stoncks_ids = []
    for stock in data:
        if (stock['raw']['gapUpPercent'] >= GAP_UP_MIN_GAP and
        stock['raw']['volume'] >= MIN_PREMARKET_VOLUME):
            stonck, created = UpGapper.objects.update_or_create(
                date = datetime.date.today(), ticker = stock['raw'].get('symbol', ''),
                defaults = {'date'                             : datetime.date.today(),
                            'ticker'                           : stock['raw'].get('symbol', ''),
                            'market'                           : stock['raw'].get('exchange', ''),
                            'company_name'                     : stock['raw'].get('symbolName', ''),
                            'industry'                         : stock['raw'].get('industry', ''),
                            'pm_source2'                       : 'barchart',
                            'pm_s2_volume'                     : stock['raw'].get('volume', 0),
                            'pm_s2_market_cap'                 : stock['raw'].get('marketCap', 0),
                            'pm_s2_shares_outstanding'         : stock['raw'].get('sharesOutstanding', 0),
                            'pm_s2_float'                      : stock['raw'].get('float', 0.0),
                            'pm_s2_held_percent_insiders'      : fix_percentage_barchart_api(stock['raw'].get('percentInsider', 0.0)),
                            'pm_s2_held_percent_institutions'  : fix_percentage_barchart_api(stock['raw'].get('percentInstitutional', 0.0)),
                            'gap_percentage'                   : stock['raw'].get('gapUpPercent', 0.0),
                            'last'                             : stock['raw'].get('lastPrice', 0.0),
                            'gap'                              : stock['raw'].get('gapUp', 0.0) })
            if created:
                stoncks.append(stonck)
            #stoncks_ids.append(stonck.id)
    return stoncks


def write_to_log_sheet(stocks, worksheet=None):
    sheet = get_sheet(worksheet=worksheet)
    day_cell = sheet.find('_Day_')
    stock_cell = sheet.find('_Stock_')
    company_name_cell = sheet.find('_Company Name_')
    price_cell = sheet.find('_Price_')
    gap_cell = sheet.find('_Gap %_')
    volume_cell = sheet.find('_Volume_')
    market_cap_cell = sheet.find('_Market Cap_')
    shares_outs_cell = sheet.find('_Shares Outstanding_')
    float_cell = sheet.find('_Float_')
    held_insiders_cell = sheet.find('_Held Insiders_')
    held_inst_cell = sheet.find('_Held Insititutions_')
    short_perc_float_cell = sheet.find('_Short Float_')
    atr_cell = sheet.find('_ATR_')
    today = str_date(datetime.date.today())
    red_gap_prob_cell = sheet.find('Red Gap Probability')
    gaps_observations_cell = sheet.find('Gaps Observations')
    for stock in stocks:
        blank_row = next_available_row_to_update(sheet)
        print('######################################################')
        print('######################################################')
        update_cell_and_wait(sheet, blank_row, day_cell.col, today,)
        update_cell_and_wait(sheet, blank_row, stock_cell.col, stock.ticker, 'Ticker')
        update_cell_and_wait(sheet, blank_row, company_name_cell.col, stock.name, 'Company')
        update_cell_and_wait(sheet, blank_row, price_cell.col, stock.price, 'Price')
        update_cell_and_wait(sheet, blank_row, gap_cell.col, stock.percentage, 'Gap %')
        update_cell_and_wait(sheet, blank_row, volume_cell.col, stock.volume, 'Volume')
        update_cell_and_wait(sheet, blank_row, market_cap_cell.col, stock.market_cap, 'Market Cap')
        update_cell_and_wait(sheet, blank_row, shares_outs_cell.col, stock.shares_outstanding, 'Shares Outstanding')
        update_cell_and_wait(sheet, blank_row, float_cell.col, stock._float, 'Float')
        update_cell_and_wait(sheet, blank_row, held_insiders_cell.col, stock.held_insiders, 'Held by insiders')
        update_cell_and_wait(sheet, blank_row, held_inst_cell.col, stock.held_institutions, 'Held by institutions')
        update_cell_and_wait(sheet, blank_row, short_perc_float_cell.col, stock.short_float, 'Short % of Float')
        update_cell_and_wait(sheet, blank_row, atr_cell.col, stock.atr, 'ATR')
        update_cell_and_wait(sheet, blank_row, red_gap_prob_cell.col, stock.red_gap_probability, 'Red Gap Probability')
        update_cell_and_wait(sheet, blank_row, gaps_observations_cell.col, stock.gaps_observations, 'Gaps Observations')


def parse_stock_statistics_yquery(stocks):
    # tickers = [stock.ticker for stock in stocks]
    # data = Ticker(tickers, asynchronus=True, max_workers=7)
    # summary_details = data.summary_detail
    # key_stats = data.key_stats
    for stock in stocks:
        print('yahooquery ', stock.ticker, stock.company_name)
        wait_random_seconds(min=1, max=3)
        data = Ticker(stock.ticker).get_modules(['quoteType', 'defaultKeyStatistics', 'summaryDetail'])
        # print(data)
        try:
            if not stock.company_name:
                stock.company_name = data[stock.ticker]['quoteType'].get('longName', None)
            stock.pm_source1 = 'YahooQuery'
            stock.pm_s1_beta = data[stock.ticker]['defaultKeyStatistics'].get('beta', None)
            stock.pm_s1_market_cap = data[stock.ticker]['summaryDetail'].get('marketCap', None)
            stock.pm_s1_shares_outstanding = data[stock.ticker]['defaultKeyStatistics'].get('sharesOutstanding', None)
            stock.pm_s1_float = data[stock.ticker]['defaultKeyStatistics'].get('floatShares', None)
            stock.pm_s1_held_percent_insiders = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInsiders', None)
            stock.pm_s1_held_percent_institutions = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInstitutions', None)
            stock.pm_s1_short_float = data[stock.ticker]['defaultKeyStatistics'].get('sharesPercentSharesOut', None)
            stock.pm_s1_shares_short = data[stock.ticker]['defaultKeyStatistics'].get('sharesShort', None)
            stock.pm_s1_short_percent_float = data[stock.ticker]['defaultKeyStatistics'].get('shortPercentOfFloat', None)
        except Exception as e:
            print('######Exception#######')
            print(stock.ticker, stock.company_name)
            print(e)
        wait_random_seconds(min=1, max=3)
        df = Ticker(stock.ticker).history(period='5y')
        if isinstance(df, dict) or len(df.index) < 20:
            continue
        df = df.reset_index()
        df.drop('symbol', axis=1, inplace=True)
        start_date = datetime.date.today()
        end_date = start_date - datetime.timedelta(days=1095)
        df['date'] = pd.to_datetime(df['date']).dt.date
        #df['gap'] = df['open'] - df['close'].shift(1)
        df['gapPercent'] = ((df['open'] - df['close'].shift(1)) / df['close'].shift(1)) * 100
        df['ATR'] = atr(df)
        df['RVOL'] = df['volume'] / df['volume'].rolling(window=5).mean()
        #df['TR'] = df['low'] - df['high']
        df['move'] = df['close'] - df['open']
        today = datetime.date.today()
        mask_today = df['date'] == today
        df_today_data = df.loc[mask_today]
        if not df_today_data.empty: # today data is in the df
            index = df_today_data.index[0] - 1
        else:
            index = df.index.stop - 1
        stock.pm_atr = round(df.loc[index]['ATR'], 2)
        mask = (df['date'] < start_date) & (df['date'] >= end_date)
        df = df.loc[mask]
        gaps_df = df[(df['gapPercent'] >= 10) & (df['RVOL'] >= 1.6)].copy()
        if gaps_df.empty:
            stock.pm_red_gaps = None
            stock.pm_observations = None
        else:
            observations = len(gaps_df.index)
            stock.pm_red_gaps = str(int((np.sum(gaps_df['move'] < 0) / observations) * 100))
            stock.pm_observations = str(observations)
        stock.save()
    return stocks





@task(name='get_benzinga_premerket_tickers')
def get_benzinga_premerket_tickers(driver):
    driver.get('https://www.benzinga.com/premarket/')
    time.sleep(4)
    try:
        wait = WebDriverWait(driver, timeout=3 )
        wait.until(EC.presence_of_element_located((By.ID, "movers-stocks-table-gainers")))
    except Exception as e:
        date = timezone.now()
        driver.save_screenshot('WebsiteScreenShot%s.png' % date)
        print('Waited and "gainers_tbl" id was not found on benzinga')
        print(e)
        return None
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    div = soup.find(id= 'movers-stocks-table-gainers')
    table = div.find('table', class_='premarket-stock-table')
    rows = table.find_all('tr')
    stoncks = []
    for row in rows[1:]:
        cells = row.find_all('td')
        print(cells[0].text.strip())
        pm_volume = convert_amount_benzinga(cells[4].text.strip())
        gap_percentage = convert_percentage_to_decimal(cells[3].text.strip())
        if (pm_volume >= MIN_PREMARKET_VOLUME and gap_percentage >= GAP_UP_MIN_GAP):
            stonck, created = UpGapper.objects.update_or_create(
                date = datetime.date.today(), ticker = cells[0].text.strip(),
                defaults = { 'date'          : datetime.date.today(),
                             'ticker'        : cells[0].text.strip(),
                             'company_name'  : cells[1].text.strip(),
                             'pm_source2'    : 'barchart',
                             'pm_s2_volume'  : pm_volume,
                             'last'          : cells[2].text.strip().split('$')[1],
                             'gap_percentage': gap_percentage })
            if created:
                stoncks.append(stonck)
    return stoncks


def scrape_stocks_statistics_barchart(driver, stocks):
    url = 'https://www.barchart.com/stocks/quotes/%s/profile'
    for stock in stocks:
        try:
            stock_url = url % stock.ticker
            print(stock.ticker)
            driver.get(stock_url)
            wait_random_seconds(min=3, max=5)
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, "html.parser")
            mc = soup.find(string=re.compile(r'^\s+Market\s+Capitalization,.+'))
            if mc:
                market_cap = mc.parent.find_next().find('span').text.strip().replace(',', '')
                if mc.strip()[-1] == 'K':
                    market_cap = int(market_cap) * 1000
                stock.pm_s2_market_cap = market_cap
            sa = soup.find(string=re.compile(r'^\s+Shares\s+Outstanding,.+'))
            if sa:
                shares_outstanding = sa.parent.find_next().find('span').text.strip().replace(',', '')
                if sa.strip()[-1] == 'K':
                    shares_outstanding = int(shares_outstanding) * 1000
                stock.pm_s2_shares_outstanding = shares_outstanding
            fl = soup.find(string=re.compile(r'^\s+Float.+'))
            if fl:
                float = fl.parent.find_next().find('span').text.strip().replace(',', '')
                if fl.strip()[-1] == 'K':
                    float = int(float) * 1000
                stock.pm_s2_float = float
            pinsi = soup.find(string=re.compile(r'^\s+%\sof\sInsider\sShareholders.+'))
            if pinsi:
                held_percent_insiders = pinsi.parent.find_next().find('span').text.strip().replace(',', '')
                if '%' in held_percent_insiders:
                    held_percent_insiders = Decimal(held_percent_insiders.split('%')[0]) / 100
                stock.pm_s2_held_percent_insiders = held_percent_insiders
            pinst = soup.find(string=re.compile(r'^\s+%\sof\sInstitutional\sShareholders.+'))
            if pinst:
                held_percent_institutions = pinst.parent.find_next().find('span').text.strip().replace(',', '')
                if '%' in held_percent_institutions:
                    held_percent_institutions = Decimal(held_percent_institutions.split('%')[0]) / 100
                stock.pm_s2_held_percent_institutions = held_percent_institutions
            ind = soup.find('h4', string='Sectors:')
            if ind:
                links = ind.parent.find_all('a')
                if links:
                    if len(links) >= 2:
                        industry = links[1].text.strip()
                    else:
                        industry = links[0].text.strip()
                    stock.industry = industry
            stock.pm_source2 = 'barchart scraping'
            stock.save()
        except Exception as e:
            date = timezone.now()
            driver.save_screenshot('WebsiteScreenShot%s.png' % date)
            print('Error parsing stocks')
            print(e)
    return stocks



@task(name='parse_gappers')
def parse_gappers():
    driver = False
    try:
        today = timezone.now()
        print('init')
        print('initializing driver')
        driver = ghost_driver()
        print('geting benzinga tickers')
        get_benzinga_premerket_tickers(driver)
        stocks = UpGapper.objects.filter(date__day=today.day, date__month=today.month, date__year=today.year)
        print('scraping barchart statistics')
        scrape_stocks_statistics_barchart(driver, stocks)
        print('parsing barcharts gappers')
        parse_gappers_barchart_and_filter()
        stocks = UpGapper.objects.filter(date__day=today.day, date__month=today.month, date__year=today.year)
        print('parsing yquery statstics')
        parse_stock_statistics_yquery(stocks)
        #print('hiting news api')
        #for s in stocks:
        #    stockNewsApi_get_resent_news(s.ticker, s.id)
        print('scraping news finviz')
        for s in stocks:
            print(s.ticker)
            scrape_finviz_news(driver, s.ticker, s.id)
            wait_random_seconds()
    except Exception as e:
        print('There has been an exception:', e)
        print('####### T R A C E B A C K #######')
        print(traceback.format_exc())
        print('####### T R A C E B A C K #######')
    finally:
        if driver:
            print('closing driver')
            driver.close()
            driver.quit()
            print('closing driver DONE')
        else:
            print('No Driver to close')


@task(name='test_print')
def test_print():
    today = timezone.now()
    string = 'this task is runing %s' % today
    print(string)
    return string



"""
     {'BRY': {'defaultKeyStatistics': {'52WeekChange': 1.3755102,
    #                               'SandP52WeekChange': 0.48798215,
    #                               'beta': 656.5119,
    #                               'bookValue': 8.933,
    #                               'category': None,
    #                               'dateShortInterest': '2021-03-31 00:00:00',
    #                               'enterpriseToEbitda': 3.92,
    #                               'enterpriseToRevenue': 1.916,
    #                               'enterpriseValue': 778131904,
    #                               'floatShares': 72924298,
    #                               'forwardEps': 0.78,
    #                               'forwardPE': 7.7683334,
    #                               'fundFamily': None,
    #                               'heldPercentInsiders': 0.013409999,
    #                               'heldPercentInstitutions': 0.96747,
    #                               'lastDividendDate': 1615507200,
    #                               'lastDividendValue': 0.04,
    #                               'lastFiscalYearEnd': '2020-12-31 00:00:00',
    #                               'lastSplitFactor': None,
    #                               'legalType': None,
    #                               'maxAge': 1,
    #                               'mostRecentQuarter': '2020-12-31 00:00:00',
    #                               'netIncomeToCommon': -262895008,
    #                               'nextFiscalYearEnd': '2022-12-31 00:00:00',
    #                               'pegRatio': -6.1,
    #                               'priceHint': 2,
    #                               'priceToBook': 0.6783052,
    #                               'profitMargins': -0.64744,
    #                               'sharesOutstanding': 80471000,
    #                               'sharesPercentSharesOut': 0.0082,
    #                               'sharesShort': 662891,
    #                               'sharesShortPreviousMonthDate': '2021-02-26 '
    #                                                               '00:00:00',
    #                               'sharesShortPriorMonth': 624218,
    #                               'shortPercentOfFloat': 0.0123000005,
    #                               'shortRatio': 1.62,
    #                               'trailingEps': -3.294},
    #      'quoteType': {'exchange': 'NMS',
    #                    'firstTradeDateEpochUtc': '2018-07-18 13:30:00',
    #                    'gmtOffSetMilliseconds': -14400000,
    #                    'longName': 'Berry Corporation',
    #                    'maxAge': 1,
    #                    'messageBoardId': 'finmb_255323',
    #                    'quoteType': 'EQUITY',
    #                    'shortName': 'Berry Corporation (bry)',
    #                    'symbol': 'BRY',
    #                    'timeZoneFullName': 'America/New_York',
    #                    'timeZoneShortName': 'EDT',
    #                    'underlyingSymbol': 'BRY',
    #                    'uuid': 'fb9bd122-b5fc-39e1-81d7-fff35cfba1ba'},
    #      'summaryDetail': {'algorithm': None,
    #                        'ask': 5.96,
    #                        'askSize': 3000,
    #                        'averageDailyVolume10Day': 301771,
    #                        'averageVolume': 333737,
    #                        'averageVolume10days': 301771,
    #                        'beta': 656.5119,
    #                        'bid': 5.94,
    #                        'bidSize': 4000,
    #                        'currency': 'USD',
    #                        'dayHigh': 6.36,
    #                        'dayLow': 5.85,
    #                        'dividendRate': 0.16,
    #                        'dividendYield': 0.028299998,
    #                        'exDividendDate': '2021-03-12 00:00:00',
    #                        'fiftyDayAverage': 5.606,
    #                        'fiftyTwoWeekHigh': 6.69,
    #                        'fiftyTwoWeekLow': 2.14,
    #                        'forwardPE': 7.7683334,
    #                        'fromCurrency': None,
    #                        'lastMarket': None,
    #                        'marketCap': 487597920,
    #                        'maxAge': 1,
    #                        'open': 6.22,
    #                        'previousClose': 5.82,
    #                        'priceHint': 2,
    #                        'priceToSalesTrailing12Months': 1.2008263,
    #                        'regularMarketDayHigh': 6.36,
    #                        'regularMarketDayLow': 5.85,
    #                        'regularMarketOpen': 6.22,
    #                        'regularMarketPreviousClose': 5.82,
    #                        'regularMarketVolume': 621254,
    #                        'toCurrency': None,
    #                        'tradeable': False,
    #                        'trailingAnnualDividendRate': 0.12,
    #                        'trailingAnnualDividendYield': 0.020618556,
    #                        'twoHundredDayAverage': 4.2442646,
    #                        'volume': 621254}}}
from gappers.tasks import *
gappers = UpGapper.objects.filter(date__day='23', date__year='2021',date__month='04').filter(pm_s2_held_percent_institutions__gt=1)
for g in gappers:
    if g.pm_s2_held_percent_insiders:
        g.pm_s2_held_percent_insiders = g.pm_s2_held_percent_insiders / 100
        g.save()
    if g.pm_s2_held_percent_institutions:
        g.pm_s2_held_percent_institutions = g.pm_s2_held_percent_institutions / 100
        g.save()

"""
