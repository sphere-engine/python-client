"""
Example presents usage of the successful test() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = 'your_access_token'
endpoint = 'problems.sphere-engine.com'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
response = client.test()
