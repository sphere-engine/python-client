"""
Example presents usage of the successful initialization of
Sphere Engine Compilers API client
"""
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV3(accessToken, endpoint)
