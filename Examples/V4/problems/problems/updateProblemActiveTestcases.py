"""
Example presents usage of the successful problems.updateActiveTestcases() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
activeTestcases = [1,2,3]

response = client.problems.updateActiveTestcases(42, activeTestcases)
