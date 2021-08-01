from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['user']

persons = db.persons
wage = int(input('Введите сумму: '))
def print_vac_wage(wage):
    for doc in persons.find({'$or': [{'wage_max': {'$gt': wage}}, {'wage_min': {'$lt': wage}}]}):
        pprint(doc)


print_vac_wage(wage)

