from common.utils import ghost_driver, wait_random_seconds
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gappers.models import UpGapper
from news.models import News

from bs4 import BeautifulSoup
import datetime



class Row(object):
    date = ''
    headline = ''

# finviz
def scrape_finviz_news(driver, ticker, up_gapper_id=None):
    no_news_found = False
    url = 'https://finviz.com/quote.ashx?t=%s' % ticker
    driver.get(url)
    try:
        wait = WebDriverWait(driver, timeout=20, poll_frequency=0.1)
        wait.until(EC.presence_of_element_located((By.ID, "news-table")))
    except:
        print('Waited and "news-table" id was not found for %s' % ticker)
        no_news_found = True
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    if no_news_found:
        print('No news was found for %s' % ticker)
    elif 'No results found for' in html_source:
        print("'No results found for' was found in html", "No news was found for %s" % ticker)
    elif 'item(s) found in screener)' in html_source:
        print("'item(s) found in screener)' was found in html",  "No news was found for %s" % ticker)
    else:
        news_itemsss = []
        table = soup.find(id='news-table')
        news_rows = table.find_all("tr")[:11]
        for i, row in enumerate(news_rows):
            print(i)
            cells = row.find_all("td")
            news_item = Row()
            if cells:
                print(cells[1].text)
                str_date = cells[0].text.strip()
                print(str_date)
                if '-' not in str_date:
                    print('searching prev day objs: ', news_itemsss)
                    prev_news_day_obj = news_itemsss[i - 1]
                    prev_news_day = prev_news_day_obj.date.split(' ')[0]
                    print('prev_news_day', prev_news_day)
                    str_date = prev_news_day + ' ' + str_date
                news_item.date = datetime.datetime.strptime(str_date, '%b-%d-%y %I:%M%p').strftime("%b-%d-%y %H:%M:%S")
                news_item.headline = cells[1].text
                news_itemsss.append(news_item)
                date = datetime.datetime.strptime(str_date + ' -0400', '%b-%d-%y %I:%M%p %z')
                obj, created = News.objects.get_or_create(
                    internal_source = 'scraping Finviz',
                    title = cells[1].text,
                    publish_date = date,
                    defaults = {
                        'source' : cells[1].find_all('span')[0].text,
                        'url' : cells[1].a.get('href')
                    }
                )
                obj_tickers = obj.tickers.split(',')
                if ticker not in obj_tickers:
                    obj_tickers.append(ticker)
                    obj.tickers = ', '.join([t for t in obj_tickers if t])
                    obj.save()
                if up_gapper_id:
                    ug = UpGapper.objects.get(id=up_gapper_id)
                    obj.up_gapper.add(ug)

stocks = UpGapper.objects.all()[:2]
stocks

driver = ghost_driver()
for s in stocks:
    scrape_finviz_news(driver, s.ticker, s.id)
    wait_random_seconds(min=8, max=10)



















no_news_found = False
url = 'https://finviz.com/quote.ashx?t=FOE'
driver.get(url)
try:
    wait = WebDriverWait(driver, timeout=20, poll_frequency=0.1)
    wait.until(EC.presence_of_element_located((By.ID, "news-table")))
except:
    print('Waited and "news-table" id was not found for %s' % ticker)
    no_news_found = True
html_source = driver.page_source
soup = BeautifulSoup(html_source, "html.parser")

news_itemsss = []
table = soup.find(id='news-table')
news_rows = table.find_all("tr")[:11]

row = news_rows[0]
cells = row.find_all("td")
news_item = Row()

str_date = cells[0].text.strip()
str_date
'-' not in str_date
news_item.date = datetime.datetime.strptime(str_date, '%b-%d-%y %I:%M%p').strftime("%b-%d-%y %H:%M:%S")
news_item.headline = cells[1].text
news_itemsss.append(news_item)
date = datetime.datetime.strptime(str_date + ' -0400', '%b-%d-%y %I:%M%p %z')
obj, created = News.objects.get_or_create(
            internal_source = 'scraping Finviz',
            title = cells[1].text,
            publish_date = date,
            defaults = {
                'source' : cells[1].find_all('span')[0].text,
                'url' : cells[1].a.get('href')
            }
        )
obj












"""
from news.tasks import stockNewsApi_get_resent_news

last = UpGapper.objects.all()[:17]

for s in last:
    stockNewsApi_get_resent_news(s.ticker, s.id)

tickers = ['AAPL', 'FB']
str_tickers = ','.join(tickers)
TOKEN_API_stockNewsApi = get_env_variable('TOKEN_API_stockNewsApi')
url = 'https://stocknewsapi.com/api/v1?tickers={tickers}&items=10&token={token}'.format(tickers=str_tickers, token=TOKEN_API_stockNewsApi)
response = requests.get(url)
response
response.status_code
data = response.json()
up_gapper_id = ugid
up_gapper_id
bool(up_gapper_id)
if data['data']:
    news = data['data']
    for n in news:
        obj, created = News.objects.get_or_create(
            internal_source = 'stockNewsApi',
            title = n['title'],
            defaults = {
                'publish_date' : str_to_dt_stockNewsAPI(n['date']),
                'publish_time_epoc' : str_to_epoch_stockNewsAPI(n['date']),
                'source' : n['source_name'],
                'title' : n['title'],
                'summary' : n['text'],
                'tickers' : ', '.join(n['tickers']),
                'url' : n['news_url'],
                'img_url' : n['image_url'],
                'sentiment' : n['sentiment'],
            }
        )
        if up_gapper_id and created:
            ug = UpGapper.objects.get(id=up_gapper_id)
ug
obj = News.objects.last()
obj
obj.up_gapper.add(ug)
"""
