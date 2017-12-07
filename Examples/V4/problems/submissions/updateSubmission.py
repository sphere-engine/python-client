"""
Example presents usage of the successful submission.update() API method
"""
from sphere_engine import ProblemsClientV4

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
submissionId = 1
private = True

response = client.submissions.update(submissionId, private)
