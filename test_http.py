import echo_client as ec
import echo_server as es
import pytest


@pytest.yield_fixture(scope='module')
def start_server():
    """set up and tear down a server"""
    import threading
    target = es.server_sock
    server_thread = threading.Thread(target=target)
    server_thread.daemon = True
    server_thread.start()
    yield


def test_response_ok():
    ''' Test ok response message. '''
    response = '200 OK'
    content_type = 'text/html'
    client_request = 'GET / HTTP/1.1\r\n'
    actual = es.response_ok('text/html', client_request)
    assert response in actual
    assert content_type in actual


def test_response_error():
    ''' Test error response message. '''
    class error_test():
        def __init__(self, code, msg):
            self.code = code
            self.msg = msg

    error = error_test('404', 'Not Found')
    actual = es.response_error(error)
    assert error.code in actual
    assert error.msg in actual


def test_parse_request_uri():
    ''' Test parse request with a good request. '''
    client_request = 'GET /index.html HTTP/1.1\r\n'
    assert '/index.html' in es.parse_request(client_request)


def test_client_socket_function_ok(start_server):
    ''' Test an OK response'''
    client_request = 'GET / HTTP/1.1\r\n'
    actual = ec.client_socket_function(client_request)

    assert '200' in actual
    assert 'OK' in actual


def test_client_socket_function_405(start_server):
    ''' Test a 405 error'''
    client_request = 'PUSH /index.html HTTP/1.1\r\n'
    error = {"code": '405', "msg": 'Method Not Allowed'}
    actual = ec.client_socket_function(client_request)

    assert error['code'] in actual
    assert error['msg'] in actual


def test_client_socket_function_505(start_server):
    ''' Test a 505 error'''
    client_request = 'GET /index.html HTTP/1.0\r\n'
    error = {"code": '505', "msg": 'HTTP Version Not Supported'}
    actual = ec.client_socket_function(client_request)

    assert error['code'] in actual
    assert error['msg'] in actual

