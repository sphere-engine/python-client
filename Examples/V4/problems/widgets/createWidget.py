"""
Example presents usage of the successful widgets.create() API method
"""
from sphere_engine import ProblemsClientV4
import datetime

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
name = 'Example widget'
problem_id = 42
compiler = 11 # C language
# date_from = datetime.datetime.utcnow() + datetime.timedelta(hours=1)


response = client.widgets.create(name, problem_id, compiler)
# response['hash'] stores the hash of the created widget
