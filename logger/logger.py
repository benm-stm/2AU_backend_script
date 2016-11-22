import logging

class logger:

    def __init__(self, log_file, log_lvl, log_format):
        self.log_lvl = logging.DEBUG
        self.log_file = log_file
        self.log_format = log_format

    def create_logger(self):
        logger = logging.getLogger("2AU")
        hdlr = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(self.log_format)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.setLevel(self.log_lvl)
        return logger

# usage code
#logger.debug('debug message')
#logger.info('info message')
#logger.warn('warn message')
#logger.error('error message')
#logger.critical('critical message')
