"""
Example presents error handling for submissions.get() API method
"""
import os
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_COMPILERS']
endpoint = os.environ['SE_ENDPOINT_COMPILERS']

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
try:
    nonexisting_submission_id = 999999999;
    response = client.submissions.get(nonexisting_submission_id)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 404:
        print('Submission does not exist')
