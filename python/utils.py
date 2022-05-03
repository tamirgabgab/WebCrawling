import re
import threading
import time
from collections import defaultdict
from pprint import pprint

import numpy as np
import requests
import tldextract

from HypeParameters import MAX_THREDS, data_name, data_regex

def domain_from(url):
    tld = tldextract.extract(url)
    domain = f'{tld.domain}.{tld.suffix}'
    return domain


def read_file(path):
    URLS = []
    with open(file=path, mode='r') as f:
        for line in f:
            URLS.append(line.strip())
    return URLS


def check_valid_url(url):
    return requests.get(url).status_code // 100 == 2


def to_dict(def_dict):
    for k in def_dict.keys():
        def_dict[k] = dict(def_dict[k])
    return dict(def_dict)


def get_datas(crawlers):
    all_datas = set()
    all_crawls_dict = {}
    for crw in crawlers:
        all_crawls_dict[crw.crawl_name] = to_dict(crw.datas_dict)
        for dat in crw.datas:
            all_datas.add(dat)
    return list(all_datas), all_crawls_dict


def to_seconds(time_string):
    converter = {'s': lambda x: x,
                 'm': lambda x: 60 * x,
                 'h': lambda x: 60 * 60 * x,
                 'd': lambda x: 60 * 60 * 24 * x,
                 'w': lambda x: 60 * 60 * 27 * 7 * x}
    T, units = float(time_string[:-1]), time_string[-1]
    return converter[units](T)


def crawl_urls(crawlers, thred=1, timeout='100s'):
    num_urls = len(crawlers)
    timeout_val = to_seconds(timeout)
    thred = min(thred, num_urls, MAX_THREDS)
    subset_index_urls = [a.tolist() for a in np.array_split(np.arange(num_urls).astype(int), thred)]

    All_viseted_URLS = defaultdict(lambda: set())
    data_lock = threading.Lock()

    def subset_crawl(subset_idx_urls, visited_urls, d_lock):
        for idx in subset_idx_urls:
            crawlers[idx].set_visited_urls_dict(visited_urls, d_lock)
            crawlers[idx].crawl()

    def make_threds(crw_threds):
        for thr in crw_threds:
            thr.start()

        for thr in crw_threds:
            thr.join(timeout_val / num_urls)

    crwlers_threds = [threading.Thread(target=subset_crawl, args=(idxs, All_viseted_URLS, data_lock), daemon=True) for idxs in subset_index_urls]
    print(f'\nStart crawling url\'s\n\n'
          f'Number of urls : {num_urls}\n'
          f'Number of threds : {thred}\n'
          f'Maximum urls to crawl (per url) : {crawlers[0].MAX_URLS}\n'
          f'Maximum open links for each url : {crawlers[0].max_length}\n'
          f'Maximum time for all url\'s : {string_time(timeout_val)}\n')

    start_time = time.time()
    make_threds(crwlers_threds)
    end_time = time.time()

    all_datas, all_crawls_dict = get_datas(crawlers)
    print(f'\ntotal time : {string_time(end_time - start_time)}'
          f'\ntotal {data_name}s found : {len(all_datas)}\n')
    # pprint(crawlers[0].All_viseted_URLS_2)
    return crawlers, all_crawls_dict, all_datas


def string_time(T):
    T = int(T)
    text_s = f'{T % 60}s '
    text_m = f'{(T // 60) % 60}m ' if (T // 60) % 60 else ''
    text_h = f'{(T // (60 * 60)) % 24}h ' if (T // (60 * 60)) % 24 else ''
    text_d = f'{(T // (60 * 60 * 24)) % 7}h ' if (T // (60 * 60 * 24)) % 7 else ''
    text_w = f'{T // (60 * 60 * 24 * 7)}h ' if T // (60 * 60 * 24 * 7) else ''
    return text_h + text_m + text_s + text_d + text_w


def print_results(data, with_text=True):
    text = ['\nAll visited urls :\n',
            '\nAll crawls urls :\n',
            f'\nAll {data_name} :\n',
            '\nMost importent urls :\n',
            '\nMost importent urls per domain :\n']
    for i, dat in enumerate(data):
        if with_text:
            print(text[i])
        pprint(dat)
        print('\n')


def cacl_the_best(crws, k=5):
    most_imported_urls = defaultdict(lambda: 0)
    most_imported_urls_per_domain = defaultdict(lambda: defaultdict(lambda: 0))
    pattern = re.compile(data_regex)
    for crw in crws:
        for (v_1, v_2) in crw.knowlage_graph.edges():
            claim_1, claim_2 = int(bool(pattern.match(v_1))), int(bool(pattern.match(v_2)))
            if (claim_1 + claim_2) % 2 == 0:
                continue
            if claim_1 and not claim_2:
                domain = domain_from(v_2)
                most_imported_urls[v_2] += 1
                most_imported_urls_per_domain[domain][v_2] += 1
            if claim_2 and not claim_1:
                domain = domain_from(v_1)
                most_imported_urls[v_1] += 1
                most_imported_urls_per_domain[domain][v_1] += 1

    most_imported_urls = sorted(most_imported_urls.items(), key=lambda item: -item[1])[:k]
    for key, val in most_imported_urls_per_domain.items():
        most_imported_urls_per_domain[key] = sorted(val.items(), key=lambda item: -item[1])[:k]
    return most_imported_urls, dict(most_imported_urls_per_domain)