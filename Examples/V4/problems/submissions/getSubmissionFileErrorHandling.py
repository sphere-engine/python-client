"""
Example presents error handling for judges.getJudgeFile() API method
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
    response = client.submissions.getSubmissionFile(2017, 'source')
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the submission is forbidden')
    elif e.code == 404:
        print('Non existing resource, error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))