"""
Example presents usage of the successful problems.updateTestcase() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
problemId = 42
testcaseNumber = 0
newInput = 'New testcase input'

response = client.problems.updateTestcase(problemId, testcaseNumber, newInput)
