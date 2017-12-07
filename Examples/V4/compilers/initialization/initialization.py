"""
Example presents usage of the successful initialization of
Sphere Engine Compilers API client
"""
from sphere_engine import CompilersClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV4(accessToken, endpoint)
