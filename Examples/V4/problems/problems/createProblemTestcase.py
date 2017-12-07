"""
Example presents usage of the successful problems.createTestcase() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
code = 'EXAMPLE'
input = 'model input'
output = 'model output'
time_limit = 5
judgeId = 1

response = client.problems.createTestcase(code, input, output, time_limit, judgeId)
# response['number'] stores the number of created testcase
