"""
Example presents usage of the successful submissions.create() API method
"""
import os
from sphere_engine import CompilersClientV3

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_COMPILERS']
endpoint = os.environ['SE_ENDPOINT_COMPILERS']

# initialization
client = CompilersClientV3(accessToken, endpoint)

# API usage
source = 'int main() { return 0; }'
compiler = 11 # C language
input = '2016'

response = client.submissions.create(source, compiler, input)
# response['id'] stores the ID of the created submission
