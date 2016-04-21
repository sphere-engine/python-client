"""
Example presents usage of the successful test() API method
"""
import os
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_COMPILERS']
endpoint = os.environ['SE_ENDPOINT_COMPILERS']

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
response = client.test()