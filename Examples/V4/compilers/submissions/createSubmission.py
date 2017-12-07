"""
Example presents usage of the successful submissions.create() API method
"""
from sphere_engine import CompilersClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV4(accessToken, endpoint)

# API usage
source = '<source code>'
compiler = 11 # C language
input = '2017'

response = client.submissions.create(source, compiler, input)
# response['id'] stores the ID of the created submission
