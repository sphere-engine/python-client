"""
Example presents usage of the successful submissions.createMultiFiles() API method
"""
from sphere_engine import CompilersClientV4

# define access parameters
accessToken = 'cf2fb7f72657ec8df3cc0e79e3a9dc02'
endpoint = 'sec.dev-container.lo:8080'

# initialization
client = CompilersClientV4(accessToken, endpoint)

# API usage
files = {
    'prog.c': '<source_code>',
    'prog.h': '<source_code>'
}
compiler = 11 # C language
input = '2017'

response = client.submissions.createMultiFiles(files, compiler, input)
# response['id'] stores the ID of the created submission
