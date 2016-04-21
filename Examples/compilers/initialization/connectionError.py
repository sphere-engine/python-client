"""
Example presents connection error handling for
Sphere Engine Compilers API client
"""
import os
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_COMPILERS']
endpoint = os.environ['SE_ENDPOINT_COMPILERS']

# initialization
try:
    client = CompilersClientV3(accessToken, endpoint)
    client.test()
except ConnectionError as e:
    print('Error: API connection error: ' + str(e))
