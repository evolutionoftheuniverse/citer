#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''All things that are specifically related to Noormags website'''

import re
import urllib2
import cookielib
from urlparse import parse_qs
from urlparse import urlparse

import langid

import bibtex
import reference
import citation

class GoogleBook():
    '''Creates a google book object'''
    
    def __init__(self, googlebook_url):
        self.url = googlebook_url
        self.bibtex = get_bibtex(googlebook_url)
        self.dictionary = bibtex.parse(self.bibtex)
        pu = urlparse(googlebook_url)
        pq = parse_qs(pu.query)
        #default domain is prefered:
        self.dictionary['url'] = 'http://' + pu.netloc +\
                                 '/books?id=' + pq['id'][0]
        #manually adding page nubmer to dictionary:
        if 'pg' in pq:
            self.dictionary['pages'] = pq['pg'][0][2:]
            self.dictionary['url'] += '&pg=' + pq['pg'][0]
        #although google does not provide a language field:
        if 'language' in self.dictionary:
            self.dictionary['language']
            self.error = 0
        else:
            self.dictionary['language'], self.dictionary['error'] =\
                                     detect_language(self.dictionary['title'])
            self.error = round((1 - self.dictionary['error']) * 100, 2)
        self.ref =reference.create(self.dictionary)
        self.cite = citation.create(self.dictionary)


def detect_language(string):
    m = langid.classify(string)
    #langid.identifier.set_languages(['en','de','fr','es','ja','fa'])
    #m = langid.classify(string)
    error = m[1]
    language = m[0]
    return language, error

def get_bibtex(googlebook_url):
    '''Gets bibtex file content from a noormags url'''
    #getting id:
    pu = urlparse(googlebook_url)
    pq = parse_qs(pu.query)
    bookid = pq['id'][0]
    url = 'http://books.google.com/books/download/?id=' +\
      bookid + '&output=bibtex'
    #Agent spoofing is needed, otherwise: HTTP Error 401: Unauthorized
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0)' +
                          ' Gecko/20100101 Firefox/24.0')]
    bibtex = opener.open(url).read()
    return bibtex

def get_irs(googlebook_url):
    '''Gets bibtex file content from a noormags url'''
    #getting id:
    pu = urlparse(googlebook_url)
    pq = parse_qs(pu.query)
    bookid = pq['id'][0]
    url = 'http://books.google.com/books/download/?id=' +\
      bookid + '&output=bibtex'
    #Agent spoofing is needed, otherwise: HTTP Error 401: Unauthorized
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0)' +
                          ' Gecko/20100101 Firefox/24.0')]
    bibtex = opener.open(url).read()
    return bibtex