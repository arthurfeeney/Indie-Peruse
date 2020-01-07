
import data_generation.url_util as uu


def test_domain_name():
    input_urls = [
        'https://website.com/stuff/more',
        'http://website.com/stuff/more',
        'htp://website.com/stuff/more'
    ]
    output_urls = [
        'https://website.com',
        'http://website.com',
        None
    ]
    for (i, o) in zip(input_urls, output_urls):
        assert uu.domain_name(i) == o


def test_artist_from_url():
    input_urls = [
        'https://menitrust.bandcamp.com/album/oncle-jazz'
        'http://artist.bandcamp.com'
    ]
    outputs = [
        'menitrust',
        'artist'
    ]
    for (i, o) in zip(input_urls, outputs):
        assert uu.artist_from_url(i) == o


def test_album_name_from_url():
    urls = [
        'https://bandcamp.com/album/albumname?akjdfl',
        'https://bandcamp.com/album/albumname',
        'https://artist.bandcamp.com/album/albumname?',
        'https://artitst.bandcamp.com/someotherstuff/album/albumname?end'
    ]
    for url in urls:
        a = uu.album_name_from_url(url)
        assert a == 'albumname'


def test_valid_assert_url_is_bandcamp():
    valid_urls = [
        'https://bandcamp.com/song',
        'http://bandcamp.com/song',
        'https://oncle-jazz.bandcamp.com/other',
        'https://menitrust.bandcamp.com/album/oncle-jazzi'
        'http://menitrust.bandcamp.com/album/oncle-jazzi'
    ]
    for url in valid_urls:
        assert uu.assert_url_is_bandcamp(url)


def test_invalid_assert_url_is_bandcamp():
    invalid_urls = [
        'https://notbandcamp.com',
        'bandcamp.com/other',
        'https://notbandcamp.com/hithere',
        'http://notbandcamp.com/hi',
        'http:bandcamp.com',
        'http://poop.com/bandcamp',
        'https://hi.bandcamp.artist.com/songstuff'
    ]
    for url in invalid_urls:
        assert not uu.assert_url_is_bandcamp(url)


def test_list_seed_url():
    urls = [
        'https://bandcamp.com/song',
        'http://bandcamp.com/song',
        'https://oncle-jazz.bandcamp.com/other',
        'https://menitrust.bandcamp.com/album/oncle-jazzi'
        'http://menitrust.bandcamp.com/album/oncle-jazzi'
    ]
    # valid urls are good.
    assert uu.assert_url_is_bandcamp(urls)
    invalid_url = 'https://notbandcamp.com'
    # add an invalid url, so it should fail
    urls.append(invalid_url)
    assert not uu.assert_url_is_bandcamp(urls)

