"""
Example presents usage of the successful judges.create() API method
"""
import os
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = 'your_access_token'
endpoint = 'problems.sphere-engine.com'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
source = 'int main() { return 0; }'
compiler = 11 # C language

response = client.judges.create(source, compiler)
# response['id'] stores the ID of the created judge
