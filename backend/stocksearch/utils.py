import datetime
import pandas as pd
from yahooquery import Ticker

from common.utils import wait_random_seconds, atr




def calculate_red_gap_probability_and_ATR(df):
    '''
        Caluclates ATR and red gap probabilty on gaps
    '''
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
    if not df_today_data.empty: #today data is in the df
        index = df_today_data.index[0] - 1
    else:
        index = df.index.stop - 1
    stock_atr = round(df.loc[index]['ATR'], 2)
    mask = (df['date'] < start_date) & (df['date'] >= end_date)
    df = df.loc[mask]
    gaps_df = df[(df['gapPercent'] >= 10) & (df['RVOL'] >= 1.6)].copy()
    if gaps_df.empty:
        return 'N/A', '0', stock_atr
    else:
        observations = len(gaps_df.index)
        red_gap_probability = str(int((np.sum(gaps_df['move'] < 0) / observations) * 100))
        gaps_observations = str(observations)
        return red_gap_probability, gaps_observations, stock_atr

def parse_stocks_fundamentals_yquery(stocks, throttle=True):
    ''' given a list of Stock(object) complete their fundamentals'''
    for stock in stocks:
        print(stock.ticker, stock.name)
        if throttle:
            wait_random_seconds()
        data = Ticker(stock.ticker).get_modules(['quoteType', 'defaultKeyStatistics', 'summaryDetail'])
        try:
            if not stock.name:
                stock.name = data[stock.ticker]['quoteType'].get('longName', 'N/A')
            stock.beta = data[stock.ticker]['defaultKeyStatistics'].get('beta', 'N/A')
            stock.market_cap = data[stock.ticker]['summaryDetail'].get('marketCap', 'N/A')
            stock.shares_outstanding = data[stock.ticker]['defaultKeyStatistics'].get('sharesOutstanding', 'N/A')
            stock._float = data[stock.ticker]['defaultKeyStatistics'].get('floatShares', 'N/A')
            stock.held_insiders = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInsiders', 'N/A')
            stock.held_institutions = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInstitutions', 'N/A')
            stock.short_float = data[stock.ticker]['defaultKeyStatistics'].get('shortPercentOfFloat', 'N/A')
        except Exception as e:
            print('######Exception#######')
            print(stock.ticker, stock.name)
            print(e)
        if throttle:
            wait_random_seconds()
        df = Ticker(stock.ticker).history(period='5y')
        if isinstance(df, dict) or len(df.index) < 20:
            continue
        stock.red_gap_probability, stock.gaps_observations, stock.atr = calculate_red_gap_probability_and_ATR(df)
    return stocks


def parse_stock_fundamentals_yquery(stock, throttle=False):
    ''' given a single Stock(object) complete their fundamentals'''
    print(stock.ticker, stock.name)
    if throttle:
        wait_random_seconds()
    data = Ticker(stock.ticker).get_modules(['quoteType', 'defaultKeyStatistics', 'summaryDetail'])
    try:
        if not stock.name:
            stock.name = data[stock.ticker]['quoteType'].get('longName', 'N/A')
        stock.beta = data[stock.ticker]['defaultKeyStatistics'].get('beta', 'N/A')
        stock.market_cap = data[stock.ticker]['summaryDetail'].get('marketCap', 'N/A')
        stock.shares_outstanding = data[stock.ticker]['defaultKeyStatistics'].get('sharesOutstanding', 'N/A')
        stock._float = data[stock.ticker]['defaultKeyStatistics'].get('floatShares', 'N/A')
        stock.held_insiders = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInsiders', 'N/A')
        stock.held_institutions = data[stock.ticker]['defaultKeyStatistics'].get('heldPercentInstitutions', 'N/A')
        stock.short_float = data[stock.ticker]['defaultKeyStatistics'].get('shortPercentOfFloat', 'N/A')
    except Exception as e:
        print('######Exception#######')
        print(stock.ticker, stock.name)
        print(e)
    if throttle:
        wait_random_seconds()
    df = Ticker(stock.ticker).history(period='5y')
    if isinstance(df, dict) or len(df.index) < 20:
        stock.red_gap_probability = 'N/A'
        stock.gaps_observations = '0'
        stock.atr = 'N/A'
    else:
        stock.red_gap_probability, stock.gaps_observations, stock.atr = calculate_red_gap_probability_and_ATR(df)
    return stock