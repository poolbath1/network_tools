import socket


def server_sock():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(10)

    conn, addr = server_socket.accept()
    buffsize = 4096
    msg = ""
    done = False
    while not done:
        part = conn.recv(buffsize)
        if len(part) < buffsize:
            done = True
        msg = "{}{}".format(msg, part)
    out = "{}{}".format("I heard: ", msg)
    conn.sendall(out)


if __name__ == '__main__':
    server_sock()
