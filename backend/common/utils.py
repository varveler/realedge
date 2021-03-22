from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials


import os
import gspread
import random
import time

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
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # specify the desired user agent
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
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
    """
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": user_agent}})
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
    if "K" in amount_string or "M" in amount_string:
        asl = amount_string.split(" ")
        if asl[1] == "K":
            return int(float(asl[0]) * 1000)
        elif asl[1] == "M":
            return int(float(asl[0]) * 1000000)
    return 0

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
