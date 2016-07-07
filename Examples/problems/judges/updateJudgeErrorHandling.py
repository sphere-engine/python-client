"""
Example presents error handling for judges.update() API method
"""
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
source = 'int main() { return 0; }'
nonexistingCompiler = 9999

try:
    response = client.judges.update(1, source, nonexistingCompiler)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 400:
        print('Empty source')
    elif e.code == 403:
        print('Access to the judge is forbidden')
    elif e.code == 404:
        # aggregates two possible reasons of 404 error
        # non existing judge or compiler
        print('Non existing resource (judge, compiler), details available in the message: ' + str(e))
