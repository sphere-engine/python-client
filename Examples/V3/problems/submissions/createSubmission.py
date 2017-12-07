"""
Example presents usage of the successful submission.create() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'TEST'
source = '<source code>'
compiler = 11 # C language

response = client.submissions.create(problemCode, source, compiler)
# response['id'] stores the ID of the created submission
