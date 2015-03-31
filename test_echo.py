# -*- coding: utf-8 -*-

from echo_client import client_socket_function


def test_HTTP_200():
    response = client_socket_function('''GET /index.html HTTP/1.1\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()

    assert response[0] == "HTTP/1.1 200 OK"


def test_HTTP_not_GET():
    response_first_line = client_socket_function('test').splitlines()[0].split()
    assert response_first_line[1] == '405'


def test_wrong_protocol():
    response_first_line = client_socket_function('''GET /index.html HTTP/1.0\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()[0].split()
    assert response_first_line[1] == '505'


def test_returns_file_content():
    response = client_socket_function('''GET /test.html HTTP/1.1\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()
    assert response[0] == "HTTP/1.1 200 OK"
    assert " ".join(response[2].split()[:3]) == "Content-Type: text/html"
    assert response[3] == "Content-Length: 24"
    assert response[4] == ""
    assert response[5] == "<div>Hello World!</div>"


def test_returns_directory_listing():
    response = client_socket_function('''GET / HTTP/1.1\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()
    assert " ".join(response[2].split()[:3]) == "Content-Type: text/html"
    assert response[3] == "Content-Length: 226"
    assert response[16] == "<li>test.html</li>"


def test_file_not_found():
    response = client_socket_function('''GET /test_wrong.html HTTP/1.1\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()
    response_first_line = response[0].split()

    assert response_first_line[1] == '404'


def test_file_above_root():
    response = client_socket_function('''GET ../echo_client.py HTTP/1.1\r\n
            Host: joelstanner.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()
    response_first_line = response[0].split()

    assert response_first_line[1] == "403"


def test_file_is_binary_like_a_jpeg():
    response = client_socket_function('''GET /images/JPEG_example.jpg HTTP/1.1\r\n
            Host: joelstanner.com\r\n
            ''').splitlines()
    assert response[0] == "HTTP/1.1 200 OK"
    assert " ".join(response[2].split()[:3]) == "Content-Type: image/jpeg"
    assert response[3] == "Content-Length: 15138"
