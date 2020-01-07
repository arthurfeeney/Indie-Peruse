"""
Utility functions for parsing URLSs.
"""
import re

def domain_name(absolute_url):
    """
    takes an absolute url, such as https://youtube.com/hithere
    and returns https://youtube.com
    """

    protocol = https_or_http(absolute_url)
    if protocol is None:
        return None
    else:
        end = absolute_url.find('/', len(protocol))
        if end == -1:
            return absolute_url
        return absolute_url[:end]

def https_or_http(absolute_url):
    if 'https://' in absolute_url:
        return 'https://'
    elif 'http://' in absolute_url:
        return 'http://'
    else:
        return None

def remove_protocol(url):
    """
    Removes the protocol (http or https) from the url
    """
    protocol = https_or_http(url)
    if protocol:
        return url[len(protocol):]
    else:
        # the input url doesn't have protocol
        return url

def artist_from_url(album_url):
    """
    Given a valid bandcamp album url, extract the artist name.
    """
    if not assert_url_is_bandcamp(album_url):
        raise Exception("album_url must be a valid bandcamp url")
    dn = domain_name(album_url)
    rp_dn = remove_protocol(dn)
    return rp_dn.split('.')[0] # artist name occurs before the first "."


def album_name_from_url(album_url):
    """
    Given a valid bandcamp url of an album page, extract the album title
    """
    # this if statement is essentially only useful for testing.
    # tests for other functions that call this one may not be a string with album/ in them.
    if not assert_url_is_bandcamp(album_url):
        raise Exception("album_url must be a valid bandcamp url")
    if 'album/' not in album_url:
        return album_url
    start_idx: int = album_url.index('album/') + len('album/')
    end_idx: int = album_url.index('?') if '?' in album_url else -1  # the last character if it's not included.
    if end_idx == -1:
        return album_url[start_idx:]  # not question mark, so just return everything after "album/"
    else:
        return album_url[start_idx:end_idx]


def assert_url_is_bandcamp(seed_url):
    """
    check if the seed url(s) are actually to bandcamp
    """
    if isinstance(seed_url, str):
        # split on non-alphanumeric characters
        seed_domain_name = domain_name(seed_url)

        # if the url does not have http(s):// then it is invalid
        if seed_domain_name is None:
            return False

        # split the domain name on non-alphanumeric characters
        split_on_non_alphanum = re.split('[^a-zA-Z1-9]', seed_domain_name)

        # bandcamp can only occur as the second to last element of the split for it to be valid
        # ".com" will be the last element
        return 'bandcamp' == split_on_non_alphanum[-2]

    # if seed_url is a list of urls, recursively assert that all are valid
    elif isinstance(seed_url, list):
        return all(assert_url_is_bandcamp(url) for url in seed_url)

    # if the input is not a string or list, it is invalid
    else:
        return False
