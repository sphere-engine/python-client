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
            self.assertEquals(1, ret['compiler']['id'], 'Submission compiler')

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

