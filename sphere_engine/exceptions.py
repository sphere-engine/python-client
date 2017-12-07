# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

class SphereEngineException(Exception):
    """
    Exceptions for Sphere Engine
    """

    code = 0
    
    error_code = 0

    def __init__(self, message, code=0, error_code=0):
        super(Exception, self).__init__(message)
        self.code = code
        self.error_code = error_code
