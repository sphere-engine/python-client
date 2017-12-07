"""
Example presents error handling for judges.update() API method
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
    response = client.judges.update(1, source, compiler)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the judge is forbidden')
    elif e.code == 404:
    	print('Judge does not exist')
	elif e.code == 400:
		print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))