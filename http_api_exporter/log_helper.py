"""
designed to easily configure logging.logger,
and consist the performance of tornado's loggers.
"""
import logging
import os

def get_logger(class_name, debug=False):
    """
    Configure logger before return if it has no handlers.
    Consist the performance of tornado's loggers.
    """
    logger = logging.getLogger(class_name)

    if not logging.getLogger().isEnabledFor(logging.CRITICAL) or not logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s.%(funcName)s %(levelname)-5s : %(message)s',
        '%m-%d %H:%M'
    )

    log_dir = "logs"
    log_file = 'http_api_exporter.log'

    log_file = os.path.join(log_dir, log_file)

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    hdlr = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when="D",
        interval=1,
        backupCount=7
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
