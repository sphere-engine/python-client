"""
Example presents error handling for judges.get() API method
"""
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = 'your_access_token'
endpoint = 'problems.sphere-engine.com'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
nonexisting_judge_id = 999999
try:
    response = client.judges.get(nonexisting_judge_id)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 404:
        print('Judge does not exist')
    elif e.code == 403:
        print('Access to the judge is forbidden')
