"""
Example presents error handling for submissions.create() API method
"""
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
source = '<source code>'
compiler = 11 # C language
input = '2016'

try:
    response = client.submissions.create(source, compiler, input)
    # response['id'] stores the ID of the created submission
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
