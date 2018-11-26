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

                elif data == 'whoslider':
                    print("Server %s:%s asks who is the leader!" % self.addr)
                    self.conn.send(str(self.server.leader).encode())

                elif 'newleader' in data:
                    print("XABLAU New leader election: ", data)

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

        # Ask to server who is the leader
        self.conn.send("whoslider".encode())

        data = self.conn.recv(1024).decode()

        self.server.leader = eval(data)
        print("New leader: %s" % str(self.server.leader))

        while True:

            try:
                data = self.conn.recv(1024).decode()

                if 'newleader' in data:
                    self.server.leader = eval(data)
                    print("New leader elected: %s " % data)

                else:
                    break

            except socket.timeout:
                continue

            except socket.error as e:
                if e.errno == errno.ECONNRESET:

                    print('MAIN SERVER DISCONNECTED:', self.addr)

                    t = ElectionThread(self.server, self.addr)
                    t.setDaemon(True)
                    t.start()

                    break
                else:
                    raise

            # Wait 1 second and go again
            time.sleep(1)


class ElectionThread(Thread):
    def __init__(self, server, addr):
        Thread.__init__(self)
        self.server = server
        self.addr = addr

    def run(self):
        # Não passar apenas o self.addr, precisa da conexão
        self.server.closeconnection(self.addr)
        self.server.makeelection()
