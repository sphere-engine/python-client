"""
Example presents connection error handling for
Sphere Engine Problems API client
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
try:
    client = ProblemsClientV4(accessToken, endpoint)
    client.test()
except ConnectionError as e:
    print('Error: API connection error: ' + str(e))
