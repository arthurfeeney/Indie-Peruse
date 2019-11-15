from bandcamp.scraper import BandcampPageScraper
from bandcamp.frontier import FIFOFrontier
from bandcamp.crawler import Crawler
from bandcamp.ust import SetUST
from bandcamp.saver import DBSaver
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
    saver = DBSaver(database='indie')
    graph = nx.Graph()
    crawler.crawl_albums(url, 2, graph=graph, saver=saver)

    print('\n * Drawing Graph * \n')
    nx.drawing.nx_pylab.draw(graph, node_size=3, node_color='r', alpha=0.3)
    plt.show()

    diam = nx.algorithms.distance_measures.diameter(graph)
    print(diam)


if __name__ == '__main__':
    main()
