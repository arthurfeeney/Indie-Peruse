'''
Utility functions for parsing URLSs and such.
'''


def domain_name(absolute_url):
    '''
    takes an absolute url, such as https://youtube.com/hithere
    and returns https://youtube.com
    '''

    https_len = len('https://')
    http_len = https_len - 1

    if 'https://' in absolute_url:
        end = absolute_url.find('/', https_len)
        if end == -1:
            return absolute_url
        return absolute_url[:end]
    elif 'http://' in absolute_url:
        end = absolute_url.find('/', http_len)
        if end == -1:
            return absolute_url
        return absolute_url[:end]
    else:
        return None


def remove_protocol(url):
    '''
    removes the protocol (http or https) from the url
    '''
    if 'https://' in url[:len('https://')]:
        url = url[len('https://'):]
    elif 'http://' in url[:len('http://')]:
        url = url[len('http://'):]
    return url
