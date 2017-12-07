"""
Example presents usage of the successful submission.getSubmissionFile() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
response = client.submissions.getSubmissionFile(2017, 'source')
