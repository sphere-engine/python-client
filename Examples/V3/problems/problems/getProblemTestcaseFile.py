"""
Example presents usage of the successful problems.getTestcaseFile() API method
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
file = 'input'

response = client.problems.getTestcaseFile(problemCode, testcaseNumber, file)
