import logging
import os

def getLogger(className, debug = False):
    logger = logging.getLogger(className)
    
    if len(logger.handlers) != 0:
        return logger
    
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s.%(funcName)s %(levelname)-5s : %(message)s',
            '%m-%d %H:%M'
        )
    
    LOG_DIR = "logs"
    LOG_FILE = 'http_api_exporter.log'
    
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
    
    logger.addHandler(hdlr)
    logger.addHandler(console)
    
    tornado_access_logger = logging.getLogger("tornado.access")
    tornado_application_logger = logging.getLogger("tornado.application")
    tornado_general_logger = logging.getLogger("tornado.general")
    
    tornado_access_logger.handlers = []
    tornado_application_logger.handlers = []
    tornado_general_logger.handlers = []
    
    tornado_access_logger.addHandler(hdlr)
    tornado_access_logger.addHandler(console)
    tornado_access_logger.setLevel(logging.DEBUG)
    
    tornado_application_logger.addHandler(hdlr)
    tornado_application_logger.addHandler(console)
    tornado_application_logger.setLevel(logging.DEBUG)
    
    tornado_general_logger.addHandler(hdlr)
    tornado_general_logger.addHandler(console)
    tornado_general_logger.setLevel(logging.DEBUG)
    
    logger.setLevel(logging.DEBUG)
    
    return logger