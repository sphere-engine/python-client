import os
import sys
import nose
import unittest
from array import array
from sphere_engine import CompilersClientV3
from .test_commons import get_mock_data
from sphere_engine.exceptions import SphereEngineException
if (sys.version_info > (3, 3)):
    from unittest.mock import patch
else:
    from mock import patch

class TestCompilers(unittest.TestCase):

    client = None

    def setUp(self):
        self.client = CompilersClientV3('781e6696de8ccfc6a3e04de943ea90fda', 'problems.sphere-engine.com')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_autorization_fail(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/unauthorizedAccess')

        client = CompilersClientV3('wrong-access-token', 'test.mock')
        with self.assertRaises(SphereEngineException):
            client.test()

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_autorization_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/test')

        self.client.test()
        # there should be no exceptions here

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_test_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/test')

        ret = self.client.test()
        self.assertTrue('pi' in ret)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_compilers_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/compilers')

        ret = self.client.compilers()
        self.assertEqual('C++', ret['items'][0]['name'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmission/success')

        ret = self.client.submissions.get(2, True)
        self.assertEquals('abc', ret['source'], 'Submission source')
        self.assertEquals(11, ret['compiler']['id'], 'Submission compiler')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_not_existing(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingSubmission')

        nonexistingSubmission = 3
        try:
            self.client.submissions.get(nonexistingSubmission)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_access_denied(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/deniedAccess')
        foreignSubmission = 1
        try:
            self.client.submissions.get(foreignSubmission)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(403, e.code)
            
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

