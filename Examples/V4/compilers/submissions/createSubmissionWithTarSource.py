"""
Example presents usage of the successful submissions.createWithTarSource() API method
"""
from sphere_engine import CompilersClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = CompilersClientV4(accessToken, endpoint)

# API usage
tar_source = '<tar_source>'
compiler = 11 # C language
input = '2017'

response = client.submissions.createWithTarSource(tar_source, compiler, input)
# response['id'] stores the ID of the created submission
