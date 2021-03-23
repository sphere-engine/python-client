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
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException
from .test_commons import get_mock_dataV4 as get_mock_data

class TestProblems(unittest.TestCase):
    """
    Unit tests for Sphere Engine Problems module
    """
    client = None

    def setUp(self):
        self.client = ProblemsClientV4('access-token', 'endpoint')

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
        mock_get.return_value = get_mock_data('problems/test')

        self.client.test()
        # there should be no exceptions here

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_test_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/test')
        self.assertTrue(len(self.client.test()['message']) > 0,
                        'Test method should return nonempty message')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_compilers_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/compilers')

        self.assertEqual('C++', self.client.compilers()['items'][0]['name'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_problems_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblems/default')

        problems = self.client.problems.all()
        self.assertEqual(10, problems['paging']['limit'])
        self.assertEqual(0, problems['paging']['offset'])
        self.assertNotIn('shortBody', problems['items'][0])
        self.assertIn('lastModified', problems['items'][0])
        self.assertIn('body', problems['items'][0]['lastModified'])
        self.assertIn('settings', problems['items'][0]['lastModified'])

        mock_get.return_value = get_mock_data('problems/getProblems/limit')
        self.assertEqual(11, self.client.problems.all(11)['paging']['limit'])

        mock_get.return_value = get_mock_data('problems/getProblems/default')
        self.assertNotIn('shortBody', self.client.problems.all(short_body=False)['items'][0])

        mock_get.return_value = get_mock_data('problems/getProblems/shortBody')
        self.assertIn('shortBody', self.client.problems.all(short_body=True)['items'][0])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_problems_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblems/invalid')

        try:
            self.client.problems.all()
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblem/success')

        problem = self.client.problems.get('TEST')
        self.assertEqual('TEST', problem['code'])
        self.assertNotIn('shortBody', problem)
        self.assertIn('lastModified', problem)
        self.assertIn('body', problem['lastModified'])
        self.assertIn('settings', problem['lastModified'])

        self.assertNotIn('shortBody', self.client.problems.get('TEST', False))

        mock_get.return_value = get_mock_data('problems/getProblem/shortBody')
        self.assertIn('shortBody', self.client.problems.get('TEST', True))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_wrong_code(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.problems.get('NON_EXISTING_PROBLEM')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblem/invalid')

        try:
            self.client.problems.get('CODE')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createProblem/success')

        problem_code = 'CODE'
        self.assertEqual(problem_code, self.client.problems.create(
            'name', 100, 'body', 2, True, code=problem_code)['code'],
                         'Creation method should return new problem code')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_code_taken(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/problemCodeTaken')
        try:
            self.client.problems.create('Taken problem code', None, code='TEST')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    def test_create_problem_method_code_empty(self):
        try:
            self.client.problems.create('Empty problem code', None, code='')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_code_invalid(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/problemCodeInvalid')

        try:
            self.client.problems.create('Invalid problem code', None, code='!@#$%^')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    def test_create_problem_method_empty_name(self):
        try:
            self.client.problems.create('', None, code='UNIQUE_CODE')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_nonexisting_masterjudge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingMasterjudge')

        nonexisting_masterjudge = 9999
        try:
            self.client.problems.create('Nonempty name', nonexisting_masterjudge, 'body',
                                        0, False, code='UNIQUE_CODE')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createProblem/invalid')

        try:
            self.client.problems.create('name', 1000, 'body', 0, False, code='CODE')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblem/success')

        problem_code = 'CODE'
        self.client.problems.update(problem_code, 'name', 1000, 'body', 2, True)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.problems.update('NON_EXISTING_CODE', 'Nonexisting problem code')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_method_nonexisting_masterjudge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingMasterjudge')

        nonexisting_masterjudge = 9999
        try:
            self.client.problems.update('TEST', 'Nonempty name', nonexisting_masterjudge, 'body',
                                        0, 0)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    def test_update_problem_method_empty_code(self):
        try:
            self.client.problems.update('', 'Nonempty name')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    def test_update_problem_method_empty_name(self):
        try:
            self.client.problems.update('TEST', '')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblem/invalid')

        try:
            self.client.problems.update('CODE', 'name')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_active_testcases_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblem/success')

        self.client.problems.updateActiveTestcases('TEST', [])
        self.client.problems.updateActiveTestcases('TEST', [0])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_testcases_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcases/success')

        self.assertEqual(0, self.client.problems.allTestcases('TEST')['items'][0]['number'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_testcases_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.problems.allTestcases('NON_EXISTING_CODE')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_testcases_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcases/invalid')

        try:
            self.client.problems.allTestcases('TEST')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcase/success')

        self.assertEqual(0, self.client.problems.getTestcase('TEST', 0)['number'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.getTestcase('NON_EXISTING_CODE', 0)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')

        try:
            self.client.problems.getTestcase('TEST', 1)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcase/invalid')

        try:
            self.client.problems.getTestcase('TEST', 422)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_testcase_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createProblemTestcase/success')

        res = self.client.problems.createTestcase('CODE', 'in0', 'out0', 10, 2, 0)
        self.assertEqual(0, res['number'], 'Testcase number')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_testcase_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.problems.createTestcase('NON_EXISTING_CODE', 'in0', 'out0', 10, 2, 1)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_testcase_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')

        nonexisting_judge = 9999
        try:
            self.client.problems.createTestcase('TEST', 'in0', 'out0', 10, nonexisting_judge, 1)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createProblemTestcase/invalid')

        try:
            self.client.problems.createTestcase('TEST', '422', '422', 10, 1, 1)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblemTestcase/success')

        self.client.problems.updateTestcase('CODE', 0, 'in0', 'out0', 10, 2, False)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.problems.updateTestcase('NON_EXISTING_CODE', 0, 'updated input')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')

        try:
            self.client.problems.updateTestcase('TEST', 1, 'updated input')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')

        nonexisting_judge = 9999
        try:
            self.client.problems.updateTestcase('TEST', 0, 'updated input',
                                                'updated output', 1, nonexisting_judge, 0)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblemTestcase/invalid')

        try:
            self.client.problems.updateTestcase('TEST', 0, '422', '422', 10, 1, 1)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/deleteProblemTestcase/success')

        self.client.problems.deleteTestcase('CODE', 1)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.problems.deleteTestcase('NON_EXISTING_CODE', 0)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')

        try:
            self.client.problems.deleteTestcase('TEST', 1)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/deleteProblemTestcase/invalid')

        try:
            self.client.problems.deleteTestcase('TEST', 422)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcaseFile/input')

        self.assertEqual('in0', self.client.problems.getTestcaseFile('CODE', 0, 'input'))

        mock_get.return_value = get_mock_data('problems/getProblemTestcaseFile/output')

        self.assertEqual('out0', self.client.problems.getTestcaseFile('CODE', 0, 'output'))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.problems.getTestcaseFile('NON_EXISTING_CODE', 0, 'input')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')

        try:
            self.client.problems.getTestcaseFile('TEST', 1, 'input')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_nonexisting_file(self, mock_get):
        try:
            self.client.problems.getTestcaseFile('TEST', 0, 'fakefile')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_judges_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudges/default')

        self.assertEqual(10, self.client.judges.all()['paging']['limit'])

        mock_get.return_value = get_mock_data('problems/getJudges/limit')

        self.assertEqual(11, self.client.judges.all(11)['paging']['limit'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_judges_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudges/invalid')

        try:
            self.client.judges.all()
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudge/success')

        self.assertEqual(1, self.client.judges.get(1)['id'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')

        nonexisting_judge = 9999
        try:
            self.client.judges.get(nonexisting_judge)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudge/invalid')

        try:
            self.client.judges.get(422)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_file_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudgeFile/source')
    
        self.assertEqual('source0', self.client.judges.getJudgeFile(1, 'source'))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_file_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')
    
        nonexisting_judge = 9999
        try:
            self.client.judges.getJudgeFile(nonexisting_judge, 'source')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)
            
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_file_method_nonexisting_file(self, mock_get):
        try:
            self.client.judges.getJudgeFile(1, 'fakefile')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_judge_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createJudge/success')

        response = self.client.judges.create('source', 1, 0, 'UT judge')
        judge_id = response['id']
        self.assertTrue(judge_id > 0, 'Creation method should return new judge ID')

    def test_create_judge_method_empty_source(self):
        try:
            self.client.judges.create('', 1, 0, '')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_judge_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')

        nonexisting_compiler = 9999
        try:
            self.client.judges.create('nonempty source', nonexisting_compiler, 0, '')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_judge_method_nonexisting_compiler_version(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompilerVersion')

        nonexisting_compiler_version = 9999
        try:
            self.client.judges.create('nonempty source', 1, 0, '', compiler_version_id=nonexisting_compiler_version)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_judge_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createJudge/invalid')

        try:
            self.client.judges.create('nonempty source', 422, 0, '')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateJudge/success')

        self.client.judges.update(1, 'source', 11, 'name')

    def test_update_judge_method_empty_source(self):
        try:
            self.client.judges.update(1, '', 1, '')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')

        nonexisting_judge = 99999999
        try:
            self.client.judges.update(nonexisting_judge, 'nonempty source', 1, '')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')

        nonexisting_compiler = 9999
        try:
            self.client.judges.update(1, 'nonempty source', nonexisting_compiler, '')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_nonexisting_compiler_version(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompilerVersion')

        nonexisting_compiler_version = 9999
        try:
            self.client.judges.update(1, 'nonempty source', 1, '', compiler_version_id=nonexisting_compiler_version)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_foreign_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/deniedAccess')

        try:
            self.client.judges.update(1, 'nonempty source', 1, '')
            self.fail("Sphere Engine Exception with 403 code expected")
        except SphereEngineException as e:
            self.assertEqual(403, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateJudge/invalid')

        try:
            self.client.judges.update(422, 'nonempty source', 422, '')
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmission/success')

        self.assertEqual(10, self.client.submissions.get(10)['id'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_nonexisting_submission(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingSubmission')

        nonexisting_submission = 9999999999
        try:
            self.client.submissions.get(nonexisting_submission)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmission/invalid')

        try:
            self.client.submissions.get(422)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_file_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissionFile/source')
        self.assertEqual('source0', self.client.submissions.getSubmissionFile(1, 'source'))
        
        mock_get.return_value = get_mock_data('problems/getSubmissionFile/stdout')
        self.assertEqual('stdout0', self.client.submissions.getSubmissionFile(1, 'output'))
        
        mock_get.return_value = get_mock_data('problems/getSubmissionFile/stderr')
        self.assertEqual('stderr0', self.client.submissions.getSubmissionFile(1, 'error'))
        
        mock_get.return_value = get_mock_data('problems/getSubmissionFile/cmperr')
        self.assertEqual('cmperr0', self.client.submissions.getSubmissionFile(1, 'cmpinfo'))
        
        mock_get.return_value = get_mock_data('problems/getSubmissionFile/psinfo')
        self.assertEqual('psinfo0', self.client.submissions.getSubmissionFile(1, 'debug'))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_file_method_nonexisting_submission(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingSubmission')
        
        nonexisting_submission = 9999
        try:
            self.client.submissions.getSubmissionFile(nonexisting_submission, 'source')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)
                
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_file_method_nonexisting_file(self, mock_get):
        try:
            self.client.submissions.getSubmissionFile(1, 'fakefile')
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/two')

        response = self.client.submissions.getMulti([9, 4])
        self.assertIn('items', response)
        self.assertEqual(2, len(response['items']))
        self.assertIn('id', response['items'][0])
        self.assertIn('id', response['items'][1])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_nonexisting_submission(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/empty')

        response = self.client.submissions.getMulti([9999999999])
        self.assertIn('items', response)
        self.assertEqual(0, len(response['items']))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_valid_param(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/one')

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
            self.fail("Value Error expected")
        except ValueError:
            pass

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/invalid')

        try:
            self.client.submissions.getMulti([422])
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createSubmission/success')

        response = self.client.submissions.create('TEST', 'source', 1)
        submission_id = response['id']
        self.assertTrue(submission_id > 0, 'Creation method should return new submission ID')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.submissions.create('NON_EXISTING_CODE', 'nonempty source', 1)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')

        nonexisting_compiler = 9999
        try:
            self.client.submissions.create('TEST', 'nonempty source', nonexisting_compiler)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_nonexisting_compiler_version(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompilerVersion')

        nonexisting_compiler_version = 9999
        try:
            self.client.submissions.create('TEST', 'nonempty source', 1, compiler_version_id=nonexisting_compiler_version)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/invalid')

        try:
            self.client.submissions.create('TEST', 'nonempty source', 422)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)
            
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_multi_files_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createSubmission/success')
    
        files = {
            'file1': 'a',
            'file2': 'b'
        }
        response = self.client.submissions.createMultiFiles('TEST', files, 1)
        submission_id = response['id']
        self.assertTrue(submission_id > 0, 'Creation method should return new submission ID')
    
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_multi_files_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.submissions.createMultiFiles('NON_EXISTING_CODE', {'nonempty source': ''}, 1)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_multi_files_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')

        nonexisting_compiler = 9999
        try:
            self.client.submissions.createMultiFiles('TEST', {'nonempty source': ''}, nonexisting_compiler)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_multi_files_method_nonexisting_compiler_version(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompilerVersion')

        nonexisting_compiler_version = 9999
        try:
            self.client.submissions.createMultiFiles('TEST', {'nonempty source': ''}, 1, compiler_version_id=nonexisting_compiler_version)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_multi_files_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/invalid')

        try:
            self.client.submissions.createMultiFiles('TEST', {'nonempty source': ''}, 422)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)
            
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_with_tar_source_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createSubmission/success')
    
        response = self.client.submissions.createWithTarSource('TEST', 'tar_source', 1)
        submission_id = response['id']
        self.assertTrue(submission_id > 0, 'Creation method should return new submission ID')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_with_tar_source_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')

        try:
            self.client.submissions.createWithTarSource('NON_EXISTING_CODE', 'nonempty source', 1)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_with_tar_source_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')

        nonexisting_compiler = 9999
        try:
            self.client.submissions.createWithTarSource('TEST', 'nonempty source', nonexisting_compiler)
            self.fail("Sphere Engine Exception with 404 code expected")
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_with_tar_source_method_nonexisting_compiler_version(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompilerVersion')

        nonexisting_compiler_version = 9999
        try:
            self.client.submissions.createWithTarSource('TEST', 'nonempty source', 1, compiler_version_id=nonexisting_compiler_version)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_with_tar_source_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/invalid')

        try:
            self.client.submissions.createWithTarSource('TEST', 'nonempty source', 422)
            self.fail("Sphere Engine Exception with 400 code expected")
        except SphereEngineException as e:
            self.assertEqual(400, e.code)
