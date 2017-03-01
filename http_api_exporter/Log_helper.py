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
    tornadologger = logging.getLogger("tornado.access")
    tornadologger.addHandler(hdlr)
    tornadologger.addHandler(console)
    tornadologger.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    
    return logger