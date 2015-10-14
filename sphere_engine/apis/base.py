
from sphere_engine.api_client import ApiClient

class AbstractApi(object):
    
    api_client = None # :type ApiClient 
    
    def __init__(self, api_client):
        self.api_client = api_client
        