"""
Example presents usage of the successful judges.update() API method
"""
import os
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_PROBLEMS']
endpoint = os.environ['SE_ENDPOINT_PROBLEMS']

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
source = 'int main() { return 0; }'
compiler = 11 # C language

response = client.judges.update(1, source, compiler)
