"""
Example presents usage of the successful submission.createMultiFiles() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
problemCode = 'TEST'
files = {
    'prog.c': '<source_code>',
    'prog.h': '<source_code>'
}
compiler = 11 # C language

response = client.submissions.createMultiFiles(problemCode, files, compiler)
# response['id'] stores the ID of the created submission
