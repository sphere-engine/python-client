import os
import sys
import nose
import unittest
from random import randrange
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

if os.environ.get('SE_ENDPOINT_PROBLEMS', None) != None and \
    os.environ.get('SE_ACCESS_TOKEN_PROBLEMS', None) != None:

    class TestProblems(unittest.TestCase):

        def setUp(self):
            self.client = ProblemsClientV3(os.environ['SE_ACCESS_TOKEN_PROBLEMS'], os.environ['SE_ENDPOINT_PROBLEMS'])

        def test_autorization_fail(self):
            self.client = ProblemsClientV3('wrong-access-token', os.environ['SE_ENDPOINT_PROBLEMS'])
            try:
                self.client.test()
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 401)

        def test_autorization_success(self):
            self.client.test()

        def test_test_method_success(self):
            self.assertTrue(len(self.client.test()['message']) > 0, 'Test method should return nonempty message')

        def test_compilers_method_success(self):
            self.assertEqual('C++', self.client.compilers()['items'][0]['name'])

        def test_all_problems_method_success(self):
            self.assertEquals(10, self.client.problems.all()['paging']['limit'])
            self.assertEquals(11, self.client.problems.all(11)['paging']['limit'])

        def test_get_problem_method_success(self):
            self.assertEquals('TEST', self.client.problems.get('TEST')['code'])

        def test_get_problem_method_wrong_code(self):
            try:
                self.client.problems.get('NON_EXISTING_PROBLEM')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_create_problem_method_success(self):
            r = str(randrange(1000000,9999999)) + str(randrange(1000000,9999999)) # 14-digits random string
            problem_code = 'UT' + r
            problem_name = 'UT' + r
            problem_body = 'UT' + r + ' body'
            problem_type = 'maximize'
            problem_interactive = True
            problem_masterjudgeId = 1000
            self.assertEquals(
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
            p = self.client.problems.get(problem_code)
            self.assertEquals(problem_code, p['code'], 'Problem code')
            self.assertEquals(problem_name, p['name'], 'Problem name')
            self.assertEquals(problem_body, p['body'], 'Problem body')
            self.assertEquals(problem_type, p['type'], 'Problem type')
            self.assertEquals(problem_interactive, p['interactive'], 'Problem interactive')
            self.assertEquals(problem_masterjudgeId, p['masterjudge']['id'], 'Problem masterjudgeId')

        def test_create_problem_method_code_taken(self):
            try:
                self.client.problems.create('TEST', 'Taken problem code')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 400)

        def test_create_problem_method_code_empty(self):
            try:
                self.client.problems.create('', 'Empty problem code')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 400)

        def test_create_problem_method_code_invalid(self):
            try:
                self.client.problems.create('!@#$%^', 'Invalid problem code')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 400)

        def test_create_problem_method_empty_name(self):
            try:
                self.client.problems.create('UNIQUE_CODE', '')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 400)

        def test_create_problem_method_nonexisting_masterjudge(self):
            nonexistingMasterjudgeId = 9999;
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
                self.assertTrue(e.code == 404)

        def test_update_problem_method_success(self):
            r = str(randrange(1000000,9999999)) + str(randrange(1000000,9999999)) # 14-digits random string
            # create problem to update
            problem_code = 'UT' + r
            problem_name = 'UT' + r
            self.client.problems.create(problem_code, problem_name)

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
            p = self.client.problems.get(problem_code)
            self.assertEquals(problem_code, p['code'], 'Problem code')
            self.assertEquals(new_problem_name, p['name'], 'Problem name')
            self.assertEquals(new_problem_body, p['body'], 'Problem body')
            self.assertEquals(new_problem_type, p['type'], 'Problem type')
            self.assertEquals(new_problem_interactive, p['interactive'], 'Problem interactive')
            self.assertEquals(new_problem_masterjudgeId, p['masterjudge']['id'], 'Problem masterjudgeId')

        def test_update_problem_method_nonexisting_problem(self):
            try:
                self.client.problems.update('NON_EXISTING_CODE', 'Nonexisting problem code')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_update_problem_method_nonexisting_masterjudge(self):
            nonexistingMasterjudgeId = 9999;
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
                self.assertTrue(e.code == 404)

        def test_update_problem_method_empty_code(self):
            try:
                self.client.problems.update('', 'Nonempty name')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 400)

        def test_update_problem_method_empty_name(self):
            try:
                self.client.problems.update('TEST', '')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 400)

        def test_update_problem_active_testcases_method_success(self):
            self.client.problems.updateActiveTestcases('TEST', [])
            self.assertEquals('', self.client.problems.get('TEST')['seq'])
            self.client.problems.updateActiveTestcases('TEST', [0])
            self.assertEquals('#0', self.client.problems.get('TEST')['seq'])

        def test_all_testcases_method_success(self):
            self.assertEquals(0, self.client.problems.allTestcases('TEST')['testcases'][0]['number'])

        def test_get_problem_testcases_method_nonexisting_problem(self):
            try:
                self.client.problems.allTestcases('NON_EXISTING_CODE')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_get_problem_testcase_method_success(self):
            self.assertEquals(0, self.client.problems.getTestcase('TEST', 0)['number'])

        def test_get_problem_testcase_method_nonexisting_problem(self):
            try:
                self.client.problems.getTestcase('NON_EXISTING_CODE', 0)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_get_problem_testcase_method_nonexisting_testcase(self):
            try:
                self.client.problems.getTestcase('TEST', 1)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_create_problem_testcase_method_success(self):
            r = str(randrange(1000000,9999999)) + str(randrange(1000000,9999999)) # 14-digits random string
            # create problem to create testcases
            problem_code = 'UT' + r;
            problem_name = 'UT' + r;
            self.client.problems.create(problem_code, problem_name)

            self.client.problems.createTestcase(problem_code, 'in0', 'out0', 10, 2, 0)
            ptc = self.client.problems.getTestcase(problem_code, 0)
            self.assertEquals(0, ptc['number'], 'Testcase number')
            self.assertEquals(False, ptc['active'], 'Testcase active')
            self.assertEquals(str(10), ptc['limits']['time'], 'Testcase timelimit')
            self.assertEquals(3, ptc['input']['size'], 'Testcase input size')
            self.assertEquals(4, ptc['output']['size'], 'Testcase output size')
            self.assertEquals(2, ptc['judge']['id'], 'Testcase judge')

        def test_create_problem_testcase_method_nonexisting_problem(self):
            try:
                self.client.problems.createTestcase('NON_EXISTING_CODE', 'in0', 'out0', 10, 2, 1)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_create_problem_testcase_method_nonexisting_judge(self):
            nonexistingJudge = 9999;
            try:
                self.client.problems.createTestcase('TEST', 'in0', 'out0', 10, nonexistingJudge, 1)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_update_problem_testcase_method_success(self):
            r = str(randrange(1000000,9999999)) + str(randrange(1000000,9999999)) # 14-digits random string
            # create problem and testcase to update the testcase
            problem_code = 'UT' + r
            problem_name = 'UT' + r
            self.client.problems.create(problem_code, problem_name)
            self.client.problems.createTestcase(problem_code, 'in0', 'out0', 1, 1, 1)

            new_testcase_input = 'in0updated'
            new_testcase_output = 'out0updated'
            new_testcase_timelimit = 10
            new_testcase_judge = 2
            new_testcase_active = 0

            self.client.problems.updateTestcase(
                    problem_code,
                    0,
                    new_testcase_input,
                    new_testcase_output,
                    new_testcase_timelimit,
                    new_testcase_judge,
                    new_testcase_active)

            ptc = self.client.problems.getTestcase(problem_code, 0)
            self.assertEquals(0, ptc['number'], 'Testcase number')
            self.assertEquals(False, ptc['active'], 'Testcase active')
            self.assertEquals(str(new_testcase_timelimit), ptc['limits']['time'], 'Testcase timelimit')
            self.assertEquals(len(new_testcase_input), ptc['input']['size'], 'Testcase input size')
            self.assertEquals(len(new_testcase_output), ptc['output']['size'], 'Testcase output size')
            self.assertEquals(new_testcase_judge, ptc['judge']['id'], 'Testcase judge')

        def test_update_problem_testcase_method_nonexisting_problem(self):
            try:
                self.client.problems.updateTestcase('NON_EXISTING_CODE', 0, 'updated input')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_update_problem_testcase_method_nonexisting_testcase(self):
            try:
                self.client.problems.updateTestcase('TEST', 1, 'updated input');
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_update_problem_testcase_method_nonexisting_judge(self):
            nonexistingJudge = 9999;
            try:
                self.client.problems.updateTestcase('TEST', 0, 'updated input', 'updated output', 1, nonexistingJudge, 0)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_delete_problem_testcase_method_success(self):
            r = str(randrange(1000000,9999999)) + str(randrange(1000000,9999999)) # 14-digits random string
            # create problem and testcase to delete the testcase
            problem_code = 'UT' + r
            problem_name = 'UT' + r
            self.client.problems.create(problem_code, problem_name)
            self.client.problems.createTestcase(problem_code, 'in0', 'out0', 1, 1, 1)
            self.client.problems.createTestcase(problem_code, 'in1', 'out1', 1, 1, 1)
            self.client.problems.deleteTestcase(problem_code, 0)

            p = self.client.problems.get(problem_code)
            self.assertEquals(1, len(p['testcases']))

            self.client.problems.deleteTestcase(problem_code, 1)

            p = self.client.problems.get(problem_code)
            self.assertEquals(0, len(p['testcases']))

        def test_delete_problem_testcase_method_nonexisting_problem(self):
            try:
                self.client.problems.deleteTestcase('NON_EXISTING_CODE', 0)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_delete_problem_testcase_method_nonexisting_testcase(self):
            try:
                self.client.problems.deleteTestcase('TEST', 1)
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_get_problem_testcase_file_method_success(self):
            r = str(randrange(1000000,9999999)) + str(randrange(1000000,9999999)) # 14-digits random string
            # create problem and testcase to retrieve file
            problem_code = 'UT' + r
            problem_name = 'UT' + r
            self.client.problems.create(problem_code, problem_name)
            self.client.problems.createTestcase(problem_code, 'in0', 'out0', 1, 1, 1)

            self.assertEquals('in0', self.client.problems.getTestcaseFile(problem_code, 0, 'input'))
            self.assertEquals('out0', self.client.problems.getTestcaseFile(problem_code, 0, 'output'))

        def test_get_problem_testcase_file_method_nonexisting_problem(self):
            try:
                self.client.problems.getTestcaseFile('NON_EXISTING_CODE', 0, 'input')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_get_problem_testcase_file_method_nonexisting_testcase(self):
            try:
                self.client.problems.getTestcaseFile('TEST', 1, 'input')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)

        def test_get_problem_testcase_file_method_nonexisting_file(self):
            try:
                self.client.problems.getTestcaseFile('TEST', 0, 'fakefile')
                self.assertTrue(False)
            except SphereEngineException as e:
                self.assertTrue(e.code == 404)
