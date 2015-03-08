from __future__ import print_function
import email.utils
import socket
import os
import mimetypes


BODY = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8"></head>\n<body>\n{}\n</body>\n</html>'

HTTP_RESPONSE_CODES = {'403': 'Forbidden',
                       '404': 'Content Not Found',
                       '405': 'Method Not Allowed',
                       '505': 'HTTP Version Not Supported'}

ROOT_DIR = os.path.join(os.getcwd(), "webroot")


def response_ok(msg, resolved):
    """Return a properly formed HTTP OK 200 response"""
    first_line = u'HTTP/1.1 200 OK'
    timestamp = u'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = u'Content-Type: {}'.format(msg)
    content_length = u'Content-Length: {}'.format(len(resolved))
    response_list = [first_line, timestamp, content_header,
                     content_length, '', resolved]
    return '\r\n'.join(response_list).encode('utf-8')


def response_error(error):
    """Return HTTP error with a proper code and explaination"""
    first_line = 'HTTP/1.1 {} {}'.format(error.code, error.msg)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}'.format(error.code, error.msg)
    content_length = 'Content-Length: {}'.format(len(body.encode('utf-8')))
    response_list = [first_line, timestamp, content_header,
                     content_length, '', body]
    return '\r\n'.join(response_list).encode('utf-8')


def parse_request(request):
    """check the HTTP header for correctness"""
    first_line = request.splitlines()[0]
    first_line = first_line.split()
    print("first line = {}".format(first_line))
    response = error_check(first_line)

    return response


def error_check(response):
    """Return proper error code and message if there is an error"""
    if response[0] != 'GET':
        error_key = '405'
        raise RequestError(error_key, HTTP_RESPONSE_CODES[error_key])
    elif response[2] != 'HTTP/1.1':
        error_key = '505'
        raise RequestError(error_key, HTTP_RESPONSE_CODES[error_key])
    else:
        return response[1]


class RequestError(Exception):
    """Exception raised for errors in the request."""
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "{} {}".format(self.code, self.msg)


def resolve_uri(uri):
    """Return a file if it's a file, return a directory listing if it's a dir"""
    path = "{}{}".format(ROOT_DIR, uri)
    if ".." in path:
        error_key = '403'
        raise RequestError(error_key, HTTP_RESPONSE_CODES[error_key])
    elif os.path.isfile(path):
        file_content = read_file(path)
        guess = mimetypes.guess_type(uri)[0]
        response = response_ok(guess, file_content)
        return response
    elif os.path.isdir(os.path.abspath(path)):
        files = gen_list(path)
        response = response_ok('text/html', files)
        return response
    else:
        error_key = '404'
        raise RequestError(error_key, HTTP_RESPONSE_CODES[error_key])


def read_file(uri):
    """Read the contents of a file"""
    try:
        with open(uri, "rb") as file:
            body = file.read()
        return body
    except IOError:
        error_key = '404'
        raise RequestError(error_key, HTTP_RESPONSE_CODES[error_key])


def gen_list(uri):
    """Create a HTML directory listing"""
    path_list = os.listdir(uri)
    dir_list = ""
    for item in path_list:
        dir_list += "<li>{}</li>\n".format(item)
    body = BODY.format("<ul>\n{}</ul>\n".format(dir_list))
    return body.encode('utf-8')


def server_sock():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )
    response = None
    port = 8889
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(10)
    print("Now serving on port", port)

    buffsize = 4096
    out = ""
    try:
        while True:
            msg = ""
            conn, addr = server_socket.accept()
            done = False
            while not done:
                part = conn.recv(buffsize)
                if len(part) < buffsize:
                    done = True
                msg = "{}{}".format(msg, part)
            out = msg

            if out:
                try:
                    uri = parse_request(out)
                    response = resolve_uri(uri)
                except RequestError as error:
                    response = response_error(error)
                conn.sendall(response)
            conn.close()

    except KeyboardInterrupt:
        server_socket.close()

if __name__ == '__main__':
    server_sock()
