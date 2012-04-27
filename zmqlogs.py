import datetime
import json
import logging
import traceback
import zmq

VERSION = '0.0.1'

class ZMQHandlerError(Exception):
    pass

class ZMQHandler(logging.Handler):
    """A Django log handler that sends the exceptions to 0MQ"""

    # ZMQ socket
    socket = None

    def __init__(self, include_html=False):
        logging.Handler.__init__(self)
        self.include_html = include_html

        # Get socket instance
        if self.socket is None:
            self.socket = self.init_zmq_socket()

    def init_zmq_socket(self):
        """Initialize a zmq connection

        Returns a socket"""
        context = zmq.Context()

        socket = context.socket(zmq.PUB)
        socket.bind('tcp://*:5556')

        return socket

    def collect_message(self, record):
        """Collects message from record

        Returns a dictionary"""
        data = {}

        data['level'] = record.levelname

        data['datetime'] = datetime.datetime.now().isoformat()

        data['ip_address'] = record.request.META.get('REMOTE_ADDR')
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
        """Sends the message via ZMQ"""
        self.socket.send(formatted_message)

        # Message was sent successfully
        return True

    def emit(self, record):
        message = self.collect_message(record)
        formatted_message = self.format_message(message)

        message_was_sent = self.send_message(formatted_message)

        if not message_was_sent:
            error_message = 'Log could not be sent: {0}'.format(message)
            raise ZMQHandlerError(error_message)

