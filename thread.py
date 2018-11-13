# Thread class
import socket
import time
from threading import Thread


class ServerThread(Thread):
    def __init__(self, server, conn, addr):
        Thread.__init__(self)
        self.conn= conn
        self.addr = addr
        self.server=server

    def run(self):
        print("\n\nConnection received from %s:%s\n\n" % self.addr)
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            print(data)
            # self.conn.sendall(data)
            # line = data.decode('UTF-8')
            # line = line.replace("\n", "")
            # print(line)

        # while True:
        #     print('listener here', self.client_address)
        #     time.sleep(20)


class ExchangeThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn= conn
        self.addr = addr

    def run(self):
        print("\n\nConnected to %s:%s\n\n" % self.addr)
        self.conn.send("Hello.".encode())
        while True:
            try:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                print(data)
            except socket.timeout:
                continue
            # self.conn.sendall(data)