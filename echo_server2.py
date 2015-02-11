import socket
import os


s = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
print 'Socket created'


def socketpair():
    done = False
    buffer_size = 16
    response = None
    try:
        parent, child = s
        pid = os.fork()
        if pid:
            parent.close()
            child.send("Hello parent, do you hear me?")
            while not done:
                message = child.recv(buffer_size)
                if len(message) < buffer_size:
                    done = True
                response += message
                print "child sent '%s'" % response
        else:
            child.close()
            
            message = parent.recv(buffer_size)
            print "parent sent '%s'" % message
            parent.send("Yes child, I hear you.")
    except:
        print('BROKEN')

if __name__ == '__main__':
    socketpair()
