from echo_server import (parse_request)
from gevent.monkey import patch_all
from gevent.server import StreamServer


def echo(socket, address):
    buffer_size = 2048
    try:
        completed = False
        while not completed:
            request = ''
            request_part = socket.recv(buffer_size).decode('utf-8')
            request += request_part
            while len(request_part) >= buffer_size:
                request_part = socket.recv(buffer_size).decode('utf-8')
                request += request_part

            completed = True
            if request:
                response = parse_request(request)
                socket.sendall(response)
            socket.close()

    except KeyboardInterrupt:
        socket.close()


if __name__ == '__main__':
    patch_all()
    server = StreamServer(('127.0.0.1', 8889), echo)
    server.serve_forever()
