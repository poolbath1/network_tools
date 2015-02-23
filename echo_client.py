#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import socket
import sys


def client_socket_function(message):
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(message.encode('utf-8'))
    client_socket.shutdown(socket.SHUT_WR)

    receive_total = ""
    buffersize = 32
    finished = 0
    while not finished:
        receive = client_socket.recv(buffersize).decode('utf-8')
        if len(receive) < buffersize:
            client_socket.close()
            finished = 1
        receive_total += receive

    return receive_total

if __name__ == '__main__':
    receive = client_socket_function(sys.argv[1])
    print(receive)
