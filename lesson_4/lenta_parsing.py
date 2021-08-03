from lxml import html
import requests
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['lesson_4']
persons = db.persons


url_u = 'https://lenta.ru/'
headers = {'User Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4421.5 Safari/537.36'}

response = requests.get(url_u, headers=headers)

dom = html.fromstring(response.text)


items = dom.xpath("//div[@class='span4']/div[@class='item']")
list_news = []
for item in items:
    data_new = {}

    name_news = item.xpath(".//a/text()")
    url = item.xpath(".//a/@href")
    name_sours = re.findall(r"\/\/([\w\-]+).\w+", f'{url}')
    if str(url[0])[1:5] == 'news':
        url = url_u + str(url[0])
        name_sours = re.findall(r"\/\/([\w\-]+).\w+", f'{url}')
        name_sours = [name_sours[0]]

    publication_date = item.xpath(".//a/time/@datetime")
    data_new['name_sours'] = name_sours
    data_new['name_news'] = name_news
    data_new['url'] = url
    data_new['publication_date'] = publication_date

    list_news.append(data_new)

persons.insert_many(list_news)

