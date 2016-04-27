"""
Example presents authorization error handling for
Sphere Engine Problems API client
"""
import os
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = 'wrong access token'
endpoint = 'problems.sphere-engine.com'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
try:
    client.test()
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
