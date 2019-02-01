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
        self.stock = None
        self.id = None
        self.href = None
        self.name = None
        self.price = None
        self.image = None
        self.returned_url = None
        self.product_dict = dict()

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
        """ Product SKU """
        self.product_dict['id'] = self.sku

        """ Product URL """
        self.product_dict['href'] = self.returned_url

        """ Product Image URL """
        r = self.response_object.find('img', {'class': 'product-image'})
        product_image = json.loads(r['data-media'])
        self.product_dict['image'] = 'https:{}'.format(product_image['565'])

        """ Product New Price """
        r = self.response_object.find('div', {'class': 'product-price'})
        self.product_dict['price'] = r.find('span', class_='new-price').text

        """ Product Name """
        r = self.response_object.find('h1', {'class': 'item-name'})
        self.product_dict['name'] = r.text

        r = self.response_object.find_all('span', {'id': 'product-size-select-productDetailPage'})
        self.product_dict['stock'] = {}
        for r in self.response_object.find_all('span', {'id': 'product-size-select-productDetailPage'}):
            size = r.find('input').attrs['data-size']
            stock = r.find('input').attrs['data-stock-level']
            self.product_dict['stock'].setdefault(size, stock)

        return self.product_dict


def run_script(sku):
    mainworker = NewIn()
    mainworker.build_url(sku)
    mainworker.get_request()
    mainworker.scrape()


sku = '203531|WHITE'
run_script(sku)