"""
Example presents usage of the successful problems.updateTestcase() API method
"""
import os
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_PROBLEMS']
endpoint = os.environ['SE_ENDPOINT_PROBLEMS']

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'TEST'
testcaseNumber = 0
newInput = 'New testcase input'

response = client.problems.updateTestcase(problemCode, testcaseNumber, newInput)