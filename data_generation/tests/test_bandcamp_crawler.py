import data_generation.bandcamp_crawler as bpc
import networkx as nx
import numpy as np


def test_general_crawl():
    seed_url = 'https://nonameraps.bandcamp.com/album/room-25'
    num_to_crawl = 2
    g, _ = bpc.general_crawl(seed_url, num_to_crawl)
    assert len(g) > 0
    assert len(g[seed_url]) > 0

