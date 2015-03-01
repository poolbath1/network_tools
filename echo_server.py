# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import email.utils
import socket
import os
import mimetypes


BODY = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n
          </head>\n<body>\n{}</body>\n</html>
          '''
HTTP_RESPONSE_CODES = {'405': 'Method Not Allowed',
                       '505': 'HTTP Version Not Supported'}


def response_ok(*args):
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: {}'.format(args[0][0])
    body = BODY.format(args[0][1])
    content_length = 'Content-Length: {}'.format(len(body.encode('utf-8')))
    response_list = [first_line, timestamp, content_header,
                     content_length, '', body]
    return '\r\n'.join(response_list).encode('utf-8')


def response_error(error):
    first_line = 'HTTP/1.1 {} {}'.format(error.code, error.msg)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}'.format(error.code, error.msg)
    body = BODY.format(body)
    content_length = 'Content-Length: {}'.format(len(body.encode('utf-8')))
    response_list = [first_line, timestamp, content_header,
                     content_length, '', body]
    return '\r\n'.join(response_list).encode('utf-8')


def parse_request(request):
    first_line = request.splitlines()[0]
    first_line = first_line.split()

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


#def resolve_uri(uri):
#    uri = uri.lstrip("/")
#    here = os.getcwd()
#    home = 'webroot'
#    webhome = os.path.join(here, home)
#
#    actual_path = os.path.join(webhome, uri)
#
#    if os.path.isdir(actual_path):
#        body = gen_list(actual_path)
#        content_type = 'text/html'
#        info = (content_type, body)
#    elif os.path.isfile(actual_path):
#        content_type = mimetypes.guess_type(actual_path)[0]
#        try:
#            with open(actual_path, 'r') as f:
#                return (f.read(), content_type)
#        except IOError:
#            error_key = '500'
#            raise RequestError(error_key, "Internal Server Error")
#        info = (content_type, body)
#    else:
#        error_key = '404'
#        raise RequestError(error_key, 'Not Found')
#    return info

def resolve_uri(uri):
    uri = uri.lstrip("/")
    here = os.getcwd()
    home = 'webroot'
    webhome = os.path.join(here, home)
    
    actual_path = os.path.join(webhome, uri)


    # if uri is a directory, return HTML listing of that directory as body
    if os.path.isdir(actual):
        directory_html = ["<li>{}</li>".format(item) for item in os.listdir(path)]
        directory_html.insert(0, "<ul>")
        directory_html.insert(len(directory_html), "</ul>")
        return ("\n".join(directory_html), "text/html")

    # if the resources is a file, return the contents of the file

    elif os.path.isfile(path):
        file_type = guess_type(path)[0]
        try:
            with open(path, 'r') as f:
                return (f.read(), file_type)
        except IOError:
            raise IOError("Access Denied")

    # if the requested resource cannot be found, raise an appropriate error
    else:
        raise IOError("File Not Found")
    
    
def gen_list(uri):
    path_list = os.listdir(uri)
    dir_list = ""
    for i in path_list:
        dir_list += "<li>"+i+"</li>\n"
    body = "<ul>\n{}</ul>\n".format(dir_list)
    return body


def gen_text(uri):
    with open(uri, "rb") as fo:
        body = fo.read()
    return body


def server_sock():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )
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
                if len(part) < buffsize:
                    done = True
                msg = "{}{}".format(msg, part)
            out = msg

            if out:
                try:
                    uri = parse_request(out)
                    info = resolve_uri(uri)
                    response = response_ok(info)
                except RequestError as error:
                    response = response_error(error)
                conn.sendall(response)
            conn.close()

    except KeyboardInterrupt:
        server_socket.close()

if __name__ == '__main__':
    server_sock()
