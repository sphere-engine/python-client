# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from array import array
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException
from .test_commons import get_mock_data

class TestCompilers(unittest.TestCase):
    """
    Unit tests for Sphere Engine Compilers module
    """
    client = None

    def setUp(self):
        self.client = CompilersClientV3('access-token', 'endpoint')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_authorization_fail(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/unauthorizedAccess')

        try:
            self.client.test()
            self.fail("Sphere Engine Exception with 401 code expected")
        except SphereEngineException as e:
            self.assertEqual(401, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_not_json_response_fail(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonJsonResponse')

        try:
            self.client.test()
            self.fail("Sphere Engine Exception with 500 code expected")
        except SphereEngineException as e:
            self.assertEqual(500, e.code)
            self.assertEqual('fatal error', str(e))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_invalid_json_response_fail(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/invalidJsonResponse')

        try:
            self.client.test()
            self.fail("Sphere Engine Exception with 502 code expected")
        except SphereEngineException as e:
            self.assertEqual(502, e.code)
            self.assertEqual("{'msg': 'fatal error'}", str(e))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_authorization_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/test')

        self.client.test()
        # there should be no exceptions here

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_test_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/test')

        ret = self.client.test()
        self.assertIn('pi', ret)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_compilers_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/compilers')

        ret = self.client.compilers()
        self.assertEqual('C++', ret['items'][0]['name'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmission/success')

        ret = self.client.submissions.get(2, True)
        self.assertEqual('abc', ret['source'], 'Submission source')
        self.assertEqual(11, ret['compiler']['id'], 'Submission compiler')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_not_existing(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingSubmission')

        nonexisting_submission = 3
        try:
            self.client.submissions.get(nonexisting_submission)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_access_denied(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/deniedAccess')

        foreign_submission = 1
        try:
            self.client.submissions.get(foreign_submission)
            self.fail("Sphere Engine Exception with 403 code expected")
        except SphereEngineException as e:
            self.assertEqual(403, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmission/invalid')

        try:
            self.client.submissions.get(123)
            self.fail("Sphere Engine Exception with 422 code expected")
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmissions/two')

        response = self.client.submissions.getMulti([4, 9])
        self.assertTrue('items' in response)
        self.assertEqual(2, len(response['items']))
        self.assertTrue('id' in response['items'][0])
        self.assertTrue('id' in response['items'][1])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_nonexisting_submission(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmissions/empty')

        response = self.client.submissions.getMulti([9999999999])

        self.assertIn('items', response)
        self.assertEqual(0, len(response['items']))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_valid_param(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmissions/one')
        try:
            self.client.submissions.getMulti(1)
            self.client.submissions.getMulti([1])
            self.client.submissions.getMulti([1, 2])
        except ValueError:
            self.fail("Unexpected Value Error raised")

    def test_get_submissions_method_invalid_param(self):
        try:
            self.client.submissions.getMulti('1')
            self.client.submissions.getMulti((1, 2))
            self.client.submissions.getMulti(array('l', [1, 2]))
            self.fail("Value Error was expected")
        except ValueError:
            pass # we expect this error

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmissions/invalid')

        try:
            self.client.submissions.getMulti([123])
            self.fail("Sphere Engine Exception with 422 code expected")
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_stream_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/getSubmissionStream/source')
        ret = self.client.submissions.getStream(2, 'source')
        self.assertEqual('abc', ret, 'Submission source')

        mock_get.return_value = get_mock_data('compilers/getSubmissionStream/input')
        ret = self.client.submissions.getStream(2, 'input')
        self.assertEqual('input', ret, 'Submission input')

        mock_get.return_value = get_mock_data('compilers/getSubmissionStream/output')
        ret = self.client.submissions.getStream(2, 'output')
        self.assertEqual('output', ret, 'Submission output')

        mock_get.return_value = get_mock_data('compilers/getSubmissionStream/error')
        ret = self.client.submissions.getStream(2, 'error')
        self.assertEqual('error', ret, 'Submission error')

        mock_get.return_value = get_mock_data('compilers/getSubmissionStream/cmpinfo')
        ret = self.client.submissions.getStream(2, 'cmpinfo')
        self.assertEqual('cmpinfo', ret, 'Submission cmpinfo')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_stream_method_not_existing_submission(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingSubmission')

        nonexisting_submission = 3
        try:
            self.client.submissions.getStream(nonexisting_submission, 'output')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    def test_get_submission_stream_method_not_existing_stream(self):
        try:
            self.client.submissions.getStream(2, 'nonexistingstream')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/createSubmission/success')

        submission_source = 'unit test'
        submission_compiler = 11
        submission_input = 'unit test input'
        response = self.client.submissions.create(
            submission_source, submission_compiler, submission_input)
        submission_id = int(response['id'])

        self.assertTrue(submission_id > 0, 'New submission id should be greater than 0')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_wrong_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')

        wrong_compiler = 9999

        try:
            self.client.submissions.create('unit_test', wrong_compiler)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('compilers/createSubmission/invalid')

        try:
            self.client.submissions.create('unit_test', 422)
            self.fail("Sphere Engine Exception with 422 code expected")
        except SphereEngineException as e:
            self.assertEqual(422, e.code)
            