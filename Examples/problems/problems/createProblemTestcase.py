"""
Example presents usage of the successful problems.createTestcase() API method
"""
import os
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = 'your_access_token'
endpoint = 'problems.sphere-engine.com'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
code = 'EXAMPLE'
input = 'model input'
output = 'model output'
timelimit = 5
judgeId = 1

response = client.problems.createTestcase(code, input, output, timelimit, judgeId)
# response['number'] stores the number of created testcase
