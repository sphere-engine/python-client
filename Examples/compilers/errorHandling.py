"""
Example presents complete error handling schema for calling API methods of
Sphere Engine Compilers API client
"""
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = 'your_access_token'
endpoint = 'compilers.sphere-engine.com'

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
try:
    # any API method usage
    # client.module.method(parameters..)
    pass
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 402:
        print('Payment required')
    elif e.code == 403:
        print('Access to the resource is forbidden')
    elif e.code == 404:
        print('Resource does not exist')
        # more details about missing resource are provided in str(e)
        # possible missing resources depend on called API method
    elif e.code == 400:
        print('Bad request')
        # more details about missing resource are provided in str(e)
        # possible reasons depend on called API method
    else:
        # handle unexpected error code
        pass
except ConnectionError as e:
    # handle API connection errors
    pass
except Exception as e:
    # handle other exceptions (connection or network errors etc.)
    pass
