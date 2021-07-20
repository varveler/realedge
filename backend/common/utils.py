from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials
#import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import gspread
import random
import time
from decimal import Decimal
import datetime
import pytz
#from webdriver_manager.chrome import ChromeDriverManager

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise Exception(error_msg)

#CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
#CHROMEDRIVER_PATH = '~/chromedriver'
#CHROMEDRIVER_PATH = '../backend/drivers/chromedriver'
CHROMEDRIVER_PATH = get_env_variable('CHROMEDRIVER_PATH')





def ghost_driver():
    options = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # specify the desired user agent
    options.add_argument(f'user-agent={user_agent}')
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
    driver = webdriver.Remote("http://hub:4444/wd/hub", desired_capabilities=options.to_capabilities())

    #driver = webdriver.Chrome(chrome_options=options)
    '''
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, "languages", {
          get: function() {
            return ["en", "es"];
          }
        });
        Object.defineProperty(navigator, "plugins", {
          get: () => new Array(Math.floor(Math.random() * 6) + 1),
        });
        Object.defineProperty(navigator, "webdriver", {
          get: () => false,
        });
        const elementDescriptor=Object.getOwnPropertyDescriptor(HTMLElement.prototype, "offsetHeight");
        Object.defineProperty(HTMLDivElement.prototype, "offsetHeight", {
            ...elementDescriptor,
          get: function() {
            if (this.id === "modernizr") {
              return 1;
            }
            return elementDescriptor.get.apply(this);
          },
        });
        ["height", "width"].forEach(property => {
          const imageDescriptor=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);
          Object.defineProperty(HTMLImageElement.prototype, property, {
            ...imageDescriptor,
            get: function() {
              // return an arbitrary non-zero dimension if the image failed to load
              if (this.complete && this.naturalHeight == 0) {
                return 24;
              }
              // otherwise, return the actual dimension
              return imageDescriptor.get.apply(this);
            },
          });
        });
        const getParameter=WebGLRenderingContext.getParameter;
        WebGLRenderingContext.prototype.getParameter=function(parameter) {
          if (parameter === 37445) {
            return "Intel Open Source Technology Center";
          }
          if (parameter === 37446) {
            return "Mesa DRI Intel(R) Ivybridge Mobile";
          }
          return getParameter(parameter);
        };

    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": user_agent}})
    '''
    return driver


def get_sheet(worksheet=None):
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials2.json', scope)
    client = gspread.authorize(creds)
    if worksheet:
        sheet = client.open('Log').worksheet(worksheet)
    else:
        sheet = client.open('Log').sheet1
    return sheet


def str_date(date):
    return date.strftime("%m/%d/%Y")


def wait_time():
    time.sleep(0.3)


def update_cell_and_wait(sheet, row, col, data, name=None):
    if name:
        print('%s:  %s' % (name, data))
    sheet.update_cell(row, col, data)
    wait_time()


def convert_amount(amount_string):
    """
    Converts any string in the format of 20.0 M or 811K to 20,000,000 or 811,000"
    """
    amount_string = amount_string.replace(',','')
    if "K" in amount_string or "M" in amount_string:
        asl = amount_string.split(" ")
        if asl[1] == "K":
            return int(float(asl[0]) * 1000)
        elif asl[1] == "M":
            return int(float(asl[0]) * 1000000)
    return 0


def convert_amount_benzinga(amount):
    """
    Converts any string in the format of 20.0 M or 811K to 20,000,000 or 811,000"
    """
    amount = amount.replace(',','')
    if "K" in amount or "M" in amount:
        if amount[-1] == "K":
            return int(float(amount[:-1]) * 1000)
        elif amount[-1] == "M":
            return int(float(amount[:-1]) * 1000000)
    return int(float(amount))



def next_available_row_to_update(worksheet, column_header='_Stock_'):
    column = worksheet.find(column_header).col
    str_list = list(filter(None, worksheet.col_values(column)))  # fastest
    return len(str_list) + 1


def wait_random_seconds(min=2, max=4):
    rand_time = random.randint(min, max)
    print('Waiting %s Seconds...' % rand_time)
    time.sleep(rand_time)

def wwma(values, n):
    """
     J. Welles Wilder's EMA
    """
    return values.ewm(alpha=1/n, adjust=False).mean()


def atr(df, n=14):
    data = df.copy()
    high = data['high']
    low = data['low']
    close = data['close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return len(str_list) + 1


class Stock(object):
    name = ''
    ticker = ''
    industry = ''
    gap_percentage = 0.0
    price = 0.0
    price_gap = 0.0
    volume = 0
    market_cap = 0
    shares_outstanding = 0
    _float = 0
    held_insiders = 0.0
    held_institutions = 0.0
    short_float = 0.0
    atr = 0.0
    news = ''

    red_gap_probability = ''
    gaps_observations = ''


def human_readble_amount(amount):
    a = str(amount)
    length = len(a)
    if length <= 3:
        return a
    if length <= 6:
        crop = length - 3
        return a[:crop] + 'K'
    crop = length - 6
    return a[:crop] + '.' + a[crop + 1] + 'M'


# not mine https://stackoverflow.com/questions/11227620/drop-trailing-zeros-from-decimal
def remove_zeros(num):
    return num.to_integral() if num == num.to_integral() else num.normalize()


def convert_percentage_to_decimal(a_string):
    return float(a_string.split('%')[0]) / 100


def fix_percentage_barchart_api(amount):
    if isinstance(amount, str):
        return Decimal(amount) / 100
    if not amount:
        return amount
    return Decimal(str(amount)) / 100

def tradeZeroDateTimeObject(str):
    return datetime.datetime.strptime(str, '%H:%M:%S %Y/%m/%d %z')

def tradeZeroDateTimeString(str):
    return tradeZeroDateTimeObject(str).strftime('%Y-%m-%d %H:%M:%S')

def iex_convert_epoch_to_dt(timestamp):
    timestamp = int(str(timestamp)[:10])
    convertion = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    #print(convertion)
    return convertion

"""
US_EASTERN_TZ = pytz.timezone('US/Eastern')
def convert_strUTC_to_aware_dt(string):
    "transform incoming data from alpaca like 2021-04-07T13:34:00Z to dt object"
    time = string.replace('Z', '-UTC')
    format = '%Y-%m-%dT%H:%M:%S-%Z'
    utc_dt = datetime.datetime.strptime(time, format)
    est_dt = utc_dt.astimezone(US_EASTERN_TZ)
    print(est_dt.strftime(format))
    return est_dt
"""


format = '%Y-%m-%dT%H:%M:%S-%Z'
US_EASTERN_TZ = pytz.timezone('US/Eastern')
utc = pytz.utc
def convert_str_to_est_dt(s,v):
    s = s.replace('T', '-').replace('Z','').replace(':', '-')
    l = [int(n) for n in s.split('-')]
    dt_utc = datetime.datetime(l[0], l[1], l[2], l[3], l[4], l[5], tzinfo=utc)
    dt_east = dt_utc.astimezone(US_EASTERN_TZ)
    #print(dt_east.strftime(format), v)
    return dt_east
