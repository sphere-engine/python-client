"""
Example presents error handling for submissions.getMulti() API method
"""
from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV4(accessToken, endpoint)

# API usage
try:
    response = client.submissions.getMulti([2017, 2018])
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 400:
        print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
