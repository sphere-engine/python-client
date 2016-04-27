"""
Example presents usage of the successful problems.create() API method
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
name = 'Example problem'

response = client.problems.create(code, name)
# response['id'] stores the ID of the created problem
