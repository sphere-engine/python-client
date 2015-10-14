
class SphereEngineException(Exception):
    
    code = 0
    
    def __init__(self, message, code=0):
        super(Exception, self).__init__(message)
        self.code = code
