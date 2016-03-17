import os
import sys
import nose
import unittest
from sphere_engine import ProblemsClientV3

if os.environ.get('SE_URL_COMPILERS', None) != None and \
    os.environ.get('SE_URL_PROBLEMS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_COMPILERS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_PROBLEMS', None) != None:
    
    class TestProblems(unittest.TestCase):
    
        def setUp(self):
            self.client = ProblemsClientV3(os.environ['SE_ACCESS_TOKEN_PROBLEMS'], os.environ['SE_URL_PROBLEMS'])
    
        def test_auth_zonk(self):
            
            self.client = ProblemsClientV3('wrong-access-token', os.environ['SE_ACCESS_TOKEN_PROBLEMS'])
            ret = self.client.test()
            #self.assertRaises(excClass, callableObj)
            self.assertTrue(False, 'Wrong auth')
    
        def test_auth_ok(self):
            
            ret = self.client.test()


