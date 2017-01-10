"""
Example presents error handling for submissions.getMulti() API method
"""
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
try:
    response = client.submissions.getMulti([2017, 2018])
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
