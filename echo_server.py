# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import email.utils
import socket


def response_ok():
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/html'
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format('200 OK')
    response_list = [first_line, timestamp, content_header, '', body, '\r\n']
    return '\r\n'.join(response_list).encode('utf-8')


def response_error(error):
    first_line = 'HTTP/1.1 {} {}'.format(error.code, error.msg)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}'.format(error.code, error.msg)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, '', body, '\r\n']
    return '\r\n'.join(response_list)


def parse_request(request):
    first_line = request.splitlines()[0]
    first_line = first_line.split(" ")

    response = error_check(first_line)

    return response


def error_check(response):
    http_response_codes = {'405': 'Method Not Allowed',
                           '505': 'HTTP Version Not Supported'}
    if response[0] != 'GET':
        error_key = '405'
        raise RequestError(error_key, http_response_codes[error_key])
    elif response[2] != 'HTTP/1.1':
        error_key = '505'
        raise RequestError(error_key, http_response_codes[error_key])
    else:
        return response[1]


class RequestError(Exception):
    """Exception raised for errors in the request."""
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "{} {}".format(self.code, self.msg)


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
                try:
                    response = parse_request(out)
                    response = response_ok()
                except RequestError as error:
                    response = response_error(error)
                conn.sendall(response)
                conn.close()

    except KeyboardInterrupt:
        server_socket.close()

if __name__ == '__main__':
    server_sock()
