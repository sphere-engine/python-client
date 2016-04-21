"""
Example presents usage of the successful submission.create() API method
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
source = 'int main() { return 0; }'
compiler = 11 # C language

response = client.submissions.create(problemCode, source, compiler)
# response['id'] stores the ID of the created submission
