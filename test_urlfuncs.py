# -*- coding: utf-8 -*-
""" Urlfuncs Library Test Module

:author: Anton Gorunov
"""

import unittest
import urlfuncs


class TestUrlfuncs(unittest.TestCase):
    """ Test Cases for urlfuncs.py library
    """

    def test_get_domain_zone(self):
        f = urlfuncs.get_domain_zone
        self.assertEqual(f('google.ca'), 'ca')
        self.assertEqual(f('www.google.org'), 'org')
        self.assertEqual(f('rada.gov.ua/'), 'gov.ua')
        self.assertEqual(f('http://www.google.com.ua/'), 'com.ua')
        self.assertEqual(f('http://www.google.co.uk/'), 'co.uk')
        self.assertEqual(f('https://www.atape.net/testpage'), 'net')
        self.assertEqual(f('ftp://www.sftp.org/'), 'org')
        self.assertEqual(f('http://привет.рф'), u'рф')
        self.assertEqual(f(u'http://привет.рф'), u'рф')
        self.assertEqual(f(u'http://test.museum/'), u'museum')

    def test_get_root_domain_zone(self):
        f = urlfuncs.get_root_domain_zone
        self.assertEqual(f('google.ca'), 'ca')
        self.assertEqual(f('www.google.org'), 'org')
        self.assertEqual(f('rada.gov.ua/testpage'), 'ua')
        self.assertEqual(f('http://www.google.com.ua/'), 'ua')
        self.assertEqual(f('http://www.google.co.uk/'), 'uk')
        self.assertEqual(f('https://www.atape.net/testpage'), 'net')
        self.assertEqual(f('ftp://www.sftp.org/'), 'org')
        self.assertEqual(f('http://привет.рф'), 'рф')
        self.assertEqual(f(u'http://привет.рф'), u'рф')
        self.assertEqual(f(u'http://test.museum/'), u'museum')

    def test_toggle_url_www(self):
        f = urlfuncs.toggle_url_www
        self.assertEqual(f('http://atape.net/'), 'http://www.atape.net/')
        self.assertEqual(f('http://www.atape.net/'), 'http://atape.net/')

        self.assertEqual(f('atape.net'), 'www.atape.net')
        self.assertEqual(f('www.atape.net'), 'atape.net')

        self.assertEqual(f('atape.net/page'), 'www.atape.net/page')
        self.assertEqual(f('www.atape.net/page'), 'atape.net/page')

        self.assertEqual(f('https://привет22.рф'), 'https://www.привет22.рф')
        self.assertEqual(f('https://www.при-вет.рф'), 'https://при-вет.рф')

        self.assertEqual(f('hell.com/hell.com'), 'www.hell.com/hell.com')

    def test_toggle_last_url_slash(self):
        f = urlfuncs.toggle_last_url_slash
        # Test regular URLS
        self.assertEqual(f('http://test.com/page'), 'http://test.com/page/')
        self.assertEqual(f('http://test.com/page/'), 'http://test.com/page')

        # Test encoded/quoted white-spaced URL without protocol
        self.assertEqual(f('test.com%2Ftest%2F ', True), 'test.com%2Ftest')
        self.assertEqual(f('test.com%2Ftest ', True), 'test.com%2Ftest%2F')

    def test_is_string_url(self):
        f = urlfuncs.is_string_url
        # Is not URL
        self.assertEqual(f(''), False)
        self.assertEqual(f('i.ua/'), False)
        self.assertEqual(f('test.com/test/test'), False)
        self.assertEqual(f('chrome://hello.com/'), False)
        self.assertEqual(f('http://a.a.a/'), False)
        self.assertEqual(f('http://a. a.a/'), False)
        # Is URL
        self.assertEqual(f('http://localhost'), True)
        self.assertEqual(f('http://localhost////'), True)
        self.assertEqual(f('http://ru.ru'), True)
        self.assertEqual(f('https://ru.ru/section/?p=1'), True)
        self.assertEqual(f(u'ftp://ru.ru'), True)
        self.assertEqual(f(u'http://привет.рф/'), True)
        self.assertEqual(f('http://привет.рф/'), True)
        self.assertEqual(f('http://50.22.113.176/a/b/c/'), True)
        self.assertEqual(f('http://политгазета.рф/item/1633-с-высоты/'), True)

    def test_is_string_domain(self):
        f = urlfuncs.is_string_domain
        # Is not domain
        self.assertEqual(f('hello-world.aero  '), False)
        self.assertEqual(f('http://google098.co.uk'), False)
        self.assertEqual(f(' dOMain.com  '), False)
        self.assertEqual(f('__asd.com'), False)
        self.assertEqual(f('gooooooogle. gtrtrtg wertgwerg'), False)
        self.assertEqual(f('gooooogle.45'), False)
        self.assertEqual(f('gooooogle.com/'), False)
        self.assertEqual(f('gooooogle.i'), False)
        self.assertEqual(f('127.0.0.1'), False)
        # Is domain
        self.assertEqual(f('localhost'), True)
        self.assertEqual(f('google098.co.uk'), True)
        self.assertEqual(f('www.en.hello.world.co.uk'), True)
        self.assertEqual(f('привет.рф'), True)
        self.assertEqual(f(u'стенгазета.рф'), True)
        self.assertEqual(f('a-b-c.museum'), True)

    def test_is_string_ipv4(self):
        f = urlfuncs.is_string_ipv4
        self.assertEqual(f('255.0.12.123'), True)
        self.assertEqual(f('0.0.0.0'), True)
        self.assertEqual(f('1.0.0.255'), True)

        self.assertEqual(f('1.123.12.-'), False)
        self.assertEqual(f('2333.123.12.1'), False)
        self.assertEqual(f('233.a.12.1'), False)
        self.assertEqual(f(''), False)
        self.assertEqual(f('helloipv4'), False)

    def test_split_url(self):
        f = urlfuncs.split_url
        self.assertEqual(
            f('http://domain.zone/section?p=2'),
            ('domain.zone', '/section?p=2'))
        self.assertEqual(
            f('https://www.test.com/hello?t=5&r=6#anchor', False),
            ('www.test.com', '/hello?t=5&r=6#anchor'))
        self.assertEqual(
            f('ftp://www.стенгазета.рф/test/'),
            ('стенгазета.рф', '/test/'))
        self.assertEqual(
            f(u'ftp://www.стенгазета.рф/test/'),
            ('стенгазета.рф', '/test/'))

        # Raises all invalid urls from `test_is_string_url` method
        with self.assertRaises(ValueError):
            f('')
        with self.assertRaises(ValueError):
            f('i.ua/')
        with self.assertRaises(ValueError):
            f('http://test .com/test/test')

    def test_is_url_domain(self):
        f = urlfuncs.is_url_domain
        # Is not url or domain
        self.assertEqual(f('aer ewr wtgw 4r g'), False)
        self.assertEqual(f('chrome://google.com/'), False)
        self.assertEqual(f('http://'), False)
        self.assertEqual(f(''), False)
        self.assertEqual(f('http://__asd__ads.com/'), False)
        self.assertEqual(f(u'http://привет.рф?t=5'), False)
        # Is valid URL and domain
        self.assertEqual(f('http://i.ua/'), True)
        self.assertEqual(f('https://www.hello-world.co.uk/'), True)
        self.assertEqual(f('http://привет.рф/'), True)
        self.assertEqual(f(u'http://привет.рф'), True)

    def test_make_absolute_url(self):
        f = urlfuncs.make_absolute_url
        self.assertEqual(
            f('file2.html', 'http://domain.com/part/file1.html'),
            'http://domain.com/part/file2.html')
        self.assertEqual(
            f('../../test.html', 'http://d.com/a/b/test.html'),
            'http://d.com/test.html')
        self.assertEqual(
            f('../../a', 'http://d.com/a/b/c'),
            'http://d.com/a')
        self.assertEqual(
            f('../b', 'http://d.com/a/b/c'),
            'http://d.com/a/b')

        # Raises all invalid urls from `test_is_string_url` method
        with self.assertRaises(ValueError):
            f('test.html', '')
        with self.assertRaises(ValueError):
            f('test.html', 'i.ua/')
        with self.assertRaises(ValueError):
            f('test.html', 'http://test .com/test/test')

    def test_get_url_domain(self):
        f = urlfuncs.get_url_domain
        self.assertEqual(f('http://test.com'), 'test.com')
        self.assertEqual(f('https://www.a.cc'), 'www.a.cc')
        self.assertEqual(f('ftp://привет.рф/сегодня/?p=1'), 'привет.рф')
        self.assertEqual(f(u'ftp://привет.рф/сегодня/?p=1'), 'привет.рф')

        # Raises all invalid urls from `test_is_string_url` method
        with self.assertRaises(ValueError):
            f('chrome://hello.com/')
        with self.assertRaises(ValueError):
            f('http://a.a.a/')
        with self.assertRaises(ValueError):
            f('http://a. a.a/')

    def test_is_link_internal(self):
        f = urlfuncs.is_link_internal
        # Is internal
        self.assertTrue(f('ya.ru', 'http://ya.ru/section/'))
        self.assertTrue(f('i.ua', 'http://ya.ru/section/'))
        self.assertTrue(f('ya.ru', 'http://i.ua/section/?p1=3&p2=1'))
        self.assertTrue(f('/ya.ru', 'http://ya.ru/section/'))
        self.assertTrue(f('../i.ua', 'http://ya.ru/section/'))
        self.assertTrue(f('', 'http://i.ua/section/?p1=3&p2=1'))
        self.assertTrue(f('http://ya.ru', 'http://ya.ru/section/'))
        self.assertTrue(f('https://ya.ru/', 'http://ya.ru/section/?p1=3&p2=1'))
        # External
        self.assertFalse(f('http://i.ua', 'http://ya.ru/section/'))

    def test_clear_http_and_last_slash(self):
        f = urlfuncs.clear_http_and_last_slash
        self.assertEqual(f('  https://www.test.eu'), '  www.test.eu')
        self.assertEqual(f('http://привет.рф/'), 'привет.рф')
        self.assertEqual(f('http://привет.рф/test/'), 'привет.рф/test')

    def test_full_clean_url(self):
        f = urlfuncs.full_clean_url
        self.assertEqual(f('   http://ya.ru/  '), 'ya.ru')
        self.assertEqual(f('   http://www.привет.рф/'), 'привет.рф')
        self.assertEqual(f('atape.net/'), 'atape.net')
        self.assertEqual(f('www.atape.net/'), 'atape.net')
        self.assertEqual(f('www.atape.net/test/'), 'atape.net/test')

    def test_remove_www(self):
        f = urlfuncs.remove_www
        self.assertEqual(f('http://www.ya.ru'), 'http://ya.ru')
        self.assertEqual(f('http://www.ya.ru/test'), 'http://ya.ru/test')
        self.assertEqual(f('www.привет.рф'), 'привет.рф')
        self.assertEqual(f('www.test.www.hello.com'), 'test.www.hello.com')

    def test_remove_last_slash(self):
        f = urlfuncs.remove_last_slash
        self.assertEqual(f('http://www.test.com////'), 'http://www.test.com')
        self.assertEqual(f('www.i.ua/'), 'www.i.ua')
        self.assertEqual(f('  a.com/test/'), '  a.com/test')
        self.assertEqual(f('  a.com/test'), '  a.com/test')

    def test_remove_http(self):
        f = urlfuncs.remove_http
        self.assertEqual(f('ya.ru  '), 'ya.ru  ')
        self.assertEqual(f('https://www.ya.ru/test'), 'www.ya.ru/test')
        self.assertEqual(f('  http://www.ya.ru'), '  www.ya.ru')
        self.assertEqual(f(' https://привет.рф/test'), ' привет.рф/test')

    def test_urlencode_string(self):
        f = urlfuncs.urlencode_string
        self.assertEqual(f(u"http://привет.рф"),
            "http%3A%2F%2F%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82.%D1%80%D1%84")
        self.assertEqual(f("http://привет.рф"),
            "http%3A//%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82.%D1%80%D1%84")
        self.assertEqual(f("hello world"), "hello%20world")

    def test_is_url_or_domain_valid(self):
        f = urlfuncs.is_url_or_domain_valid
        self.assertTrue(f("http://www.google.com"))
        self.assertTrue(f("www.google.co.uk"))
        self.assertTrue(f("a.ru"))
        self.assertTrue(f("привет.рф"))
        self.assertTrue(f(u"привет.рф"))

        self.assertFalse(f(""))
        self.assertFalse(f(" spaced text"))
        self.assertFalse(f("word"))
        self.assertFalse(f("a.a.a.a.a.a.a.a.a.a.a.aa..a"))

    def test_decode_url(self):
        f = urlfuncs.decode_url
        self.assertEqual(f("http://привет.рф/hello"),
            u"http://xn--b1agh1afp.xn--p1ai/hello")
        # Proof that we can work gently with IDNA encoding
        self.assertEqual(f("http://алло.укр/алло-тест"),
            u"http://xn--80awam.xn--j1amh/алло-тест")
        self.assertEqual(f("http://hello-world.com/page"),
            "http://hello-world.com/page")

    def decode_string(self):
        f = urlfuncs.decode_string
        # Decode strings from any encoding in fast way
        self.assertEqual(f("hello"), u"hello")
        self.assertEqual(f(u"привет"), u"привет")
        self.assertEqual(f(u"test".encode('cp1251')), u"test")
        self.assertEqual(f(u"кои8р".encode('koi8-r')), u"кои8р")

    def test_parse_url_list(self):
        f = urlfuncs.parse_url_list
        urls_text = ' http://test.com/some-page/ \n\n https://test2.com?q=     \r\n'
        urls_list = ['http://test.com/some-page/', 'https://test2.com?q=']
        self.assertEqual(f(urls_text), urls_list)

        not_valid_urls_text = ' not-valid-url \n\n https://test2.com?q=     \r\n'
        with self.assertRaises(ValueError):
            f(not_valid_urls_text)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
