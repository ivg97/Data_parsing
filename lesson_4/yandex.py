from lxml import html
import requests
from pprint import pprint
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['lesson_4']
persons = db.persons


url_u = 'https://yandex.ru/news/'
headers = {'User Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4421.5 Safari/537.36'}

response = requests.get(url_u, headers=headers)

dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class, 'mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top')]/div")
list_news = []
for item in items:
    data_new = {}

    name_news = item.xpath(".//div[@class = 'mg-card__annotation']/text()")
    url = item.xpath(".//a[@class = 'mg-card__source-link']/@href")
    name_sours = item.xpath(".//span[@class = 'mg-card-source__source']/a/text()")
    # if str(url[0])[1:5] == 'news':
    #     url = url_u + str(url[0])
    #     name_sours = re.findall(r"\/\/([\w\-]+).\w+", f'{url}')
    #     name_sours = [name_sours[0]]

    publication_date = item.xpath(".//span[@class = 'mg-card-source__time']/text()")
    data_new['name_sours'] = name_sours
    data_new['name_news'] = name_news
    data_new['url'] = url
    data_new['publication_date'] = publication_date

    list_news.append(data_new)
pprint(list_news)
