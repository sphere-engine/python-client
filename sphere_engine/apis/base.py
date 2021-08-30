# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""


class AbstractApi(object):
    """
    Abstract API class
    """
    api_client = None # :type ApiClient

    def __init__(self, api_client):
        self.api_client = api_client
