"""
Example presents usage of the successful problems.create() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
code = 'EXAMPLE'
name = 'Example problem'

response = client.problems.create(code, name)
# response['id'] stores the ID of the created problem
