import socket


def response_ok():
    pass

def server_sock():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(10)

    buffsize = 4096
    out = ""
    while True:
        msg = ""
        conn, addr = server_socket.accept()
        done = False
        while not done:
            part = conn.recv(buffsize)
            print part
            if len(part) < buffsize:
                done = True
            msg = "{}{}".format(msg, part)
        out = msg
        conn.sendall(out)
        conn.close()

if __name__ == '__main__':
    server_sock()
