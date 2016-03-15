import os
import sys
import nose
import unittest

if os.environ.get('SE_URL_COMPILERS', None) != None and \
    os.environ.get('SE_URL_PROBLEMS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_COMPILERS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_PROBLEMS', None) != None:
    
    class TestCompilers(unittest.TestCase):
    
        def setUp(self):
            
            self.options = {
                'SE_URL_COMPILERS': os.environ['SE_URL_COMPILERS'],
                'SE_URL_PROBLEMS': os.environ['SE_URL_PROBLEMS'],
                'SE_ACCESS_TOKEN_COMPILERS': os.environ['SE_ACCESS_TOKEN_COMPILERS'],
                'SE_ACCESS_TOKEN_PROBLEMS': os.environ['SE_ACCESS_TOKEN_PROBLEMS'],
            }
    
        def test_upper(self):
            self.assertEqual('foo'.upper(), 'FOO')
    
        def test_isupper(self):
            self.assertTrue('FOO'.isupper())
            self.assertFalse('Foo'.isupper())
    
        def test_split(self):
            s = 'hello world'
            self.assertEqual(s.split(), ['hello', 'world'])
            # check that s.split fails when the separator is not a string
            with self.assertRaises(TypeError):
                s.split(2)


