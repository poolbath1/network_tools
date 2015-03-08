#!/usr/bin/env python
import socket
import sys


def client_socket_function(message):
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 8889))
    client_socket.sendall(message.encode('utf-8'))
    client_socket.shutdown(socket.SHUT_WR)

    receive_total = ""
    buffersize = 2048
    finished = False
    while not finished:
        receive = client_socket.recv(buffersize).decode('utf-8')
        if len(receive) < buffersize:
            finished = True
            client_socket.close()
        receive_total += receive
    return receive_total

if __name__ == '__main__':
    receive = client_socket_function(sys.argv[1])
