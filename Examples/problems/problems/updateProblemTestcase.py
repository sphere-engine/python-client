"""
Example presents usage of the successful problems.updateTestcase() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'TEST'
testcaseNumber = 0
newInput = 'New testcase input'

response = client.problems.updateTestcase(problemCode, testcaseNumber, newInput)
