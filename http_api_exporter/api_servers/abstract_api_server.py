"""
The base class of all api servers.
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

class AbstractApiServer(object):
    """This class is the main class which handles all the logic."""
    def __init__(self, *args, **kwargs):
        self.application = None
        self.periodic_tasks = []

    def bind(self, route=None, function=None, dictionary=None):
        """bind the route with function."""
        raise NotImplementedError("This function should be implemented in the subclass.")
                            
    def start_all_periodic_tasks(self):
        for task in self.periodic_tasks:
            task.start()

    def start(self, *args, **kwargs):
        """start the application"""
        raise NotImplementedError("This function should be implemented in the subclass.")

    def make_app(self):
        """make the application based on the router_list"""
        raise NotImplementedError("This function should be implemented in the subclass.")

    def add_periodic_task(self, function, interval):
        if not hasattr(function, '__call__'):
            raise TypeError('"function" should be a function.')
        if not (isinstance(interval, int) or isinstance(interval, float)):
            raise TypeError('"interval" should be an integer or float.')

        self.periodic_tasks.append(tornado.ioloop.PeriodicCallback(function, interval))
