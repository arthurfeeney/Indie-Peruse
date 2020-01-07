from data_generation.scraper import BandcampPageScraper
from data_generation.frontier import FIFOFrontier
from data_generation.crawler import Crawler
from data_generation.ust import SetUST
import data_generation.url_util as uu
import networkx as nx
import numpy as np


def general_crawl(seed_url, num_to_crawl, saver=None):
    """
    crawl bandcamp.com starting from seed_url(s) can be a url string a list of url strings.
    """
    # check that urls are actually to bandcamp

    if not uu.assert_url_is_bandcamp(seed_url):
        print('seed_url contains non-bandcamp site')
        return None, None

    crawler = Crawler(BandcampPageScraper(), SetUST(), FIFOFrontier())
    # graph is updated in-place
    graph = nx.Graph()
    graph, saver = crawler.crawl_albums(seed_url, num_to_crawl, graph=graph, saver=saver)
    return graph, saver


