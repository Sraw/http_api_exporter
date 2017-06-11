"""
contains all handlers.
"""
import json
import copy
import traceback
import tornado

class WelcomeHandler(tornado.web.RequestHandler):
    """A handler used for welcome page. Can be access at route '/'"""
    def initialize(self, welcome_page, logger):
        """This function is the same as __init__"""
        self.__welcome_page = welcome_page
        self.__logger = logger

    def get(self):
        """return welcome page"""
        self.finish(self.__welcome_page)

class MainHandler(tornado.web.RequestHandler):
    """A handler used for export functions."""
    def initialize(self, function, logger):
        """This function is the same as __init__"""
        self.__function = function
        self.__logger = logger

    def post(self):
        """execute the corresponding function and return the result."""
        logger = self.__logger

        logger.info('A coming request at route "%s".' % (self.request.uri))

        json_input = self.request.body.decode('utf8')
        if json_input is not "":
            try:
                form = json.loads(json_input)
            except json.decoder.JSONDecodeError as error:
                self.set_status(400)
                error_msg = self.__get_error_msg("Body parse error, only JSON is accepted.")
                logger.error(traceback.format_exc())
                self.finish(error_msg)
                return

            if 'Input' in form:
                input_array = copy.deepcopy(form['Input'])
                del form['Input']
                args_dict = form
            else:
                input_array = list()
                args_dict = form

            if not isinstance(input_array, list):
                self.set_status(400)
                error_msg = self.__get_error_msg("Input must be a list.")
                logger.error("'Input' in the coming request is not a list.")
                self.finish(error_msg)
                return
        else:
            input_array = list()
            args_dict = dict()

        try:
            result = self.__function(*input_array, **args_dict)
        except Exception as error:
            self.set_status(500)
            error_msg = self.__get_error_msg(str(error))
            logger.error(traceback.format_exc())
            self.finish(error_msg)
            return

        if result is not None:
            if not isinstance(result, dict):
                self.set_status(400)
                error_msg = self.__get_error_msg("You are calling a function"
                                                 " whose result is not a dictionary,"
                                                 " please contact with author.")
                logger.error("The coming request is calling a function"
                             " whose result is not a dictionary.")
                self.finish(error_msg)
                return

            try:
                json_output = self.__get_success_msg(result)
            except TypeError as error:
                self.set_status(400)
                error_msg = self.__get_error_msg("The result returned from the function"
                                                 " you are calling is not jsonifiable,"
                                                 " please contact with author.")
                logger.error(traceback.format_exc())
                self.finish(error_msg)
                return
        else:
            logger.warning("The coming request is calling a function without returned value,"
                           " please make sure this is what you want.")
            json_output = self.__get_success_msg({
                "msg" : "The function you have called has no returned value,"
                        " please make sure this is what you want."
            })

        self.set_status(200)
        self.finish(json_output)

    @classmethod
    def __get_error_msg(cls, msg):
        """used to format error message."""
        msg_dict = {
            'msg' : msg
        }
        return msg_dict

    @classmethod
    def __get_success_msg(cls, result):
        """used to format success message."""
        msg_dict = result
        return msg_dict
