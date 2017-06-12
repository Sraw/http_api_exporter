"""
This is the main file of this http_api_exporter module. This module is designed
to easily export apis as http services.
"""
import json
import traceback
import os
import socket
import logging
import tornado
import tornado.web
import tornado.ioloop
from http_api_exporter.log_helper import get_logger
from http_api_exporter.handler import WelcomeHandler, MainHandler

class ApiHttpServer(object):
    """This class is the main class which handles all the logic."""
    def __init__(self, function_dict=None,
                 welcome_page="Python APIs are providing.",
                 debug=False):
        logger = get_logger(self.__class__.__name__, debug)

        self.__logger = logger

        self.__function_dict = dict()
        if function_dict:
            for key, item in function_dict.items():
                self.bind(key, item)

        self.__welcome_page = welcome_page
        self.application = None

    def bind(self, route=None, function=None, dictionary=None):
        """bind the route with function."""
        logger = self.__logger

        if isinstance(dictionary, dict):
            for _route, _function in dictionary.items():
                logger.info('Bind route "%s" with function "%s"', _route, _function.__name__)
                self.__function_dict[_route] = _function
        elif hasattr(function, '__call__') and isinstance(route, str):
            logger.info('Bind route "%s" with function "%s"', route, function.__name__)
            self.__function_dict[route] = function
        else:
            raise TypeError("'route' should be a str and 'function' should be a function."
                            " Or dictionary should be a dictonary")

    def start(self, port=80, retry=0):
        """start IOLoop listen on the specific port."""
        if self.application:
            app = self.application
        else:
            app = self.__make_app()

        check_listen = None
        for tried in range(retry + 1):
            try:
                check_listen = app.listen(port + tried)
                self.__logger.info("The server starts at port %d", port + tried)
                break
            except socket.error:
                self.__logger.info("Port %d has been used.", port + tried)
        if check_listen is None:
            if retry > 0:
                self.__logger.warning("All retries failed.")
                raise socket.error("Port %d to %d have been used,"
                                   " please change your port.", port, port + retry)
            else:
                raise socket.error("Port %d has been used,"
                                   " please consider to enable retry"
                                   " or change your port", port)
        tornado.ioloop.IOLoop.current().start()

    def __make_app(self):
        """make the application based on the router_list"""
        router_list = list()
        for router, function in self.__function_dict.items():
            router_list.append((router, MainHandler, dict(function=function, logger=self.__logger)))

        router_list.append((r'/', WelcomeHandler, dict(welcome_page=self.__welcome_page,
                                                       logger=self.__logger)))

        self.application = tornado.web.Application(router_list)
        return self.application
