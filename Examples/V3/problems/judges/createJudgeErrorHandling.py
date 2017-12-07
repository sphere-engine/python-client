"""
Example presents error handling for judges.create() API method
"""
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
source = '<source code>'
nonexisting_compiler = 9999

try:
    response = client.judges.create(source, nonexisting_compiler)
    # response['id'] stores the ID of the created judge
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 400:
        print('Empty source')
    elif e.code == 404:
        print('Compiler does not exist')
