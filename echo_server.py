from __future__ import print_function
import socket
import os


s = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
print ('Socket created')


def socketpair():
    done = False
    buffer_size = 16
    response = ''
    try:
        parent, child = s
        pid = os.fork()
        print('PID = ', pid)
        if pid:
            parent.close()
            child.send("Hello parent, do you hear me?")
            while not done:
                child_message = child.recv(buffer_size)
                if len(child_message) < buffer_size:
                    done = True
                response += child_message
            print("parent sent '%s'" % response)
        else:
            child.close()
            parent.send("Yes child, I hear you.")
            while not done:
                parent_message = parent.recv(buffer_size)
                if len(parent_message) < buffer_size:
                    done = True
                response += parent_message
            print("child sent '%s'" % response)
    except:
        raise

if __name__ == '__main__':
    socketpair()
