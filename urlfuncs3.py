# -*- coding: utf-8 -*-
""" URLS handling module.
This module contains useful functions for any url-related jobs.
"""

import re
import urllib.parse
import chardet

POPULAR_ENCODINGS = ('utf-8', 'ascii')

REMOVE_WWW_PATTERN = re.compile('^(http(s)?://)?w{3}\.(.+)')

DJANGO_URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'(?:[\w](?:[\w-]{0,61}[\w])?\.)+(?:[\w]{2,6}\.?|[\w-]{2,}\.?)|'
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE | re.UNICODE)

DOMAIN_REGEX = re.compile(
    r'^(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'(?:[^\W_](?:[^\W_-]{0,61}[^\W_])?\.)+'
        r'(?:[^\W_]{2,6}\.?|[^\W_-]{2,}\.?)|'
    r'localhost)$', re.IGNORECASE | re.UNICODE)

IPV4_REGEX = re.compile(
    r'^[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}$',
    re.UNICODE)


def decode_string(string):
    """ Universal method to decode strings to UNICODE
    """

    if isinstance(string, str):
        return string

    # Set popular encodings list in frequency order
    for encoding in POPULAR_ENCODINGS:
        try:
            unicode_string = string.decode(encoding)
            return unicode_string
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            pass

    # If all decodings from popular list was failed
    # Try to detect encoding with chardet module
    try:
        enc = chardet.detect(string)
        return string.decode(enc['encoding'])
    except:
        pass
    # When all methods failed, just return input value
    return string


def decode_url(url):
    """ Universal function to decode URLS with IDNA
    """
    decoded_string = decode_string(url)
    parsed = urllib.parse.urlparse(decoded_string)
    if parsed.netloc:
        netloc = parsed.netloc
        # Convert domain name via IDNA
        try:
            idna_netloc = netloc.encode("idna").decode()
        except:
            idna_netloc = netloc
        unicode_url = decoded_string.replace(netloc, idna_netloc, 1)
    else:
        unicode_url = decoded_string
    return unicode_url


def is_url_or_domain_valid(url):
    """ Check if URL or DOMAIN is valid

    :param url: URL or Domain string
    :returns: Boolean True or False
    """
    # Create URL validation FAILURE marker
    is_url_invalid = (not is_string_url(url) and
                      not is_string_domain(url))
    if is_url_invalid:
        return False
    return True


def urlencode_string(string):
    """ Encode string as valid url parameter

    :param string: Any string to be encoded
    :returns: urlencoded ascii string
    """
    return urllib.parse.quote(string.encode('utf-8'), '')


def remove_http(url):
    """ Remove first occurrence of http:// or https:// from url string

    :param url: Something like URL
    :returns: url without http(s)://
    """
    url = url.replace('https://', '', 1)
    url = url.replace('http://', '', 1)
    return url


def remove_last_slash(string):
    """ Remove last slashed from string or URL

    :param string: URL or any string
    :returns: string without slashes at the end
    """
    while True:
        if string[-1:] != '/':
            break
        string = string[:-1]
    return string


def remove_www(url):
    """ Remove www from URL

    :param url: Something like URL
    :returns: URL without www
    """
    try:
        url = ''.join(REMOVE_WWW_PATTERN.findall(url)[0])
    except IndexError:
        pass
    return url


def full_clean_url(url):
    """ Clear URL from white spaces, protocol, www, last slashes

    :param url: Something like URL
    :returns: Dramatically cleared URL
    """
    url = url.strip()
    url = remove_http(url)
    url = remove_last_slash(url)
    url = remove_www(url)
    return url


def clear_http_and_last_slash(string):
    """ Remove protocol and last slash from URL

    :param string: Something like URL
    :returns: Cleared URL
    """
    url = string
    url = remove_http(url)
    url = remove_last_slash(url)
    return url


def is_link_internal(link, domain):
    """ Check is link internal for domain

    :param link: URL/URI found on page of domain
    :param domain: Regular domain name
    :returns: Boolean True or False
    """
    relativity = True
    url = link.strip()
    if is_string_url(url):
        try:
            clean_url = full_clean_url(url)
            if is_string_url(domain):
                domain = get_url_domain(domain)
            clean_domain = full_clean_url(domain)

            pos = clean_url.index(clean_domain)
            if pos != 0:
                relativity = False

        except ValueError:
            relativity = False
    return relativity


def get_url_domain(url):
    """ Get domain from URL

    :param url: Regular valid URL
    :returns: domain or raises ValueError
    """
    if not is_string_url(url):
        raise ValueError("Not valid URL: %s" % url)
    domain =  urllib.parse.urlparse(url).netloc
    return domain


def make_absolute_url(relative, baseurl):
    """ Makes ABS URL from current URL/URI and base URL

    :param relative: Current relative URI or URL
    :param baseurl: Base parent absolute URL
    :returns: Absolute URL or raises ValueError
    """
    if not is_string_url(baseurl):
        raise ValueError('Not valid URL %s' % baseurl)
    absolute_url = urllib.parse.urljoin(baseurl, relative)
    return absolute_url


def is_url_domain(url):
    """ Checks is URL domain

    :param url: Regular URL
    :returns: Boolean True or False
    """
    if not is_string_url(url):
        return False

    parsed_url = urllib.parse.urlparse(url)
    if not is_string_domain(parsed_url.netloc):
        return False

    is_domain_path_valid = (parsed_url.path == '' or parsed_url.path == '/')
    if is_domain_path_valid and not parsed_url.query:
        return True
    return False


def split_url(url, clean_domain=True):
    """ Split URL to domain and URI path

    :param url: Regular URL
    :param clean_domain: Bool flag to clean www in domain
    :returns: (domain, uri) tuple or raises ValueError
    """
    if not is_string_url(url):
        raise ValueError('Can not split invalid URL: %s' % url)

    domain = get_url_domain(url)
    if clean_domain:
        domain = remove_www(domain)
    uri = url.split(domain)[-1]
    splitted_url = (domain, uri)
    return splitted_url


def is_string_ipv4(string):
    """ Check is string valid IPV4

    :param string: IPV4 string
    :returns: Boolean True or False
    """
    if not IPV4_REGEX.search(string):
        return False
    return True


def is_string_domain(string):
    """ Check is string valid domain

    :param string: Domain string
    :returns: Boolean True or False
    """
    decoded_string = decode_string(string)

    try:
        # If last domain part is integer - it is not domain
        int(decoded_string.split('.')[-1])
        return False
    except ValueError:
        pass

    if not DOMAIN_REGEX.search(decoded_string):
        return False
    return True


def is_string_url(url):
    """ Check is string valid URL in formal terms

    :param string: Something to check is it URL
    :returns: boolean True or False
    """
    decoded_url = decode_url(url)
    if not DJANGO_URL_REGEX.search(decoded_url):
        return False
    return True


def toggle_last_url_slash(url, encoded=False):
    """ Toggle last slash in URL

    :param url: Any kind of URL
    :param encoded: Boolean flag of URL presentation
    :returns: URL with toggled last slash
    """
    trimmed_url = url.strip()
    if encoded:
        slash = "%2F"
    else:
        slash = "/"

    if trimmed_url.endswith(slash):
        toggled_url = trimmed_url[:-len(slash)]
    else:
        toggled_url = trimmed_url + slash
    return toggled_url


def toggle_url_www(url):
    """ Toggle www in URL or URI string

    :param url: Any kind of URL or domain string
    :returns: String with toggled www domain
    """
    # Get domain from URL
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc:
        netloc = parsed_url.netloc
    else:
        netloc = parsed_url.path.split('/')[0]

    # Toggle www
    if netloc.lower().startswith('www.'):
        toggled_netloc = netloc[4:]
    else:
        toggled_netloc = 'www.' + netloc
    # Replace first occurrence of domain in original string
    toggled_url = url.replace(netloc, toggled_netloc, 1)
    return toggled_url


def get_root_domain_zone(url):
    """ Get ROOT Domain Zone (last word after last dot)

    :param url: Any kind or URL or domain string
    :returns: Root domain zone
    """
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc:
        netloc = parsed_url.netloc
    else:
        netloc = parsed_url.path.split('/')[0]
    splitted = netloc.split('.')
    root_domain_zone = splitted[-1]
    return root_domain_zone


def get_domain_zone(url):
    """ Not so accurate but efficient way to get domain zone from URL string.

    :param url: Any kind or URL or domain string
    :returns: domain zone string
    """
    # Get domain from string
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc:
        netloc = parsed_url.netloc
    else:
        netloc = parsed_url.path.split('/')[0]

    # Get domain zone from domain
    domain_zone = list()
    splitted = netloc.split('.')
    domain_zone.append(splitted[-1])
    splitted = splitted[:-1]
    for part in reversed(splitted):
        if 1 < len(part) < 4:
            domain_zone.append(part)
        else:
            break
    dz = '.'.join(reversed(domain_zone))
    return dz


def parse_url_list(text):
    """ Parse urls from text. Raises Exception if any of rows is not an url.

    :param text: String text with urls in every line
    :returns: list of urls
    """
    urls = [ url.strip() for url in text.splitlines() if url ]
    for i, url in enumerate(urls):
        if not is_string_url(url):
            raise ValueError('Invalid URL %s on string %s' % (url.encode('utf-8'), i))
            break
    return urls

def parse_domain_list(text):
    """ Parse domains from list. Raises Exception if any of rows is not a domain.

    :param text: String list with domains in every line
    :returns: list of domains
    """
    domains = [ domain.strip() for domain in text.splitlines() if domain ]
    validDomains = []
    for i, domain in enumerate(domains):

        parsed_domain = urllib.parse.urlparse(domain)
        if parsed_domain.netloc:
            domain = parsed_domain.netloc
        elif parsed_domain.path:
            domain = parsed_domain.path.split('/')[0]
        validDomains.append(domain)
        
        if not is_string_domain(domain):
            raise ValueError('Invalid domain %s on string %s' % (domain.encode('utf-8'), i))
            break
    return validDomains


if __name__ == "__main__":
    url = "http://привет.рф/"
    print(urlencode_string(url))
