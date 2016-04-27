"""
Example presents connection error handling for
Sphere Engine Problems API client
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = 'your_access_token'
endpoint = 'problems.sphere-engine.com'

# initialization
try:
    client = ProblemsClientV3(accessToken, endpoint)
    client.test()
except ConnectionError as e:
    print('Error: API connection error: ' + str(e))
