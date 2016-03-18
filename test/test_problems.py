import os
import sys
import nose
import unittest
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

if os.environ.get('SE_URL_COMPILERS', None) != None and \
    os.environ.get('SE_URL_PROBLEMS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_COMPILERS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_PROBLEMS', None) != None:
    
    class TestProblems(unittest.TestCase):
    
        def setUp(self):
            self.client = ProblemsClientV3(os.environ['SE_ACCESS_TOKEN_PROBLEMS'], os.environ['SE_URL_PROBLEMS'])
    
        def test_auth_zonk(self):
            
            self.client = ProblemsClientV3('wrong-access-token', os.environ['SE_URL_PROBLEMS'])
            
            with self.assertRaises(SphereEngineException):
                self.client.test()
            
             
    
        def test_auth_ok(self):
            
            ret = self.client.test()


