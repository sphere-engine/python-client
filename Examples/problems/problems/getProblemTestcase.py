"""
Example presents usage of the successful problems.getTestcase() API method
"""
import os
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = 'your_access_token'
endpoint = 'problems.sphere-engine.com'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'TEST'
testcaseNumber = 0

response = client.problems.getTestcase(problemCode, testcaseNumber)
