from scraper import BandcampPageScraper


def test_init():
    bcps = BandcampPageScraper('html string')
    assert bcps.html == 'html string'


def test_audiourl():
    bcps = BandcampPageScraper('hello <http_song_url> my name is arthur')
    s = bcps._BandcampPageScraper__audiourl(0, '<', '>')
    assert s[0] == 'http_song_url'


def test_scrape_data():
    bcps = BandcampPageScraper('hello <http_song_url1> <http_song_url2>')
    urls = bcps._BandcampPageScraper__scrape_data('<', '>')
    assert urls == ['http_song_url1', 'http_song_url2']

    bcps = BandcampPageScraper('start http words end')
    urls = bcps._BandcampPageScraper__scrape_data('start', 'end')
    assert urls == ['http words ']


def test_find_closing_brace():
    bcps = BandcampPageScraper('{{{}}}')
    end_idx = bcps._BandcampPageScraper__find_closing_brace(0)
    assert bcps.html[:end_idx] == '{{{}}}'

    bcps = BandcampPageScraper('{ax{d{3gd}}hf}asdf')
    end_idx = bcps._BandcampPageScraper__find_closing_brace(0)
    assert bcps.html[:end_idx] == '{ax{d{3gd}}hf}'

    # no closing brace returns None
    bcps = BandcampPageScraper('{{{')
    end_idx = bcps._BandcampPageScraper__find_closing_brace(0)
    assert end_idx == None

    # if the first char isn't a brace it returns None
    bcps = BandcampPageScraper('a{{{')
    end_idx = bcps._BandcampPageScraper__find_closing_brace(0)
    assert end_idx == None
