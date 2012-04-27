import os

ZMQ_CONNECT_ADDRESS = os.environ.get('ZMQ_CONNECT_ADDRESS') or 'ipc:///tmp/zmqlogs'
ZMQ_BIND_ADDRESS = os.environ.get('ZMQ_BIND_ADDRESS') or 'ipc:///tmp/zmqlogs'
ZMQ_FILTER = os.environ.get('ZMQ_FILTER') or ''

