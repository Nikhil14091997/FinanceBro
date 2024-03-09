import logging

class LoggerSetup:
    '''
    Class to handle the logging
    @methods:
        - setup_logger: setup the logger
        - add_formatter: add formatter to the logger
    '''
    def __init__(self, logger_name: str, log_level: int = logging.INFO):
        self.logger_name = logger_name
        self.log_level = log_level
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)

        # Add a StreamHandler if no handlers are present
        if not logger.handlers:
            stream_handler = logging.StreamHandler()
            logger.addHandler(stream_handler)

        return logger

    def add_formatter(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)
