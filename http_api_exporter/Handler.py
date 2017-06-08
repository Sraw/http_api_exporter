import json
import copy
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
        
        if self.request.body is not None:
            try:
                form = json.loads(self.request.body.decode('utf8'))
            except Exception as e:
                self.set_status(400)
                ErrorMsg = self.__getErrorMsg("Body parse error, only JSON is accepted.")
                logger.error(traceback.format_exc())
                self.finish(ErrorMsg)
                return
            
            if 'Input' in form:
                Input = copy.deepcopy(form['Input'])
                del form['Input']
                ArgsDict = form
            else:
                Input = list()
                ArgsDict = form
                
            if not isinstance(Input, list):
                self.set_status(400)
                ErrorMsg = self.__getErrorMsg("Input must be a list.")
                logger.error("'Input' in the coming request is not a list.")
                self.finish(ErrorMsg)
                return
        else:
            Input = list()
            ArgsDict = dict()
        
        try:    
            result = self.__Function(*Input, **ArgsDict)
        except Exception as e:
            self.set_status(500)
            ErrorMsg = self.__getErrorMsg(str(e))
            logger.error(traceback.format_exc())
            self.finish(ErrorMsg)
            return
        
        if result is not None:
            if not isinstance(result, dict):
                self.set_status(400)
                ErrorMsg = self.__getErrorMsg("You are calling a function whose result is not a dictionary, please contact with author.")
                logger.error("The coming request is calling a function whose result is not a dictionary.")
                self.finish(ErrorMsg)
                return
        
            try:
                JsonOutput = self.__getSuccessMsg(result)
            except TypeError as e:
                self.set_status(400)
                ErrorMsg = self.__getErrorMsg("The result returned from the function you are calling is not jsonifiable, please contact with author.")
                logger.error(traceback.format_exc())
                self.finish(ErrorMsg)
                return
        else:
            logger.warning("The coming request is calling a function without returned value, please make sure this is what you want.")
            JsonOutput = self.__getSuccessMsg({
                "msg" : "The function you have called has no returned value, please make sure this is what you want."
            })
        
        self.set_status(200)
        self.finish(JsonOutput)

    def __getErrorMsg(self, msg):
        msgDict = {
            'msg' : msg
        }
        return msgDict

    def __getSuccessMsg(self, result):
        msgDict = result
        return msgDict