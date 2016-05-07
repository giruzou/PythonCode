from __future__ import print_function
import socket
from contextlib import closing
import time

def main():
    host = '127.0.0.1'
    port = 4000
    bufsize = 4096
    for i in range(100):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect((host, port))
            sendmsg='Hello'+str(i)
            print(sendmsg)
            sock.send(sendmsg)
            print(sock.recv(bufsize))
            sock.send('hoge')
    return

if __name__ == '__main__':
  main()