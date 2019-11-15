'''
module provides class to crawl bandcamp album pages. 
'''

import certifi
import urllib3
import subprocess


class Crawler:
    '''
    used to crawl bandcamp album pages and scrape data from them. 
    '''

    def __init__(self, scraper, ust, frontier):
        '''
        pass in implementations of scraper, url-seen-test, and frontier. 
        '''
        self.scraper = scraper
        self.ust = ust
        self.frontier = frontier

    def crawl_albums(self, seed_url, n_iter=100, graph=None, saver=None):
        '''
        crawl pages starting from seed_url. 
        graph is just a graph with albums as vertices and edges if 
        an album is recommended on another's page. 
        saver is used to save the current data the has been scraped.
        '''
        self.frontier.add(seed_url)
        self.ust.add(seed_url)
        current_iter = 0
        while not self.frontier.empty() and current_iter < n_iter:
            url = self.frontier.get()
            data = self.__retrieve_data(url)
            data['album_url'] = url
            if saver is not None:
                self.__save_data(saver, data)
            for adj_url in data['recommended_albums']:
                if graph is not None:
                    graph.add_edges_from([(url, adj_url)])
                if not adj_url in self.ust:
                    self.frontier.add(adj_url)
                    self.ust.add(adj_url)
            print(data)
            current_iter += 1

    def __save_data(self, saver, data):
        saver.insert(data['author'], data['album'], data['album_url'],
                     data['album_data']['price'],
                     data['album_data']['release_date'],
                     data['recommended_albums'])

    def __retrieve_data(self, url):
        '''
        given a url, this downloads the HTML and scrapes the interesting
        data from it. 
        '''
        html = self.__retrieve_html(url)
        self.scraper.set_html(html)
        return self.scraper.scrape_page()

    def __retrieve_html(self, url):
        '''
        downloads HTML from url and returns it as a string
        '''
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                   ca_certs=certifi.where())
        req = http.request('GET', url, timeout=2.5)
        html = req.data.decode('utf-8')
        return html
