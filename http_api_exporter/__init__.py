import tornado.ioloop
import tornado.web
import json
import traceback
import logging
import os

class ApiHttpServer:
    
    def __init__(self, functionDict = dict(), WelcomePage = "Python APIs are providing.", debug = False):
        
        #set logging
        logger = logging.getLogger()
        
        logger.setLevel(logging.NOTSET)
        
        formatter = logging.Formatter(
                '%(asctime)s - %(name)s.%(funcName)s %(levelname)-5s : %(message)s',
                '%m-%d %H:%M'
            )
        
        LOG_DIR = "logs"
        LOG_FILE = 'APIphone.log'
        
        LOG_DIR = os.path.join(os.path.dirname(__file__), LOG_DIR)
        LOG_FILE = os.path.join(LOG_DIR, LOG_FILE)
        
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
        
        if not os.path.exists(LOG_FILE):
            open(LOG_FILE, 'w').close()
        
        hdlr = logging.handlers.TimedRotatingFileHandler(
                LOG_FILE,
                when = "D",
                interval = 1,
                backupCount = 7
            )
        hdlr.setLevel(logging.DEBUG)
        hdlr.setFormatter(formatter)
            
        console = logging.StreamHandler()
        if debug:
            console.setLevel(logging.DEBUG)
        else:
            console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        
        logger.handlers = []
        logger.addHandler(hdlr)
        logger.addHandler(console)
        
        logger = logging.getLogger(self.__class__.__name__)
        #finish set logging
        
        self.__functionDict = dict()
        for key, item in functionDict.items():
            self.bind(key, item)
            
        self.__WelcomePage = WelcomePage
    
    def __make_app(self):
        RouterList = list()
        for router, function in self.__functionDict.items():
            RouterList.append(('/' + router, self.__MainHandler, dict(Function = function)))
        
        RouterList.append((r'/', self.__WelcomeHandler, dict(WelcomePage=self.__WelcomePage)))
        return tornado.web.Application(RouterList)
    
    def bind(self, route = None, function = None, diction = None):
        logger = logging.getLogger(self.__class__.__name__)
        
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
        def initialize(self, WelcomePage):
            self.__WelcomePage = WelcomePage
        
        def get(self):
            self.write(self.__WelcomePage)
    
    class __MainHandler(tornado.web.RequestHandler):
        def initialize(self, Function):
            self.__Function = Function

        def post(self):
            logger = logging.getLogger(self.__class__.__name__)
            
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