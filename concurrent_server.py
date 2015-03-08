from echo_server import (parse_request, resolve_uri,
                         response_error, RequestError)
from gevent.monkey import patch_all
from gevent.server import StreamServer


def echo(socket, address):
    buffsize = 2048
    try:
        message = ""
        while True:
            data = socket.recv(buffsize)
            if data:
                message += data
            else:
                try:
                    uri = parse_request(message)
                    response = resolve_uri(uri)
                except RequestError as error:
                    response = response_error(error)
                socket.sendall(response)
                socket.close()
                break
    except:
        socket.close()
        raise


if __name__ == '__main__':
    patch_all()
    server = StreamServer(('127.0.0.1', 8889), echo)
    server.serve_forever()
