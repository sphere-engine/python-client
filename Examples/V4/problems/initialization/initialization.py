"""
Example presents usage of the successful initialization of
Sphere Engine Problems API client
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)
