"""
Example presents usage of the successful problems.deleteTestcase() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'EXAMPLE'
testcaseNumber = 0

response = client.problems.deleteTestcase(problemCode, testcaseNumber)
