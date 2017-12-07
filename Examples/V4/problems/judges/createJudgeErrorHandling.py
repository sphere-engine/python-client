"""
Example presents error handling for judges.create() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
source = '<source code>'
compiler = 11 # C language

try:
    response = client.judges.create(source, compiler)
    # response['id'] stores the ID of the created judge
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 400:
        print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
