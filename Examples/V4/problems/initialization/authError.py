"""
Example presents authorization error handling for
Sphere Engine Problems API client
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = 'wrong access token'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
try:
    client.test()
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
