"""
Example presents usage of the successful submissions.getMulti() API method
"""
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
response = client.submissions.getMulti([2017, 2018])
