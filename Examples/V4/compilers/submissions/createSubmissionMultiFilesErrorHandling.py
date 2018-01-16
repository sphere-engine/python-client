"""
Example presents error handling for submissions.createMultiFiles() API method
"""
from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV4(accessToken, endpoint)

# API usage
files = {
    'prog.c': '<source_code>',
    'prog.h': '<source_code>'
}
compiler = 11 # C language
input = '2017'

try:
    response = client.submissions.createMultiFiles(files, compiler, input)
    # response['id'] stores the ID of the created submission
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 402:
        print('Unable to create submission')
    elif e.code == 400:
        print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
