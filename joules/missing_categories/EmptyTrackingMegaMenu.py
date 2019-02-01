# -*- coding: utf-8 -*-
# python 3.x

import requests
import bs4
import logging

"""
    Captures the InsecureRequestWarning (HTTPS SSL Verification Error)
"""
logging.captureWarnings(True)


class Main(object):

    def __init__(self):
        self.mega_menu_404 = []
        self.missing_product = []
        self.mm_list_unfiltered = []
        self.list_purge_duplicates = []
        self.empty_tracking_list = []
        self.mega_menu_url_list = []
        self.list_purge_duplicates = []
        self.list_purge_duplicates_one = []
        self.list_purge_duplicates_two = []
        self.parse_soup = None
        self.product_dict = dict()
        self.domain_url = None

    def html_object_soup(self, url):
        """
        HTTP request to store html as an object
        """
        self.domain_url = url
        for i in range(len(url)):
            res = requests.get(url[i], verify=False)

            if res.status_code == 200:
                self.parse_soup = bs4.BeautifulSoup(res.text, "html.parser")
                # print("The Status Code returned is", res.status_code, url[i])

                if len(url) > 1:
                    """
                        Searches for product pages with 0 products and appends to a list object
                    """
                    for product in self.parse_soup.find_all('div', {"class": "totalResults"}):
                        self.missing_product.append(url[i])

            elif res.status_code == 404:
                # print("The Status Code returned is", res.status_code, url[i])
                self.mega_menu_404.append(url[i])

            else:
                # print("The Status Code returned is", res.status_code, url[i])
                pass

    def mega_menu_list_unfiltered(self):
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

    def filter_external_urls(self):
        """
            Filter out external urls such as blog/pinterest
        """
        global list_purge_external_urls
        list_purge_external_urls = list(self.list_purge_duplicates)

        [list_purge_external_urls.remove(i) for i in self.list_purge_duplicates if i.__contains__('.')]

    def iterate(self):
        for i in list_purge_external_urls:
            for j in self.domain_url:
                self.mega_menu_url_list.append(j + i)

    def write_out(self):
        """
           Product Pages with 0 products
        """
        return self.missing_product


def run_script(env):
    worker = Main()
    worker.html_object_soup(url=env)
    worker.mega_menu_list_unfiltered()
    worker.nav_list_duplicates()
    worker.filter_external_urls()
    worker.iterate()
    print(worker.mega_menu_url_list)
    worker.html_object_soup(url=worker.mega_menu_url_list)
    """ for testing only """
    # worker.html_object_soup(url=['https://www.joules.com/Girls-Clothing/Little-Joule-Characters', 'https://www.joules.com/Girls-Clothing/Slippers', 'https://www.joules.com/Boys-Clothing/Slippers'])
    lst = worker.write_out()
    print(lst)
    return lst


live = [['https://www.joules.com'], ['https://www.joulesusa.com'], ['https://www.tomjoule.de']]
run_script(env=live[0])
