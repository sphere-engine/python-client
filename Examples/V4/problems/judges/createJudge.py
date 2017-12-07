"""
Example presents usage of the successful judges.create() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
source = '<source code>'
compiler = 11 # C language

response = client.judges.create(source, compiler)
# response['id'] stores the ID of the created judge
