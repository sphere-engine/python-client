"""
Example presents usage of the successful judges.create() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
source = '<source code>'
compiler = 11 # C language

response = client.judges.create(source, compiler)
# response['id'] stores the ID of the created judge
