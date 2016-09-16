"""
Example presents error handling for submissions.getStream() API method
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
    response = client.submissions.getStream(2016, 'nonexistingstream')
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 404:
        # aggregates two possible reasons of 404 error
        # non existing submission or stream
        print('Non existing resource (submission, stream), details available in the message: ' + str(e))
