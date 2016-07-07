"""
Example presents usage of the successful problems.createTestcase() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

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
