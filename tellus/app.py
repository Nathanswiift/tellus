from config import TellusConfig
from typing import List, Dict
from .errors import ErrorHandler
from .db import Database
from .router import RouteHandler

class Tellus:
    """TELLUS FRAMEWORK"
    
    Module that atleast acts abit like a framework.
    """

    def __init__(self):
        # import the configuration file
        self.config = TellusConfig

        # this will be the encoding for the app
        self.ENCODE = self.config.ENCODE

        # initiate the route handler
        self.route_handler = RouteHandler()

        # this is a decorator that should be used when
        # defining routes
        self.route = self.route_handler.route

    def __call__(self, env, start_response):
        """The call method 
        """
        URI = env["REQUEST_URI"]
        METHOD = env["REQUEST_METHOD"]
        try:
            valid = self.route_handler.validate(URI, METHOD)      
            if valid == True:
                return self.create_response(
                    self.route_handler.routes[URI]['function'], METHOD, start_response
                )
            else:
                return self.create_response(
                    valid, METHOD, start_response
                )
       
        except Exception as e:
            return self.create_response(ErrorHandler.internal_server_error, METHOD, start_response)

    def create_response(self, func, method, start_response):
        """Creates the response from the API
        """
        values = func(method)
        start_response(values["status"], [values["content-type"]])

        return bytes(str(values["content"]).encode(self.ENCODE))

    def run(self):
        """Development server

        This function is used when you want to use python directly
        over uWSGI
        """
        options = {"use_reloader": True, "use_debugger": True, "threaded": True}
        from werkzeug.serving import run_simple

        try:
            run_simple(TellusConfig.DEV_ENV, TellusConfig.DEV_ENV_PORT, self, options)
        finally:
            # reset the first request information if the development server
            # reset normally.  This makes it possible to restart the server
            # without reloader and that stuff from an interactive shell.
            self._got_first_request = False
