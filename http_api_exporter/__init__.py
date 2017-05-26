import tornado.ioloop
import tornado.web
import json
import traceback
import os
import socket
import logging
from .Log_helper import getLogger
from .Handler import *
from tornado.options import options

class ApiHttpServer:
    
    def __init__(self, functionDict = dict(), WelcomePage = "Python APIs are providing.", debug = False):
        logger = getLogger(self.__class__.__name__)
        
        self.__logger = logger
        
        self.__functionDict = dict()
        for key, item in functionDict.items():
            self.bind(key, item)
            
        self.__WelcomePage = WelcomePage
    
    def bind(self, route = None, function = None, diction = None):
        logger = self.__logger
        
        if isinstance(diction, dict):
            for _route, _function in diction.items():
                logger.info('Bind route "%s" with function "%s"' % (_route, _function.__name__))
                self.__functionDict[_route] = _function
        elif hasattr(function, '__call__') and isinstance(route, str):
                logger.info('Bind route "%s" with function "%s"' % (route, function.__name__))
                self.__functionDict[route] = function
        else:
            raise TypeError("'route' should be a str and 'function' should be a function. Or diction should be a dictonary")
        
    def start(self, port = 80, retry = 5):
        app = self.__make_app()
        checkListen = None
        for tried in range(retry + 1):
            try:
                checkListen = app.listen(port + tried)
                self.__logger.info("The server starts at port {0}".format(port + tried))
                break
            except socket.error as e:
                self.__logger.info("Port {0} has been used.".format(port + tried))
        if checkListen is None :
            self.__logger.warning("All retries failed.")
            raise socket.error("Port {0} to {1} have been used.".format(port, port + retry))
        tornado.ioloop.IOLoop.current().start()
        
    def __make_app(self):
        RouterList = list()
        for router, function in self.__functionDict.items():
            RouterList.append(('/' + router, MainHandler, dict(Function = function, logger = self.__logger)))
        
        RouterList.append((r'/', WelcomeHandler, dict(WelcomePage=self.__WelcomePage, logger = self.__logger)))
        return tornado.web.Application(RouterList)