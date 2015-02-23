# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket


def response_ok(uri):
    response = []
    response.append("HTTP/1.1 200 OK")
    response.append("Content-Type = text/html; charset=utf-8")
    response.append("")
    response.append(uri)

    response = "\r\n".join(response).encode("utf-8")
    return response


def response_error(error, error_msg):
    response = []
    response.append("HTTP/1.1 {} {}".format(error, error_msg))
    response.append("")
    response = "\r\n".join(response).encode("utf-8")

    return response


def parse_request(request):
    first_line = request.splitlines()[0]
    first_line = first_line.split(" ")

    if first_line[0] == "GET":
        if first_line[2] == "HTTP/1.1":
            return response_ok(first_line[1])
        else:
            return response_error(505, "Protocol must be HTTP/1.1")
    else:
        return response_error(405, "Method not allowed")


def server_sock():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(10)

    buffsize = 4096
    out = ""
    try:
        while True:
            msg = ""
            conn, addr = server_socket.accept()
            done = False
            while not done:
                part = conn.recv(buffsize).decode('utf-8')
                print part
                if len(part) < buffsize:
                    done = True
                msg = "{}{}".format(msg, part)
            out = msg

            if out:
                response = parse_request(out)
                conn.sendall(response)
                conn.close()
    except KeyboardInterrupt:
        server_socket.close()

if __name__ == '__main__':
    server_sock()
