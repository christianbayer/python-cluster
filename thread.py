import errno
import socket
import time
from threading import Thread


class ConnectionThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        while True:
            self.server.connectotoneighbourhood()
            # Wait 10 seconds and try connect again
            time.sleep(10)


# Server
class ServerThread(Thread):
    def __init__(self, server, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.server = server

    def run(self):
        print("\n\nConnection received from %s:%s\n\n" % self.addr)
        while True:
            try:
                data = self.conn.recv(1024).decode()

                if not data:
                    break

                print('Data received:', data)

                if data == 'Hello':
                    print("Server %s:%s send Hello!" % self.addr)

                elif data == 'whoslider':
                    print("Server %s:%s asks who is the leader!" % self.addr)
                    self.conn.send(str(self.server.leader).encode())

            except socket.timeout as e:
                continue

            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    self.server.closeconnection(self.addr)
                    print('Server disconnected:', self.addr)
                    break
                else:
                    raise


# Client Server
class ExchangeThread(Thread):
    def __init__(self, server, conn, addr):
        Thread.__init__(self)
        self.server = server
        self.conn = conn
        self.addr = addr

    def run(self):

        print("\n\nConnected to %s:%s\n\n" % self.addr)

        # Increase timeout
        self.conn.settimeout(10)

        # Send hello message to server
        self.conn.send("Hello".encode())

        time.sleep(1)

        # Ask to server who is the leader
        self.conn.send("whoslider".encode())

        data = self.conn.recv(1024).decode()
        print('leader response:', data)

        self.server.leader = eval(data)
        print(self.server.leader)

        while True:

            try:
                data = self.conn.recv(1024).decode()

                if data == 'Hello':
                    print("Server %s:%s send Hello!")

                else:
                    break

            except socket.timeout:
                continue

            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    self.server.closeconnection(self.addr)

                    # disparar uma nova eleição

                    print('MAIN SERVER DISCONNECTED:', self.addr)
                    break
                else:
                    raise

            # Wait 1 second and go again
            time.sleep(1)
