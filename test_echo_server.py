# -*- coding: utf-8 -*-
from echo_client import client_socket_function
from echo_server import server_socket_function
import pytest


@pytest.yield_fixture(scope='module')
def start_server():
    """set up and tear down a server"""
    import threading
    target = server_socket_function
    server_thread = threading.Thread(target=target)
    server_thread.daemon = True
    server_thread.start()
    yield


def test_client_socket_function_short(start_server):
    ''' 16 byte message. Short response'''
    message = "Can you hear me?"
    receive = client_socket_function(message)
    assert receive == message


def test_client_socket_function_long(start_server):
    ''' 74 byte message. '''
    message = "Can you hear me? I am waiting for you to respond. Come on, where are you?!"
    receive = client_socket_function(message)
    assert receive == message


def test_client_socket_function_unicode(start_server):
    ''' Unicode. '''
    message = u"éclaire"
    receive = client_socket_function(message)
    assert receive == message
