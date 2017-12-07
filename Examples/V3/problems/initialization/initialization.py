"""
Example presents usage of the successful initialization of
Sphere Engine Problems API client
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)
