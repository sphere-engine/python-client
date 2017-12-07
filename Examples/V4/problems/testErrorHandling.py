"""
Example presents usage of the successful test() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
try:
    response = client.test()
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
