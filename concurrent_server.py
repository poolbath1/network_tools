from echo_server import (parse_request, resolve_uri, RequestError,
                         response_error)
from gevent.monkey import patch_all
from gevent.server import StreamServer


def echo(socket, address):
    buffer_size = 2048
    try:
        message = ""
        while True:
            data = socket.recv(buffer_size)
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

    except KeyboardInterrupt:
        socket.close()


if __name__ == '__main__':
    patch_all()
    port = 8889
    server = StreamServer(('127.0.0.1', port), echo)
    print('Serving on port {}'.format(port))
    server.serve_forever()
