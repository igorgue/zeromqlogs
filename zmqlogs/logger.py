import datetime
import json
import logging
import traceback
import zmq

from .config import ZMQ_BIND_ADDRESS

VERSION = '0.0.1'

class ZMQHandlerError(Exception):
    pass

class ZMQHandler(logging.Handler):
    """A Django log handler that sends the exceptions to 0MQ"""

    # ZMQ socket
    socket = None
    context = None

    def __init__(self, include_html=False):
        logging.Handler.__init__(self)

        self.include_html = include_html
        self.init_zmq_socket()

    def init_zmq_socket(self):
        """Initialize a zmq connection

        Returns a socket"""
        self.context = zmq.Context()

        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(ZMQ_BIND_ADDRESS)

        self.socket

    def collect_message(self, record):
        """Collects message from record

        Returns a dictionary"""
        data = {}

        data['level'] = record.levelname

        data['datetime'] = datetime.datetime.now().isoformat()

        if hasattr(record, 'request'):
            data['ip_address'] = record.request.META.get('REMOTE_ADDR')
            data['http_host'] = record.request.META.get('HTTP_HOST')

        data['message'] = record.getMessage()

        if record.exc_info:
            data['stack_trace'] = '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            data['stack_trace'] = 'No stack trace available'

        return data

    def format_message(self, message):
        """Formats the message to send via 0MQ

        Return a JSON string"""
        return json.dumps(message)

    def send_message(self, formatted_message):
        """Sends the message via ZMQ

        Return true or false depending on error or not"""
        try:
            self.socket.send('{0}\n'.format(formatted_message))
        except Exception:
            # Gotta catch them' all
            return False

        # Message was sent successfully
        return True

    def emit(self, record):
        message = self.collect_message(record)
        formatted_message = self.format_message(message)

        message_was_sent = self.send_message(formatted_message)

        if not message_was_sent:
            error_message = 'Log could not be sent: {0}'.format(message)
            raise ZMQHandlerError(error_message)

