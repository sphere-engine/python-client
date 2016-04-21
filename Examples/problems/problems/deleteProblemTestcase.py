"""
Example presents usage of the successful problems.deleteTestcase() API method
"""
import os
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_PROBLEMS']
endpoint = os.environ['SE_ENDPOINT_PROBLEMS']

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'EXAMPLE'
testcaseNumber = 0

response = client.problems.deleteTestcase(problemCode, testcaseNumber)
