"""
Example presents authorization error handling for
Sphere Engine Compilers API client
"""
import os
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = 'wrong access token'
endpoint = 'compilers.sphere-engine.com'

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
try:
    client.test()
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
