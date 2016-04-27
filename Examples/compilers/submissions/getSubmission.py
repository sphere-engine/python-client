"""
Example presents usage of the successful submissions.get() API method
"""
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = 'your_access_token'
endpoint = 'compilers.sphere-engine.com'

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
response = client.submissions.get(2016)
