# -*- coding: utf-8 -*-
# python 3.x

import time
import requests
import bs4
import logging
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession

"""
    Captures the InsecureRequestWarning (HTTPS SSL Verification Error)
"""
logging.captureWarnings(True)
session = HTMLSession()


class Main(object):

    def __init__(self):
        self.missing_product = []
        self.mm_list_unfiltered = []
        self.list_purge_duplicates = []
        self.empty_tracking_list = []
        self.mega_menu_url_list = []
        self.list_purge_duplicates = []
        self.list_purge_duplicates_one = []
        self.list_purge_duplicates_two = []
        self.parse_soup = None
        self.domain_url = None

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

    def re(self, url):
        """
        HTTP request to store html as an object
        """
        r = session.get(url)

        if r.html.find('div.totalResults'):
            self.missing_product.append(url)

    def nav_list_unfiltered(self):
        """
            Stored list of navigation links from the mega menu // unfiltered
        """
        lst = self.parse_soup.find_all('li', {'class': 'yCmsComponent mobile-nav-item Lc'})

        for i in lst:
            self.mm_list_unfiltered.append(i.find("a").get("href"))
            # print(i.find("a").get("href"))

    def nav_list_duplicates(self):
        """
            Function to remove duplicates from a list, preserves original list order
        """

        """ Removes URLs start with &, these are JS injected """
        [self.list_purge_duplicates_one.append(i) for i in self.mm_list_unfiltered if not i.startswith('&')]

        """ Removes tracking """
        for i in self.list_purge_duplicates_one:
            if '?' in i:
                x = i.split('?')[0]
                self.list_purge_duplicates_two.append(x)
            elif '?' not in i:
                self.list_purge_duplicates_two.append(i)

        """ Removes duplicate URLS """
        [self.list_purge_duplicates.append(i) for i in self.list_purge_duplicates_two if not self.list_purge_duplicates.count(i)]

        return self.list_purge_duplicates

    def nav_filter_external(self):
        """
            Filter out external urls such as blog/pinterest
        """
        global list_purge_external_urls
        list_purge_external_urls = list(self.list_purge_duplicates)

        [list_purge_external_urls.remove(i) for i in self.list_purge_duplicates if i.__contains__('.')]

    def iterate(self):
        for i in list_purge_external_urls:
            self.mega_menu_url_list.append(self.domain_url + i)

    def write_out(self):
        """
           Product Pages with 0 products
        """
        return self.missing_product


def run_script(env):
    start_time = time.time()
    print(f'Running search on {env[0]}...')
    worker = Main()
    worker.request(url=worker.domain(url=env[0]))
    worker.nav_list_unfiltered()
    worker.nav_list_duplicates()
    worker.nav_filter_external()
    worker.iterate()

    with ThreadPoolExecutor(max_workers=10000) as pool:
        pool.map(worker.re, worker.mega_menu_url_list)

    print("--- %s seconds ---" % (time.time() - start_time))
    return worker.write_out()


if __name__ == '__main__':
    live = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk'], ['https://www.joulesusa.com'], ['https://www.tomjoule.de']]
    run_script(env=live[0])
