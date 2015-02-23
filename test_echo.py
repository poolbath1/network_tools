# -*- coding: utf-8 -*-

import pytest
from echo_client import client_socket_function
import echo_server


def test_HTTP_200():
    response_first_line = client_socket_function('''GET /index.html HTTP/1.1\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()[0].split()

    assert response_first_line[1] == '200' and response_first_line[2] == 'OK'


def test_HTTP_not_GET():
    response_first_line = client_socket_function('test').splitlines()[0].split()
    assert response_first_line[1] == '405'


def test_wrong_protocol():
    response_first_line = client_socket_function('''GET /index.html HTTP/1.0\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()[0].split()
    assert response_first_line[1] == '505'
