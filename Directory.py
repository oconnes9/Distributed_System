import sys
import socket
import select
import re
import threading

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 2048
PORT = 8008