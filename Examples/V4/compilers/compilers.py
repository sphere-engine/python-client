"""
Example presents usage of the successful compilers() API method
"""
from sphere_engine import CompilersClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV4(accessToken, endpoint)

# API usage
response = client.compilers()
