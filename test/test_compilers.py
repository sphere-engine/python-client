import os
import sys
import nose
import unittest
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

if os.environ.get('SE_ENDPOINT_COMPILERS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_COMPILERS', None) != None:
    
    class TestCompilers(unittest.TestCase):
    
        client = None
    
        def setUp(self):
            self.client = CompilersClientV3(os.environ['SE_ACCESS_TOKEN_COMPILERS'], os.environ['SE_ENDPOINT_COMPILERS'])
    
        def test_auth_zonk(self):
            
            """
            with self.assertRaises(Exception):
                self.client = CompilersClientV3('wrong-access-token', os.environ['SE_ENDPOINT_COMPILERS'])
                self.client.test()
            """
            pass
    
        def test_auth_ok(self):
            
            ret = self.client.test()
            
        def test_compilers(self):
            
            ret = self.client.compilers()
            
        def test_create_submission(self):
            
            try:
                self.client.submissions.create('', None)
                self.assertTrue(False, '#1')
            except:
                self.assertTrue(True, 'empty source code')
            
            try:
                self.client.submissions.create('', 'abc')
                self.assertTrue(False, '#1')
            except:
                self.assertTrue(True, 'empty source code')
                
            try:
                self.client.submissions.create('abc', 'abc')
                self.assertTrue(False, '#1')
            except:
                self.assertTrue(True, 'empty source code')
                
            try:
                self.client.submissions.create('abc', '11')
                self.assertTrue(False, '#1')
            except:
                self.assertTrue(True, 'empty source code')
            
            ret = self.client.submissions.create('abc', 11)
            self.assertIsNotNone(ret, 'empty ret')
            
        def test_get_submission_notfound(self):    
            
            try:
                self.client.submissions.get(-1)
                self.assertTrue(False, 'code not exits!')
            except:
                self.assertTrue(True, 'code found?')
            
        def test_create_submission_sendandget(self):
            
            ret = self.client.submissions.create('abc', 1, '')
            ret = self.client.submissions.get(ret['id'])
            
    

