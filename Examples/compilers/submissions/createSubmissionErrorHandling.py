"""
Example presents error handling for submissions.create() API method
"""
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = 'your_access_token'
endpoint = 'compilers.sphere-engine.com'

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
source = 'int main() { return 0; }'
compiler = 11 # C language
input = '2016'

try:
    response = client.submissions.create(source, compiler, input)
    # response['id'] stores the ID of the created submission
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
