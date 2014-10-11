#! /usr/bin/env/ python3

from pyscape.util.clean import *
import unittest
import sys

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_http_strip(self):
        # make sure the shuffled sequence does not lose any elements
        test_url = "http://www.example.com/"
        expected_url = "www.example.com/"
        self.assertEqual(clean_url(test_url), expected_url)

if __name__ == '__main__':
    sys.exit(unittest.main())