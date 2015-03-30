from echo_server import (parse_request, resolve_uri, RequestError,
                         response_error, response_ok)
from gevent.monkey import patch_all
from gevent.server import StreamServer


def echo(socket, address):
    buffer_size = 2048
    try:
        request = ''
        completed = False
        while not completed:
            request_part = socket.recv(buffer_size)
            if len(request_part) < buffer_size:
                completed = True
            request += request_part

        if request:
            try:
                uri = parse_request(request)
                info = resolve_uri(uri)
                response = response_ok(info)
            except RequestError as error:
                response = response_error(error)
            socket.sendall(response)
        socket.close()

    except KeyboardInterrupt:
        socket.close()


if __name__ == '__main__':
    patch_all()
    port = 8889
    server = StreamServer(('127.0.0.1', port), echo)
    print('Serving on port {}'.format(port))
    server.serve_forever()
