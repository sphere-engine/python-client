import os
import sys
import nose
import unittest
from array import array
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

if os.environ.get('SE_ENDPOINT_COMPILERS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_COMPILERS', None) != None:

    class TestCompilers(unittest.TestCase):

        client = None

        def setUp(self):
            self.client = CompilersClientV3(os.environ['SE_ACCESS_TOKEN_COMPILERS'], os.environ['SE_ENDPOINT_COMPILERS'])

        def test_autorization_fail(self):
            self.client = CompilersClientV3('wrong-access-token', os.environ['SE_ENDPOINT_COMPILERS'])
            with self.assertRaises(SphereEngineException):
                self.client.test()

        def test_autorization_success(self):
            self.client.test()

        def test_test_method_success(self):
            ret = self.client.test()
            self.assertTrue('pi' in ret)

        def test_compilers_method_success(self):
            ret = self.client.compilers()
            self.assertEqual('C', ret['11'][0])

        def test_get_submission_method_success(self):
            ret = self.client.submissions.get(2, True)
            self.assertEquals('abc', ret['source'], 'Submission source')
            self.assertEquals(11, ret['compiler']['id'], 'Submission compiler')

        def test_get_submission_method_not_existing(self):
            nonexistingSubmission = 3
            try:
                self.client.submissions.get(nonexistingSubmission)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_get_submission_method_access_denied(self):
            foreignSubmission = 1
            try:
                self.client.submissions.get(foreignSubmission)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 403)
                
        def test_get_submissions_method_success(self):
            response = self.client.submissions.getMulti([1, 2])
            
            self.assertTrue('items' in response)
            self.assertEquals(2, len(response['items']))
            self.assertTrue('id' in response['items'][0])
            self.assertTrue('id' in response['items'][1])
            
        def test_get_submissions_method_nonexisting_submission(self):
            response = self.client.submissions.getMulti([9999999999])
            
            self.assertTrue('items' in response)
            self.assertEquals(0, len(response['items']))
        
        def test_get_submissions_method_valid_param(self):
            
            try:
                self.client.submissions.getMulti(1)
                self.client.submissions.getMulti([1])
                self.client.submissions.getMulti([1, 2])
                self.assertTrue(True)
            except ValueError:
                self.assertTrue(False)
        
        def test_get_submissions_method_invalid_param(self):
            
            try:
                self.client.submissions.getMulti('1')
                self.client.submissions.getMulti((1, 2))
                self.client.submissions.getMulti(array('l', [1, 2]))
                self.assertTrue(False)
            except ValueError:
                self.assertTrue(True)

        def test_get_submission_stream_method_success(self):
            ret = self.client.submissions.getStream(2, 'source')
            self.assertEquals('abc', ret, 'Submission source')

        def test_get_submission_stream_method_not_existing_submission(self):
            nonexistingSubmission = 3
            try:
                self.client.submissions.getStream(nonexistingSubmission, 'output')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_get_submission_stream_method_not_existing_stream(self):
            try:
                self.client.submissions.getStream(2, 'nonexistingstream')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_create_submission_method_success(self):
            submission_source = 'unit test'
            submission_compiler = 11
            submission_input = 'unit test input'
            response = self.client.submissions.create(submission_source, submission_compiler, submission_input)
            submission_id = int(response['id'])

            self.assertTrue(submission_id > 0, 'New submission id should be greater than 0')

            s = self.client.submissions.get(submission_id, True, True)
            self.assertEquals(submission_source, s['source'], 'Submission source')
            self.assertEquals(submission_input, s['input'], 'Submission input')
            self.assertEquals(submission_compiler, s['compiler']['id'], 'Submission compiler ID')

        def test_create_submission_method_wrong_compiler(self):
            wrongCompilerId = 9999

            try:
                self.client.submissions.create('unit_test', wrongCompilerId)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

