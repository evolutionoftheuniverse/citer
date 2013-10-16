#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

def parse(ris_text):
    '''Parses RIS_text data and returns a dictionary of information'''
    d = {}
    #type: (book, journal, . . . )
    m = re.match('TY  - (.*)', ris_text)
    if m:
        d['type'] = m.group(1).strip()
    #author:
    m = re.findall('(:?AU|A\d)  - (.*)', ris_text)
    #d['authors'] should not be created unless there are some authors
    if m:
        d['authors'] = []
        for author in m:
            d['authors'].append(author[1])
        #author parameter needs to be parsed itself:
        d['lastnames'] = []
        d['firstnames'] = []
        for author in d['authors']:
            if ',' in author:
                lastname, firstname = author.split(',')
            else:
                lastname, firstname = author, ''
            d['lastnames'].append(lastname.strip())
            d['firstnames'].append(firstname.strip())
            
    m = re.search('T1  - (.*)', ris_text)
    if m:
        d['title'] = m.group(1).strip()
    m = re.search('PB  - (.*)', ris_text)
    if m:
        d['publisher'] = m.group(1).strip()
    m = re.search('JF  - (.*)', ris_text)
    if m:
        d['journal'] = m.group(1).strip()
    m = re.search('IS  - (.*)', ris_text)
    if m:
        d['number'] = m.group(1).strip()
    m = re.search('Y1  - (\d*)', ris_text)
    if m:
        d['year'] = m.group(1).strip()
    m = re.search('SN  - (.*)', ris_text)
    if m:
        d['isbn'] = m.group(1).strip()
    m = re.search('SP  - (.*)', ris_text)
    if m:
        d['startpage'] = m.group(1).strip()
        d['pages'] = d['startpage']
    m = re.search('EP  - (.*)', ris_text)
    if m:
        d['endpage'] = m.group(1).strip()
        d['pages'] = d['startpage'] + '–' + d['endpage']
    m = re.search('UR  - (.*)', ris_text)
    if m:
        #in IRS, url can be seprated using a ";"
        d['url'] = m.group(1).split(';')[0].strip()
    m = re.search('LA  - (.*)', ris_text)
    if m:
        d['language'] =  m.group(1).strip()
    return d