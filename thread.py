import errno
import socket
import time
from threading import Thread

from utils import ping


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


# Listen thread
class TestThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        while True:
            print("Testing connections received...", self.server.connectionsReceived)
            for connection in self.server.connectionsReceived:

                # Get socket connection
                conn = connection[0]

                try:

                    # Ask if it still wake
                    conn.send("areyouwake".encode())

                    # Wait for response
                    data = conn.recv(1024).decode()

                except socket.error as e:
                    if e.errno != errno.EPIPE:
                        # Not a broken pipe
                        raise

                    # Close connection
                    self.server.closeconnection(connection[1])

                    continue

                # print("Pinging to %s: %s" % (ip, ping(ip)))
                #
                # if not ping(ip):
                #
                #     # If the leader is not responding
                #     if connection[1] == self.server.leader:
                #         # Start a new election
                #         t = ElectionThread(self.server)
                #         t.setDaemon(True)
                #         t.start()
                #
                #     # Else, just remove from connections array
                #     else:
                #         self.server.closeconnection(ip)

            # Before test again, wait 5 secons
            time.sleep(5)


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

                elif 'areyouwake' in data:
                    print("Someone asked if i'm awake.")
                    self.conn.send("yes".encode())

                else:
                    break

            except socket.timeout:
                continue

            except socket.error as e:
                if e.errno == errno.ECONNRESET:

                    print('MAIN SERVER DISCONNECTED:', self.addr)

                    t = ElectionThread(self.server)
                    t.setDaemon(True)
                    t.start()

                    break
                else:
                    raise

            # Wait 1 second and go again
            time.sleep(1)


class ElectionThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        # Não passar apenas o self.addr, precisa da conexão
        self.server.closeconnection(self.server.leader)
        self.server.makeelection()
