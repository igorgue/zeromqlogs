import zmq

from .config import ZMQ_CONNECT_ADDRESS, ZMQ_FILTER

class ZMQLogsServerError(Exception):
    pass

class ZMQLogsServer(object):

    # ZMQ socket
    socket = None
    context = None
    log_filter = None

    def __init__(self):
        # Get socket instance
        self.init_zmq_socket()

    def init_zmq_socket(self):
        """Initialize a zmq connection

        Returns a socket"""
        #  Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.logs_filter = ZMQ_FILTER

        self.socket.connect(ZMQ_CONNECT_ADDRESS)

        self.socket.setsockopt(zmq.SUBSCRIBE, self.logs_filter)

    def save_to_filesystem(self, message, filename=None):
        if not filename:
            filename = '/tmp/zmqlogs.log'

        with open(filename, 'a+') as zmqlog_file:
            zmqlog_file.write(message)

    #def save_to_redis(self, message, redis_client=None):
        #pass

    def just_print(self, message):
        print message

    def run(self):
        # Event loop
        while True:
            message = self.socket.recv()

            self.save_to_filesystem(message)
