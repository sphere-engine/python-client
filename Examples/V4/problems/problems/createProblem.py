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
name = 'Example problem'

response = client.problems.create(name)
# response['id'] stores the ID of the created problem
