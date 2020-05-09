from urllib.parse import urlparse
from unittest import TestCase, main
from unittest.mock import patch

from app import (
    url_doi_isbn_scr, TLDLESS_NETLOC_RESOLVER, google_com_scr, googlebooks_scr,
    noormags_scr, noorlib_scr, encrypted_google_scr
)


def fake_resolver(*_):
    raise NotImplementedError


def assert_and_patch_resolver(url, resolver):
    d = TLDLESS_NETLOC_RESOLVER.__self__
    netloc = urlparse('http://' + url).netloc
    if netloc[:4] == 'www.':
        netloc = netloc[4:]
    tldless_netloc = netloc.rpartition('.')[0]
    assert d[tldless_netloc] == resolver
    return patch.dict(d, {tldless_netloc: fake_resolver})


class TestURLHandler(TestCase):

    def assert_scr(self, url, resolver):
        with assert_and_patch_resolver(url, resolver):
            self.assertRaises(
                NotImplementedError, url_doi_isbn_scr, url, '%Y-%m-%d')

    def assert_google_books_scr(self, url, resolver=googlebooks_scr):
        self.assert_scr(url, resolver)

    def test_google_books_netloc(self):
        ag = self.assert_google_books_scr
        # note that top level domains are ignored
        ag('encrypted.google.com/books?id=6upvonUt0O8C', encrypted_google_scr)
        ag('books.google.com/books?id=pzmt3pcBuGYC')
        ag('books.google.de/books?id=pzmt3pcBuGYC')
        ag('books.google.com.ar/books?id=pzmt3pcBuGYC')
        ag('books.google.co.il/books?id=pzmt3pcBuGYC')

    def assert_noormags_scr(self, url):
        self.assert_scr(url, noormags_scr)

    def test_noormags(self):
        an = self.assert_noormags_scr
        an('www.noormags.ir/view/fa/articlepage/105489/')
        an('www.noormags.net/view/fa/articlepage/105489/')
        an('noormags.ir/view/fa/articlepage/105489/')

    def assert_noorlib_scr(self, url):
        self.assert_scr(url, noorlib_scr)

    def test_noorlib(self):
        an = self.assert_noorlib_scr
        an('www.noorlib.ir/View/fa/Book/BookView/Image/6120')
        an('www.noorlib.net/View/fa/Book/BookView/Image/6120')
        an('noorlib.ir/View/fa/Book/BookView/Image/6120')


if __name__ == '__main__':
    main()
