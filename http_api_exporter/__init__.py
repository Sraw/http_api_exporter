import tornado.ioloop
import tornado.web
import json
import traceback
import logging
import os
from .Log_helper import getLogger

class ApiHttpServer:
    
    def __init__(self, functionDict = dict(), WelcomePage = "Python APIs are providing.", debug = False):
        logger = getLogger(self.__class__.__name__)
        
        self.__logger = logger
        
        self.__functionDict = dict()
        for key, item in functionDict.items():
            self.bind(key, item)
            
        self.__WelcomePage = WelcomePage
    
    def __make_app(self):
        RouterList = list()
        for router, function in self.__functionDict.items():
            RouterList.append(('/' + router, self.__MainHandler, dict(Function = function, logger = self.__logger)))
        
        RouterList.append((r'/', self.__WelcomeHandler, dict(WelcomePage=self.__WelcomePage, logger = self.__logger)))
        return tornado.web.Application(RouterList)
    
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
        
    def start(self, port = 80):
        app = self.__make_app()
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()
        
    class __WelcomeHandler(tornado.web.RequestHandler):
        def initialize(self, WelcomePage, logger):
            self.__WelcomePage = WelcomePage
            self.__logger = logger
        
        def get(self):
            self.write(self.__WelcomePage)
    
    class __MainHandler(tornado.web.RequestHandler):
        def initialize(self, Function, logger):
            self.__Function = Function
            self.__logger = logger

        def post(self):
            logger = self.__logger
            
            logger.info('A coming request at route "%s".' % (self.request.uri))
            
            self.set_header("content-type","application/json")
            
            try:
                form = json.loads(self.request.body.decode('utf8'))
            except Exception as e:
                self.set_status(400)
                ErrorMsg = self.__getErrorMsg(1001, "Body parse error, only JSON is accepted.")
                self.write(ErrorMsg)
                return
            
            try:
                if 'Input' in form:
                    Input = form['Input']
                    del form['Input']
                    ArgsDict = form
                else:
                    Input = list()
                    ArgsDict = form
                    
                if not isinstance(Input, list):
                    self.set_status(400)
                    ErrorMsg = self.__getErrorMsg(1002, "Input must be a list.")
                    self.write(ErrorMsg)
                    return
                
                result = self.__Function(*Input, **ArgsDict)
                
                if not isinstance(result, dict):
                    self.set_status(400)
                    ErrorMsg = self.__getErrorMsg(1002, "The result of function must be a dict.")
                    self.write(ErrorMsg)
                    return
                
                JsonOutput = self.__getSuccessMsg(1000, result)
                self.set_status(200)
                self.write(JsonOutput)
                return
            except KeyError as e:
                self.set_status(400)
                ErrorMsg = self.__getErrorMsg(1002, '{0} is not a available function.'.format(e))
                self.write(ErrorMsg)
                return
            except Exception as e:
                self.set_status(500)
                ErrorMsg = self.__getErrorMsg(1004, traceback.format_exc())
                traceback.print_exc()
                self.write(ErrorMsg)

        def __getErrorMsg(self, code, msg):
            msgDict = {
                'code' : code,
                'msg' : msg
            }
            msgJson = json.dumps(msgDict, ensure_ascii=False)
            return msgJson

        def __getSuccessMsg(self, code, result):
            msgDict = result
            msgDict['code'] = code
            msgJson = json.dumps(msgDict, ensure_ascii=False)
            return msgJson