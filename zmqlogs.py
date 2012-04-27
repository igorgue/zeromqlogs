import logging

VERSION = '0.0.1'

class ZMQHandler(logging.Handler):
    """A Django log handler that sends the exceptions to 0MQ"""

    def __init__(self, include_html=False):
        logging.Handler.__init__(self)
        self.include_html = include_html

    def emit(self, record):
        print record

