import requests
import bs4
import logging
import json


class NewIn(object):

    def __init__(self):
        self.domain = 'https://www.joules.com/'
        self.parts = 'a/b/c/d/e?id='
        self.url = None
        self.sku = None
        self.response_object = None
        self.product_id = None
        self.product_href = None
        self.product_name = None
        self.product_price = None
        self.product_wasprice = None
        self.product_waswasprice = None
        self.product_image = None
        self.returned_url = None
        self.product_dict = dict()
        self.product = None

    def dict(self, product):
        self.product = product
        self.product_dict[f'{self.product}'] = {}

    def build_url(self, sku):
        self.sku = sku
        url_parts = [self.domain, self.parts, self.sku]
        self.url = ''.join(url_parts)
        return self.url

    def get_request(self):
        logging.captureWarnings(True)
        response = requests.get(self.url, verify=False, allow_redirects=True)
        self.returned_url = response.url
        if response.status_code == 200:
            self.response_object = bs4.BeautifulSoup(response.text, "html.parser")

    def scrape(self):
        """ Product Image URL """
        r = self.response_object.find('img', {'class': 'product-image'})
        product_image = json.loads(r['data-media'])
        self.product_image = 'https:{}'.format(product_image['565'])

        """ New Price """
        price_object = self.response_object.find('div', {'class': 'product-price'})
        self.product_price = price_object.find('span', class_='new-price').text

        """ Was Price """
        if price_object.find("span", class_='old-price'):
            old_price_container = price_object.find("span", class_='old-price')
            try:
                div = old_price_container.find("div", {"id": "was-productDetailPage"}).text
                self.product_wasprice = div.strip(' \t\n\r')
            except AttributeError:
                pass

            """ Was Was Price """
            try:
                div = old_price_container.find("div", {"id": "wasWas-productDetailPage"}).text
                self.product_waswasprice = div.strip(' \t\n\r')
            except AttributeError:
                pass

        """ Product Name """
        r = self.response_object.find('h1', {'class': 'item-name'})
        self.product_name = r.text
        self.product_dict[f'{self.product}'][f'product_id'] = self.sku
        self.product_dict[f'{self.product}'][f'product_name'] = self.product_name
        self.product_dict[f'{self.product}'][f'product_href'] = self.returned_url
        self.product_dict[f'{self.product}'][f'product_image'] = self.product_image
        self.product_dict[f'{self.product}'][f'product_price'] = self.product_price
        self.product_dict[f'{self.product}'][f'product_wasprice'] = self.product_wasprice
        self.product_dict[f'{self.product}'][f'product_waswasprice'] = self.product_waswasprice

        return self.product_dict


def run_script(sku):
    mainworker = NewIn()
    mainworker.dict(product='Product_01')
    mainworker.build_url(sku)
    mainworker.get_request()
    your_name = mainworker.scrape()
    print(your_name)

run_script(sku='203531|WHITE')