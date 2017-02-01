import os
import sys
import nose
import unittest
from random import randrange
from sphere_engine import ProblemsClientV3
from array import array
from .test_commons import get_mock_data
from sphere_engine.exceptions import SphereEngineException
if (sys.version_info > (3, 3)):
    from unittest.mock import patch
else:
    from mock import patch

class TestProblems(unittest.TestCase):

    def setUp(self):
        self.client = ProblemsClientV3('access-token', 'endpoint')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_autorization_fail(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/unauthorizedAccess')
        try:
            self.client.test()
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertTrue(401, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_autorization_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/test')
        self.client.test()

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_test_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/test')
        self.assertTrue(len(self.client.test()['message']) > 0, 'Test method should return nonempty message')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_compilers_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/compilers')
        self.assertEqual('C++', self.client.compilers()['items'][0]['name'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_problems_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblems/default')
        problems = self.client.problems.all()
        self.assertEquals(10, problems['paging']['limit'])
        self.assertEquals(0, problems['paging']['offset'])
        self.assertEquals(False, 'shortBody' in problems['items'][0])
        self.assertEquals(True, 'lastModifiedBody' in problems['items'][0])
        self.assertEquals(True, 'lastModifiedSettings' in problems['items'][0])

        mock_get.return_value = get_mock_data('problems/getProblems/limit')
        self.assertEquals(11, self.client.problems.all(11)['paging']['limit'])

        mock_get.return_value = get_mock_data('problems/getProblems/default')
        self.assertEquals(False, 'shortBody' in self.client.problems.all(shortBody=False)['items'][0])

        mock_get.return_value = get_mock_data('problems/getProblems/shortBody')
        self.assertEquals(True, 'shortBody' in self.client.problems.all(shortBody=True)['items'][0])
    
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_problems_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblems/invalid')

        try:
            self.client.problems.all()
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblem/success')
        problem = self.client.problems.get('TEST')
        self.assertEquals('TEST', problem['code'])
        self.assertEquals(False, 'shortBody' in problem)
        self.assertEquals(True, 'lastModifiedBody' in problem)
        self.assertEquals(True, 'lastModifiedSettings' in problem)

        self.assertEquals(False, 'shortBody' in self.client.problems.get('TEST', False))

        mock_get.return_value = get_mock_data('problems/getProblem/shortBody')
        self.assertEquals(True, 'shortBody' in self.client.problems.get('TEST', True))
    
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_wrong_code(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.get('NON_EXISTING_PROBLEM')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertTrue(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblem/invalid')

        try:
            self.client.problems.get('CODE')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createProblem/success')
        problem_code = 'CODE'
        problem_name = 'UT name'
        problem_body = 'UT body'
        problem_type = 'maximize'
        problem_interactive = True
        problem_masterjudgeId = 1000
        self.assertEqual(
                problem_code,
                self.client.problems.create(
                        problem_code,
                        problem_name,
                        problem_body,
                        problem_type,
                        problem_interactive,
                        problem_masterjudgeId
                    )['code'],
                'Creation method should return new problem code')

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_code_taken(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/problemCodeTaken')
        try:
            self.client.problems.create('TEST', 'Taken problem code')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    def test_create_problem_method_code_empty(self):
        try:
            self.client.problems.create('', 'Empty problem code')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_code_invalid(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/problemCodeInvalid')
        try:
            self.client.problems.create('!@#$%^', 'Invalid problem code')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    def test_create_problem_method_empty_name(self):
        try:
            self.client.problems.create('UNIQUE_CODE', '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_method_nonexisting_masterjudge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingMasterjudge')
        nonexistingMasterjudgeId = 9999
        try:
            self.client.problems.create(
                'UNIQUE_CODE',
                'Nonempty name',
                'body',
                'binary',
                False,
                nonexistingMasterjudgeId)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createProblem/invalid')

        try:
            self.client.problems.create('CODE', 'name', 'body', 'binary', False, 1000)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblem/success')
        problem_code = 'CODE'
        problem_name = 'Name'
        new_problem_name = problem_name + 'updated'
        new_problem_body = 'update'
        new_problem_type = 'maximize'
        new_problem_interactive = 1
        new_problem_masterjudgeId = 1000
        self.client.problems.update(
                problem_code,
                new_problem_name,
                new_problem_body,
                new_problem_type,
                new_problem_interactive,
                new_problem_masterjudgeId)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.update('NON_EXISTING_CODE', 'Nonexisting problem code')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_method_nonexisting_masterjudge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingMasterjudge')
        nonexistingMasterjudgeId = 9999
        try:
            self.client.problems.update(
                'TEST',
                'Nonempty name',
                'body',
                'binary',
                0,
                nonexistingMasterjudgeId)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    def test_update_problem_method_empty_code(self):
        try:
            self.client.problems.update('', 'Nonempty name')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    def test_update_problem_method_empty_name(self):
        try:
            self.client.problems.update('TEST', '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblem/invalid')

        try:
            self.client.problems.update('CODE', 'name')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_active_testcases_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblem/success')
        self.client.problems.updateActiveTestcases('TEST', [])
        self.client.problems.updateActiveTestcases('TEST', [0])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_testcases_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcases/success')
        self.assertEquals(0, self.client.problems.allTestcases('TEST')['testcases'][0]['number'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_testcases_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.allTestcases('NON_EXISTING_CODE')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_testcases_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcases/invalid')

        try:
            self.client.problems.allTestcases('TEST')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcase/success')
        self.assertEquals(0, self.client.problems.getTestcase('TEST', 0)['number'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.getTestcase('NON_EXISTING_CODE', 0)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')
        try:
            self.client.problems.getTestcase('TEST', 1)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcase/invalid')

        try:
            self.client.problems.getTestcase('TEST', 422)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

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
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_testcase_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')
        nonexistingJudge = 9999
        try:
            self.client.problems.createTestcase('TEST', 'in0', 'out0', 10, nonexistingJudge, 1)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createProblemTestcase/invalid')

        try:
            self.client.problems.createTestcase('TEST', '422', '422', 10, 1, 1)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblemTestcase/success')

        new_testcase_input = 'in0updated'
        new_testcase_output = 'out0updated'
        new_testcase_timelimit = 10
        new_testcase_judge = 2
        new_testcase_active = 0

        self.client.problems.updateTestcase(
                'CODE',
                0,
                new_testcase_input,
                new_testcase_output,
                new_testcase_timelimit,
                new_testcase_judge,
                new_testcase_active)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.updateTestcase('NON_EXISTING_CODE', 0, 'updated input')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')
        try:
            self.client.problems.updateTestcase('TEST', 1, 'updated input')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')
        nonexistingJudge = 9999
        try:
            self.client.problems.updateTestcase('TEST', 0, 'updated input', 'updated output', 1, nonexistingJudge, 0)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateProblemTestcase/invalid')

        try:
            self.client.problems.updateTestcase('TEST', 0, '422', '422', 10, 1, 1)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/deleteProblemTestcase/success')
        self.client.problems.deleteTestcase('CODE', 1)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.deleteTestcase('NON_EXISTING_CODE', 0)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')
        try:
            self.client.problems.deleteTestcase('TEST', 1)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_delete_problem_testcase_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/deleteProblemTestcase/invalid')

        try:
            self.client.problems.deleteTestcase('TEST', 422)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcaseFile/input')
        self.assertEquals('in0', self.client.problems.getTestcaseFile('CODE', 0, 'input'))

        mock_get.return_value = get_mock_data('problems/getProblemTestcaseFile/output')
        self.assertEquals('out0', self.client.problems.getTestcaseFile('CODE', 0, 'output'))

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.problems.getTestcaseFile('NON_EXISTING_CODE', 0, 'input')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_nonexisting_testcase(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingTestcase')
        try:
            self.client.problems.getTestcaseFile('TEST', 1, 'input')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_nonexisting_file(self, mock_get):
        try:
            self.client.problems.getTestcaseFile('TEST', 0, 'fakefile')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_problem_testcase_file_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getProblemTestcaseFile/invalid')

        try:
            self.client.problems.getTestcaseFile('TEST', 422, 'input')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_judges_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudges/default')
        self.assertEquals(10, self.client.judges.all()['paging']['limit'])

        mock_get.return_value = get_mock_data('problems/getJudges/limit')
        self.assertEquals(11, self.client.judges.all(11)['paging']['limit'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_all_judges_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudges/invalid')

        try:
            self.client.judges.all()
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudge/success')
        self.assertEquals(1, self.client.judges.get(1)['id'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')
        nonexistingJudge = 9999
        try:
            self.client.judges.get(nonexistingJudge)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_judge_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getJudge/invalid')

        try:
            self.client.judges.get(422)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_judge_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createJudge/success')

        judge_source = 'source'
        judge_compiler = 1
        judge_type = 'testcase'
        judge_name = 'UT judge'

        response = self.client.judges.create(
            judge_source,
            judge_compiler,
            judge_type,
            judge_name)
        judge_id = response['id']
        self.assertTrue(judge_id > 0, 'Creation method should return new judge ID')

    def test_create_judge_method_empty_source(self):
        try:
            self.client.judges.create('', 1, 'testcase', '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_judge_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')
        nonexistingCompiler = 9999
        try:
            self.client.judges.create('nonempty source', nonexistingCompiler, 'testcase', '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_judge_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createJudge/invalid')

        try:
            self.client.judges.create('nonempty source', 422, 'testcase', '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateJudge/success')
        judge_id = 1
        new_judge_source = 'updated source'
        new_judge_compiler = 11
        new_judge_name = 'UT judge updated'

        self.client.judges.update(
                judge_id,
                new_judge_source,
                new_judge_compiler,
                new_judge_name)

    def test_update_judge_method_empty_source(self):
        try:
            self.client.judges.update(1, '', 1, '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_nonexisting_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingJudge')
        nonexistingJudge = 99999999
        try:
            self.client.judges.update(nonexistingJudge, 'nonempty source', 1, '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')
        judgeId = 1
        nonexistingCompiler = 9999
        try:
            self.client.judges.update(judgeId, 'nonempty source', nonexistingCompiler, '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_foreign_judge(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/deniedAccess')
        nonexistingCompiler = 9999
        try:
            self.client.judges.update(1, 'nonempty source', 1, '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(403, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_update_judge_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/updateJudge/invalid')

        try:
            self.client.judges.update(422, 'nonempty source', 422, '')
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmission/success')
        self.assertEquals(10, self.client.submissions.get(10)['id'])

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_nonexisting_submission(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingSubmission')
        nonexistingSubmission = 9999999999
        try:
            self.client.submissions.get(nonexistingSubmission)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)
    
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submission_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmission/invalid')

        try:
            self.client.submissions.get(422)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/two')
        response = self.client.submissions.getMulti([9, 4])
        
        self.assertTrue('items' in response)
        self.assertEquals(2, len(response['items']))
        self.assertTrue('id' in response['items'][0])
        self.assertTrue('id' in response['items'][1])
        
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_nonexisting_submission(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/empty')
        response = self.client.submissions.getMulti([9999999999])
        
        self.assertTrue('items' in response)
        self.assertEquals(0, len(response['items']))
    
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_valid_param(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/one')
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
        
    @patch('sphere_engine.ApiClient.make_http_call')
    def test_get_submissions_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/invalid')

        try:
            self.client.submissions.getMulti([422])
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_success(self, mock_get):
        mock_get.return_value = get_mock_data('problems/createSubmission/success')
        submission_problem_code = 'TEST'
        submission_source = 'source'
        submission_compiler = 1

        response = self.client.submissions.create(
                submission_problem_code,
                submission_source,
                submission_compiler)
        submission_id = response['id']
        self.assertTrue(submission_id > 0, 'Creation method should return new submission ID')

    def test_create_submission_method_empty_source(self):
        try:
            self.client.submissions.create('TEST', '', 1)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(400, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_nonexisting_problem(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingProblem')
        try:
            self.client.submissions.create('NON_EXISTING_CODE', 'nonempty source', 1)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_nonexisting_compiler(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingCompiler')
        nonexistingCompiler = 9999
        try:
            self.client.submissions.create('TEST', 'nonempty source', nonexistingCompiler)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_nonexisting_user(self, mock_get):
        mock_get.return_value = get_mock_data('exceptions/nonexistingUser')
        nonexistingUser = 9999999999
        try:
            self.client.submissions.create('TEST', 'nonempty source', 1, nonexistingUser)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(404, e.code)

    @patch('sphere_engine.ApiClient.make_http_call')
    def test_create_submission_method_invalid_response(self, mock_get):
        mock_get.return_value = get_mock_data('problems/getSubmissions/invalid')

        try:
            self.client.submissions.create('TEST', 'nonempty source', 422)
            self.assertTrue(False)
        except SphereEngineException as e:
            self.assertEqual(422, e.code)