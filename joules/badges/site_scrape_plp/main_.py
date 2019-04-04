# -*- coding: utf-8 -*-
# python 3.x

from pathlib import Path
import os.path
import time
import requests
import bs4
import logging
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from openpyxl import load_workbook


logging.captureWarnings(True)
session = HTMLSession()


class Main(object):

    def __init__(self):
        self.missing_product = []
        self.mm_list_unfiltered = []
        self.purge_duplicates = []
        self.empty_tracking_list = []
        self.mega_menu_url_list = []
        self.purge_duplicates = []
        self.purge_duplicate_urls_one = []
        self.purge_duplicate_urls_two = []
        self.parse_soup = None
        self.domain_url = None
        self.product_list = []

    def domain(self, url):
        self.domain_url = url
        return self.domain_url

    def request(self, url):
        """
        HTTP request to store html as an object
        """
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            self.parse_soup = bs4.BeautifulSoup(r.text, "html.parser")

            if self.parse_soup.find_all('div', {"class": "totalResults"}):
                self.missing_product.append(url)

    def list_unfiltered(self):
        """
            Stored list of navigation links from the mega menu // unfiltered
        """
        lst = self.parse_soup.find_all('li', {'class': 'yCmsComponent mobile-nav-item Lc'})

        for i in lst:
            self.mm_list_unfiltered.append(i.find("a").get("href"))

    def list_duplicates(self):
        """
            Function to remove duplicates from a list, preserves original list order
        """

        """ Removes URLs start with &, these are JS injected """
        [self.purge_duplicate_urls_one.append(i) for i in self.mm_list_unfiltered if not i.startswith('&')]

        """ Removes tracking """
        for i in self.purge_duplicate_urls_one:
            if '?' in i:
                x = i.split('?')[0]
                self.purge_duplicate_urls_two.append(x)
            elif '?' not in i:
                self.purge_duplicate_urls_two.append(i)

        """ Removes duplicate URLS """
        [self.purge_duplicates.append(i) for i in self.purge_duplicate_urls_two if not self.purge_duplicates.count(i)]

        return self.purge_duplicates

    def filter_external(self):
        """
            Filter out external urls such as blog/pinterest
        """
        global list_purge_external_urls
        list_purge_external_urls = list(self.purge_duplicates)

        [list_purge_external_urls.remove(i) for i in self.purge_duplicates if i.__contains__('.')]

    def concatenate_url(self):
        """
            join menu links to domain
        """
        for url in list_purge_external_urls:
            self.mega_menu_url_list.append(self.domain_url + url)

    def category(self, url):
        """
            Iterate through each category URL and scrape information from the product listing pages
        """
        for j in range(100):
            html_doc = requests.get(str(url) + "?showFragment=true&page=" + str(j),
                                    verify=False,
                                    allow_redirects=False)

            soup = bs4.BeautifulSoup(html_doc.text, "html.parser")
            tags = soup.find_all("div", {"class": "product-grid-item-inner"})
            if tags:
                for i in tags:
                    """ New Price """
                    new_price = None
                    try:
                        new_temp = i.find('div', {'class': 'product-price'})
                        new_price = new_temp.find('span', class_='new-price').text
                    except:
                        pass

                    """ Was Price """
                    was_price = None
                    try:
                        c = new_temp.find("span", class_='old-price')
                        was_temp = c.find("div", {"id": "was-"}).text
                        was_price = was_temp.strip(' \t\n\r')
                    except:
                        pass
                    try:
                        was_temp = c.find("div", {"id": "wasFormated-"}).text
                        was_price = was_temp.strip(' \t\n\r')
                    except:
                        pass

                    """ Was Was Price """
                    waswas_price = None
                    try:
                        waswas_temp = c.find("div", {"id": "wasWas-"}).text
                        waswas_price = waswas_temp.strip(' \t\n\r')
                    except:
                        pass
                    try:
                        waswas_temp = c.find("div", {"id": "wasWasFormated-"}).text
                        waswas_price = waswas_temp.strip(' \t\n\r')
                    except:
                        pass

                    """ Image Badge Name """
                    img_badge = None
                    try:
                        o = i.find('div', {'id': 'badges'})
                        img_string = o.find('img')['src']
                        f = img_string.split('medias/')[1]
                        img_badge = f.split('?')[0]
                    except:
                        pass

                    """ Product ID """
                    product_id = None
                    try:
                        r = i.find('div', {'class': 'product-name'})
                        product_href = r.a['href']
                        product_id = product_href.split('?id=')[1]
                    except:
                        pass

                    """
                        get request to product landing page,
                        to collect 404, prices etc
                    """
                    tmp_lst = [[html_doc.status_code, product_id, img_badge, waswas_price, was_price, new_price]]
                    self.product_list.extend(tmp_lst)

            else:
                break

    def return_list(self):
        return self.product_list


def run_script(env):
    start_time = time.time()
    print(f'Running search on {env[0]}...')
    worker = Main()
    worker.request(url=worker.domain(url=env[0]))
    worker.list_unfiltered()
    worker.list_duplicates()
    worker.filter_external()
    worker.concatenate_url()

    with ThreadPoolExecutor(max_workers=1) as pool:
        pool.map(worker.category, worker.mega_menu_url_list)
        # pool.map(worker.category, ['https://www.joules.com/Home-and-Garden/Bathroom/Towels'])

    worker.return_list()
    print("--- %s seconds ---" % (time.time() - start_time))

    return worker.return_list()


if __name__ == '__main__':
    live = [['https://www.joules.com']]
    run_script(env=live[0])
