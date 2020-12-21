from functools import wraps
from .errors import ErrorHandler

class RouteHandler:
    """Used to handle the routes
    
    The class both registers and validates the routes. 
    """
    def __init__(self):
        # this is the dictionary that stores all available routes 
        self.routes = {}
    
    def route(self, endpoint, methods=['GET']):  
        """Decorator that is used to define routes.
        """ 
        def route_wrapper(func, **kwargs):
            self.routes[endpoint] = {
                        "methods": methods,
                        "function": func
                    }                
        return route_wrapper

    def validate(self, endpoint, method):
        """Used to validate the endpoints 
        
        the function both validates that the endpoint exists and 
        that the endpoint allows usage of the requested method
        """
        if endpoint not in self.routes:
            return ErrorHandler.not_found

        if method not in self.routes[endpoint]['methods']:
            return ErrorHandler.method_not_allowed

        return True