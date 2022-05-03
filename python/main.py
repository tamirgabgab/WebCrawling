import mpld3
import webbrowser
from HypeParameters import saved_html_name, open_html, print_results, path
from Plot_vision import beutiful_plot
from Crawler import set_crawlers
from utils import crawl_urls, read_file, cacl_the_best, print_results


def main():
    urls = read_file(path)
    crawlers = set_crawlers(urls, max_links=4, max_urls=4)
    crawlers, all_crawls_dict, all_emails = crawl_urls(crawlers, thred=4, timeout='120s')
    imported_urls, imported_urls_per_domain = cacl_the_best(crawlers, k=5)
    if print_results:
        print_results([all_crawls_dict, all_emails, imported_urls, imported_urls_per_domain], with_text=True)
    fig = beutiful_plot(crawlers, node_size=100, edge_width=4, circle_size=50, figsize=(20, 30))
    mpld3.save_html(fig, saved_html_name)
    if open_html:
        webbrowser.open(saved_html_name)


if __name__ == "__main__":
    main()