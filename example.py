from sphere_engine import CompilersClientV4
from sphere_engine import ProblemsClientV4


# define access parameters
accessTokenCompilers = '<access_token>'
endpointCompilers = '<endpoint>'
accessTokenProblems = '<access_token>'
endpointProblems = '<endpoint>'

# initialization
clientCompilers = CompilersClientV4(accessTokenCompilers, endpointCompilers)
clientProblems = ProblemsClientV4(accessTokenProblems, endpointProblems)

# API usage
response = clientCompilers.test()
print(response)

# API usage
response = clientProblems.test()
print(response)
