"""
Example presents usage of the successful problems.update() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
newProblemName = 'New example problem name'

response = client.problems.update('EXAMPLE', newProblemName)
