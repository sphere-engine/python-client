"""
Example presents error handling for submissions.create() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
submissionId = 1
private = True

try:
    response = client.submissions.update(submissionId, private)
except SphereEngineException as e:
    if e.code == 401:
    	print('Invalid access token')
    elif e.code == 403:
    	print('Access to the submission is forbidden')
    elif e.code == 404:
    	print('Submission does not exist')
