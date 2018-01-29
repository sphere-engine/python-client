"""
Example presents usage of the successful submission.createWithTarSource() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
problemId = 42
tarSource = '<tar_source>'
compiler = 11 # C language

response = client.submissions.createWithTarSource(problemId, tarSource, compiler)
# response['id'] stores the ID of the created submission
