"""
Example presents usage of the successful initialization of
Sphere Engine Compilers API client
"""
import os
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_COMPILERS']
endpoint = os.environ['SE_ENDPOINT_COMPILERS']

# initialization
client = CompilersClientV3(accessToken, endpoint)