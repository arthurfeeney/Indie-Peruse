from scraper import BandcampPageScraper
from frontier import FIFOFrontier
from crawler import Crawler
from ust import SetUST
from saver import DBSaver
import certifi
import urllib3
import subprocess
import matplotlib.pyplot as plt
import networkx as nx


def main():
    #url = 'https://hiraeth-records.bandcamp.com/album/building-a-better-world'
    url = 'https://astrangelyisolatedplace.bandcamp.com/album/apex'
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where())
    r = http.request('GET', url, timeout=2.5)
    html = r.data.decode('utf-8')

    bcps = BandcampPageScraper()
    crawler = Crawler(bcps, SetUST(), FIFOFrontier())
    graph = nx.Graph()
    crawler.crawl_albums(url, 50, graph=graph)

    #remove = [node for node, degree in G.degree() if degree < 2]
    #G.remove_nodes_from(remove)

    print('\n * Drawing Graph * \n')
    nx.drawing.nx_pylab.draw(graph, node_size=3, node_color='r', alpha=0.3)
    plt.show()

    diam = nx.algorithms.distance_measures.diameter(graph)
    print(diam)


def print_dict(d, depth=0):
    '''
    to make printing dict of dict a little prettier
    '''
    if not isinstance(d, dict):
        print(''.join(['   ' for _ in range(depth)]) + str(d))
        return
    for i in d.keys():
        print(''.join(['   ' for _ in range(depth)]) + i + ': ', end='\n')
        print_dict(d[i], depth + 1)
        print()


if __name__ == '__main__':
    main()
