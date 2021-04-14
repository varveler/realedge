# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
# from common.utils import get_env_variable, get_sheet, str_date, update_cell_and_wait,
from common.utils import (convert_amount, wait_random_seconds,
                          ghost_driver, Stock, next_available_row_to_update,
                          str_date, get_sheet, update_cell_and_wait, atr)
from yahooquery import Ticker
#from pyvirtualdisplay import Display

# from gapdb import probabilty_red_gap_yq_all_in_one, atr
from gappers.models import UpGapper
from celery.decorators import task

import datetime
import time
import requests
from urllib.parse import unquote
# import random
# import re
# import json
# import yfinance as yf
# import pytz
# import sys
import pandas as pd
import numpy as np


# frontier values
MIN_PREMARKET_VOLUME = 50000  # int
MAX_PRICE = 101.0  # float
MAX_GAP_PERCENTAGE = 9.0  # float
MIN_GAP_PERCENTAGE = -9.0  # float
GAP_UP_MIN_GAP = 0.05  # 5%
GAP_DOWN_MIN_GAP = -0.05

# home_folder_name = get_env_variable('HOME_FOLDER_NAME')
# FIREFOX_PROFILE = '/home/%s/.mozilla/firefox/r8abwwfd.default' % home_folder_name

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
            stonck = UpGapper(
                date                             = datetime.date.today(),
                ticker                           = stock['raw'].get('symbol', ''),
                market                           = stock['raw'].get('exchange', ''),
                company_name                     = stock['raw'].get('symbolName', ''),
                industry                         = stock['raw'].get('industry', ''),
                pm_source2                       = 'barchart',
                pm_s2_volume                     = stock['raw'].get('volume', 0),
                pm_s2_market_cap                 = stock['raw'].get('marketCap', 0),
                pm_s2_shares_outstanding         = stock['raw'].get('sharesOutstanding', 0),
                pm_s2_float                      = stock['raw'].get('float', 0.0),
                pm_s2_held_percent_insiders      = stock['raw'].get('percentInsider', 0.0),
                pm_s2_held_percent_institutions  = stock['raw'].get('percentInstitutional', 0.0),
                gap_percentage                   = stock['raw'].get('gapUpPercent', 0.0),
                last                             = stock['raw'].get('lastPrice', 0.0),
                gap                              = stock['raw'].get('gapUp', 0.0))
            stonck.save()
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
        print(stock.ticker, stock.company_name)
        wait_random_seconds(min=1, max=3)
        data = Ticker(stock.ticker).get_modules(['quoteType', 'defaultKeyStatistics', 'summaryDetail'])
        print(data)
        try:
            if not stock.company_name:
                stock.company_name = data[stock.ticker]['quoteType'].get('longName', None)
            stock.pm_s1_beta = data[stock.ticker]['defaultKeyStatistics'].get('beta', None)
            stock.pm_s1_market_cap = data[stock.ticker]['summaryDetail'].get('marketCap', None)
            stock.pm_s1_shares_outstanding = data[stock.ticker]['defaultKeyStatistics'].get('sharesOutstanding', None)
            stock.pm_s1_float = data[stock.ticker]['defaultKeyStatistics'].get('floatShares', None)
            stock.pm_s1_held_percent_insiders = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInsiders', None)
            stock.pm_s1_held_percent_institutions = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInstitutions', None)
            stock.pm_s1_short_float = data[stock.ticker]['defaultKeyStatistics'].get('sharesPercentSharesOut', None)
            stock.pm_s1_shares_short = data[stock.ticker]['defaultKeyStatistics'].get('sharesShort', None)
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

@task(name='parse_gappers')
def parse_gappers():
    stocks = parse_gappers_barchart_and_filter()
    parse_stock_statistics_yquery(stocks)
