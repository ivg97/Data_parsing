from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from pprint import pprint
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['lesson_5']
persons = db.persons

path = os.path.abspath('chromedriver')
driver = webdriver.Chrome(path)
driver.implicitly_wait(15)
url = 'https://mail.ru/'

driver.get(url)
# time.sleep(1)
remember = driver.find_element_by_id('saveauth').click()
login = driver.find_element_by_name('login')
login.send_keys('study.ai_172')
login.send_keys(Keys.ENTER)
# time.sleep(1)
password = driver.find_element_by_name('password')
password.send_keys('NextPassword172!?')
password.send_keys(Keys.ENTER)


menu = driver.find_element_by_xpath("//a[@class = 'sidebar__menu-item']")
menu.click()

count_email = driver.find_element_by_xpath("//nav[contains(@class, 'nav nav_expanded nav_hover-support')]/a[1]").get_attribute('title')
count_email = int(count_email.split()[1]) // 8 # так как по 8 писем листает вниз

menu = driver.find_element_by_xpath("//a[@data-title =  'Все фильтры']")
time.sleep(3)
menu.click()

list_data = []
res_data_list = []

for i in range(count_email):
    tegs_a = driver.find_elements_by_xpath("//a[contains(@class, 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal')]")
    for a in tegs_a:
        if a is not list_data:
            list_data.append(a)
        else:
            pass
#
    actions = ActionChains(driver)
    actions.move_to_element(tegs_a[-1])
    actions.perform()

list_data = set(list_data)

for a in list_data:
    data_list = {}
    from_who = a.find_element_by_xpath("//span[@class = 'll-crpt']")
    from_who = from_who.get_attribute('title')
    data = a.find_element_by_xpath("//div[@class = 'llc__item llc__item_date']")
    data = data.text
    theme = a.find_element_by_xpath("//span[@class = 'll-sj__normal']")
    theme = theme.text
    text = a.find_element_by_xpath("//span[@class = 'll-sj__normal']")
    text = text.text
    data_list['from_who'] = from_who
    data_list['data'] = data
    data_list['theme'] = theme
    data_list[text] = text

    res_data_list.append(data_list)





# pprint(res_data_list)
# print(len(res_data_list))

persons.insert_many(res_data_list)


# print(remember)
