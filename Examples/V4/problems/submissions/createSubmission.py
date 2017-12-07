"""
Example presents usage of the successful submission.create() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
problemCode = 'TEST'
source = '<source code>'
compiler = 11 # C language

response = client.submissions.create(problemCode, source, compiler)
# response['id'] stores the ID of the created submission
