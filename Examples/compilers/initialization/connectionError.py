"""
Example presents connection error handling for
Sphere Engine Compilers API client
"""
import os
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = 'your_access_token'
endpoint = 'compilers.sphere-engine.com'

# initialization
try:
    client = CompilersClientV3(accessToken, endpoint)
    client.test()
except ConnectionError as e:
    print('Error: API connection error: ' + str(e))
