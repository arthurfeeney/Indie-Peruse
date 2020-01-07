'''
module contains BandcampPageScraper that is used to scrap album data from a
singe bandcamp. The data it scraps includes links to other albums.
'''

from collections import deque
import re
import hjson


class BandcampPageScraper():
    """
    scrapes data from a single album page
    """

    def __init__(self, html=None):
        self.html = html

    def set_html(self, html):
        """
        reassigns the html
        """
        self.html = html

    def scrape_page(self):
        """
        scrape data from a bandcamp page and put it in a dictionary.
        """
        album_title, author = self.__album_title_and_author()
        album_data = self.__page_album_data()
        recommended_song_downloads = self.__page_audiodata()
        recommended_album_urls = self.__page_recommended_album()
        return {
            'album': album_title,
            'author': author,
            'album_data': album_data,
            'recommended_songs': recommended_song_downloads,
            'recommended_albums': recommended_album_urls
        }

    def __album_title_and_author(self):
        """
        retrieves the album title and author from the html title.
        """
        start_idx = self.html.find('<title>') + len('<title>')
        end_idx = self.html.find('<', start_idx + 1)
        title, author = self.html[start_idx:end_idx].split(' | ')
        return title, author

    def __album_description(self):
        """
        parses string of the album description
        """
        tag = 'name="Description" content="'
        start_idx = self.html.find(tag) + len(tag)
        end_idx = self.html.find('"', start_idx + 1)
        return self.html[start_idx:end_idx]

    def __album_page_urls(self):
        """
        retrieves urls to other album pages.
        """
        audiourl_tag = '"go-to-album album-link" href='
        return self.__scrape_data(audiourl_tag, '"')

    def __page_album_data(self):
        """
        retrieves relevant pieces of album data dict.
        """
        album_data_dict = self.__page_album_data_dict()
        album_data = {}
        if 'current' not in album_data_dict:
            # if 'current' is not in the dict, then something went wrong
            # in this case, it should just skip it without terminating.
            return None
        album_data['title'] = album_data_dict['current']['title']
        album_data['album_id'] = album_data_dict['current']['id']
        album_data['artist'] = album_data_dict['current']['artist']
        album_data['artist_id'] = album_data_dict['current']['band_id']
        album_data['price'] = album_data_dict['current']['minimum_price']
        album_data['release_date'] = album_data_dict['album_release_date']
        track_info = album_data_dict['trackinfo']
        album_data['songs'] = [(s['title'], s['file'], s['track_id'])
                               for s in track_info]
        return album_data

    def __page_album_data_dict(self):
        """
        parse song and album info.
        Looks for relevant info in TralbumData JSON.
        """
        tag = 'TralbumData = '
        album_data_start = self.html.find(tag) + len(tag)
        album_data_end = self.__find_closing_brace(album_data_start)
        album_data_string = self.html[album_data_start:album_data_end]
        # remove warning comments at top
        ads_l = [a for a in album_data_string.split('\n') if '// ' not in a]
        clean_data_string = '\n'.join(ads_l)
        # concatenate urls to form absolute url.
        clean_data_string = re.sub(r'\"(.+?)\" \+ \"(.+?)\"', r'"\1\2"',
                                   clean_data_string)
        album_data_dict = hjson.loads(clean_data_string)
        return album_data_dict

    def __find_closing_brace(self, start_idx):
        """
        Finds the closing brace wrapping around the json album data.
        The deque is used as a queue.
            - If it finds a left brace, it adds it to the queue.
            - If it finds a right brace, it removes a brace from the queue.
            - Every brace has an associated opening/closing brace, so once the queue is empty,
                we know it has found the closing brace.
        """
        if self.html[start_idx] != '{':
            return None
        queue = deque()
        for idx in range(start_idx, len(self.html)):
            if self.html[idx] == '}':
                queue.popleft()
            elif self.html[idx] == '{':
                queue.append(self.html[idx])
            if not queue:
                return idx + 1
        return None

    def __page_audiodata(self):
        """
        parse all audiodata urls from a single page.
        These should be 'recommended' songs
        """
        audiourl_tag = 'data-audiourl="{'
        return self.__scrape_data(audiourl_tag, '}')

    def __page_recommended_album(self):
        album_url_tag = 'class="title-and-artist album-link" href='
        return self.__scrape_data(album_url_tag, '"')

    def __scrape_data(self, tag, end_tag):
        """
        scraps urls (and only urls!) contained between some tag and end_tag.
        """
        clean_urls = []
        starting_idx = 0
        while starting_idx < len(self.html):
            clean_url, starting_idx = self.__audiourl(starting_idx, tag,
                                                      end_tag)
            if clean_url:
                clean_urls.append(clean_url)
        return clean_urls

    def __audiourl(self, starting_idx, audiourl_tag, end_tag):
        """
        Finds the first audiourl in html that occurs after starting_idx.
        """
        audiourl_tag_idx = self.html.find(audiourl_tag, starting_idx)
        if audiourl_tag_idx == -1:
            return None, len(self.html)
        audiourl_front = audiourl_tag_idx + len(audiourl_tag)
        audiourl_back = self.html.find(end_tag, audiourl_front + 1)
        dirty_url = self.html[audiourl_front:audiourl_back]
        clean_url = dirty_url[dirty_url.find('http'):]
        return clean_url, audiourl_back
