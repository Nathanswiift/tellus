from typing import List
import json

data = {}

# Content-types
CONTENT_TYPE_PLAIN = ("Content-Type", "text/plain")

# Status code texts
NOT_FOUND = "URL not found"
METHOD_NOT_ALLOEWD = "Method is not allowed"
INTERNAL_SERVER_ERROR = "Internal server error"

class ErrorHandler:
    @classmethod
    def method_not_allowed(cls, start_response):
        """Function should be used when the requested method
        is not allowed.
        """
        data["content"] = METHOD_NOT_ALLOEWD
        data["content-type"] = CONTENT_TYPE_PLAIN
        data["status"] = '405'
        return data

    @classmethod
    def internal_server_error(cls, start_response):
        """Function should be used when an unexpected error occurs
        """
        data["content"] = INTERNAL_SERVER_ERROR
        data["content-type"] = CONTENT_TYPE_PLAIN
        data["status"] = '500'
        return data
    
    @classmethod
    def not_found(cls, start_response):
        """Function should be used when the endpoint cannot be found.
        """
        data["content"] = NOT_FOUND
        data["content-type"] = CONTENT_TYPE_PLAIN
        data["status"] = '404'
        return data

