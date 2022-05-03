import networkx as nx
import requests
from urllib.parse import urljoin
import random
import time
import re

from collections import defaultdict, deque
from bs4 import BeautifulSoup
from utils import domain_from
from HypeParameters import data_regex, crw_Data


def set_crawlers(urls, max_links=4, max_urls=40):
    urls = urls if isinstance(urls, list) else [urls]
    return [CrawlingObject(crawl_name=f'crawl {idx + 1}', main_url=url,
                           max_length=max_links, max_urls=max_urls) for idx, url in enumerate(urls)]


class CrawlingObject:

    def __init__(self, crawl_name, main_url, max_length=4, max_urls=100):
        self.crawl_name = crawl_name
        self.main_url = main_url
        self.max_length = max_length
        self.MAX_URLS = max_urls

        self.knowlage_graph = nx.Graph()
        self.domain_graph = nx.Graph()

        self.main_url_attrs = crw_Data.main_url_attrs
        self.urls_attrs = crw_Data.urls_attrs
        self.empty_urls_attrs = crw_Data.empty_urls_attrs
        self.data_attrs = crw_Data.data_attrs

        self.edge_urls_attrs = crw_Data.edge_urls_attrs
        self.edge_data_attrs = crw_Data.edge_data_attrs

        self.main_url_attrs_domain = crw_Data.main_url_attrs_domain
        self.urls_attrs_domain = crw_Data.urls_attrs_domain
        self.empty_urls_attrs_domain = crw_Data.empty_urls_attrs_domain
        self.data_attrs_domain = crw_Data.data_attrs_domain

        self.legends = crw_Data.legends
        self.legends_domain = crw_Data.legends_domain

        self.DATA_REGEX = data_regex
        self.datas = set()
        self.visited_urls = set()
        self.datas_dict = defaultdict(lambda: defaultdict(lambda: set()))
        self.All_viseted_URLS_2 = None
        self.locking = None
        self.time = 0

    def set_visited_urls_dict(self, set_visited_urls_dict, locking):
        self.All_viseted_URLS_2 = set_visited_urls_dict
        self.locking = locking

    def __repr__(self):
        return f'crawler {self.crawl_name} (main_url={self.main_url}, ' \
               f'max_length={self.max_length}, max_urls={self.MAX_URLS})'

    def extract_data(self, response, shuffle=True):
        doc = BeautifulSoup(response.text, "html.parser")
        url_links = doc.find_all('a', href=True, limit=20*self.max_length)

        if shuffle:
            random.shuffle(url_links)

        urls_datas = set(re.findall(self.DATA_REGEX, response.text, re.I))
        return list(url_links), list(urls_datas), response.status_code

    def add_datas_to_graphs(self, url, datas):
        domain = domain_from(url)
        for dat in datas:
            self.datas.add(dat)
            self.knowlage_graph.add_node(dat, **self.data_attrs)
            self.knowlage_graph.add_edge(url, dat, **self.edge_data_attrs)

            self.domain_graph.add_node(dat, **self.data_attrs_domain)
            self.domain_graph.add_edge(domain, dat, **self.edge_data_attrs)

            self.datas_dict[domain][url].add(dat)

    def add_urls_to_graphs(self, curr_url, new_url):
        curr_domain = domain_from(curr_url)
        new_domain = domain_from(new_url)
        self.knowlage_graph.add_node(new_url, **self.urls_attrs)
        self.knowlage_graph.add_edge(curr_url, new_url, **self.edge_urls_attrs)
        if new_domain != curr_domain:
            self.domain_graph.add_node(new_domain, **self.urls_attrs_domain)
            self.domain_graph.add_edge(curr_domain, new_domain, **self.edge_urls_attrs)

    def BFS(self):
        q = deque([self.main_url])
        total_urls = 1
        while q:
            first_url = q.popleft()
            try:
                response = requests.get(first_url)
            except:
                print(f'fail read {first_url}')
                total_urls -= 1
                continue

            domain = domain_from(first_url)
            hyper_links, new_datas, status_code = self.extract_data(response)

            self.locking.acquire()
            exist_url = False
            if (domain in self.All_viseted_URLS_2.keys() and first_url in self.All_viseted_URLS_2[domain]) \
                    or '?' in first_url or '#' in first_url:
                exist_url = True
            self.locking.release()
            if exist_url:
                continue

            self.All_viseted_URLS_2[domain].add(first_url)
            self.add_datas_to_graphs(first_url, new_datas)
            self.visited_urls.add(first_url)
            print(f'{self.crawl_name} go to : {first_url} ({len(self.visited_urls)}/{self.MAX_URLS})')

            add_urls = 0
            for new_url in hyper_links:
                new_url = urljoin(first_url, new_url['href'])
                if total_urls == self.MAX_URLS or add_urls == self.max_length:
                    break
                if 'http' not in new_url or '.pdf' in new_url:
                    continue
                if new_url not in self.knowlage_graph.nodes():
                    total_urls += 1
                    add_urls += 1
                    q.append(new_url)
                    self.add_urls_to_graphs(first_url, new_url)

            if not hyper_links:
                self.knowlage_graph.add_node(first_url, **self.empty_urls_attrs)

    def crawl(self):
        start_time = time.time()
        self.knowlage_graph.add_node(self.main_url, **self.main_url_attrs)
        self.domain_graph.add_node(domain_from(self.main_url), **self.main_url_attrs_domain)
        self.BFS()
        end_time = time.time()
        self.time = end_time - start_time
