from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
import bs4
import logging
import json

from .forms import NameForm


def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST or None)
        if form.is_valid():
            sku = form.cleaned_data['sku']
            run_script = NewIn()
            run_script.build_url(sku)
            run_script.get_request()
            product = run_script.scrape()

            return render(request, 'post.html', {'form': form, 'product': product})

    else:
        form = NameForm()

    return render(request, 'post.html', {'form': form})


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
        self.product_image = None
        self.returned_url = None
        self.product_dict = dict()

    def build_url(self, sku):
        """ build url """
        self.sku = sku
        url_parts = [self.domain, self.parts, self.sku]
        self.url = ''.join(url_parts)
        return self.url

    def get_request(self):
        """ disable insecure warning """
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

        """ Product Name """
        r = self.response_object.find('h1', {'class': 'item-name'})
        self.product_name = r.text

        """ add with product info to dictionary"""
        self.product_dict[f'product_id'] = self.sku
        self.product_dict[f'product_name'] = self.product_name
        self.product_dict[f'product_href'] = self.returned_url
        self.product_dict[f'product_image'] = self.product_image
        self.product_dict[f'product_price'] = self.product_price

        return self.product_dict