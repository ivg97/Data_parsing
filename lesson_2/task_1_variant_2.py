from bs4 import BeautifulSoup as bs
import requests
import json

url = 'https://roscontrol.com'
additionally = '/category/produkti'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
full_url = url + additionally
url_list = []
result_list = []
def parse_product(url, params=None, headers=headers):


    response = requests.get(url, headers=headers)
    html = response.text
    soup = bs(html, 'html.parser')
    products = soup.find_all('div', attrs={'class': 'grid-padding grid-column-3 grid-column-large-6 grid-flex-mobile grid-column-middle-6 grid-column-small-12 grid-left'})
    for product in products:
        url_p = full_url + product.find('a', attrs={'class': 'catalog__category-item util-hover-shadow'}).get('href')
        url_list.append(url_p)
        parse_product(url_p, headers)

    return url_list


lst = parse_product(full_url, headers)
lst = list(set(i for i in lst if i.count('/') > 8))
pages = 15
for page in range(pages):
    for i in lst:
        response = requests.get(i, headers=headers, params={'page': page})
        html = response.text
        soup = bs(html, 'html.parser')
        prds = soup.find_all('div', attrs={'class': 'wrap-product-catalog__item grid-padding grid-column-4 grid-column-large-6 grid-column-middle-12 grid-column-small-12 grid-left js-product__item'})

        for prd in prds:
            data_p = {}
            product_url = url + prd.find('a', attrs={'class': 'block-product-catalog__item js-activate-rate util-hover-shadow clear'}).get('href')
            product_name = prd.find('div', attrs={'class': 'product__item-link'}).getText()
            if prd.find('div', attrs={'class': 'rate'}) is None:
                overall_score = 'В чёрном списке'
            else:
                overall_score = prd.find('div', attrs={'class': 'rate'}).getText().strip()
            try:
                safety = prd.find_all('div', attrs={'class': 'row'})[0].find('div', attrs={'class': 'right'}).getText()
                naturalness = prd.find_all('div', attrs={'class': 'row'})[1].find('div', attrs={'class': 'right'}).getText()
                nutritional_value = prd.find_all('div', attrs={'class': 'row'})[2].find('div', attrs={'class': 'right'}).getText()
                quality = prd.find_all('div', attrs={'class': 'row'})[3].find('div', attrs={'class': 'right'}).getText()
            except IndexError:
                safety = 'В чёрном списке'
                naturalness = 'В чёрном списке'
                nutritional_value = 'В чёрном списке'
                quality = 'В чёрном списке'

            data_p['name'] = product_name
            data_p['url'] = product_url
            data_p['overall_score'] = overall_score
            data_p['safety'] = safety
            data_p['naturalness'] = naturalness
            data_p['nutritional_value'] = nutritional_value
            data_p['quality'] = quality
            result_list.append(data_p)

with open('shop_products.json', 'w', encoding='utf-8') as f:
    json.dump({'products': result_list}, f, indent=4, ensure_ascii=False)




















