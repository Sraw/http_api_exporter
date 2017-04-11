import json
import tornado
import traceback

class WelcomeHandler(tornado.web.RequestHandler):
    def initialize(self, WelcomePage, logger):
        self.__WelcomePage = WelcomePage
        self.__logger = logger
    
    def get(self):
        self.write(self.__WelcomePage)

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, Function, logger):
        self.__Function = Function
        self.__logger = logger

    def post(self):
        logger = self.__logger
        
        logger.info('A coming request at route "%s".' % (self.request.uri))
        
        try:
            form = json.loads(self.request.body.decode('utf8'))
        except Exception as e:
            self.set_status(400)
            ErrorMsg = self.__getErrorMsg("Body parse error, only JSON is accepted.")
            logger.error(e)
            self.finish(ErrorMsg)
        
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
                ErrorMsg = self.__getErrorMsg("Input must be a list.")
                self.finish(ErrorMsg)
            
            result = self.__Function(*Input, **ArgsDict)
            
            if not isinstance(result, dict):
                self.set_status(400)
                ErrorMsg = self.__getErrorMsg("The result of function must be a dict.")
                self.finish(ErrorMsg)
            
            JsonOutput = self.__getSuccessMsg(result)
            self.set_status(200)
            self.finish(JsonOutput)
        except KeyError as e:
            self.set_status(400)
            ErrorMsg = self.__getErrorMsg('{0} is not a available function.'.format(e))
            logger.error(e)
            self.finish(ErrorMsg)
        except Exception as e:
            self.set_status(500)
            ErrorMsg = self.__getErrorMsg(traceback.format_exc())
            logger.error(e)
            self.finish(ErrorMsg)

    def __getErrorMsg(self, msg):
        msgDict = {
            'msg' : msg
        }
        return msgDict

    def __getSuccessMsg(self, result):
        msgDict = result
        return msgDict