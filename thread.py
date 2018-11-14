# Thread class
import errno
import socket
import time
from threading import Thread


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

        # while True:
        #     print('listener here', self.client_address)
        #     time.sleep(20)


# class VerifyConnections(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#         # self._stop_event = threading.Event()
#         self.connections = []
#         self.sleep = 5
#
#     # def stop(self):
#     # self._stop_event.set()
#
#     # def stopped(self):
#     #     return self._stop_event.is_set()
#
#     def run(self):
#         while True:
#             print('da thread:', self.connections)
#             for connection in self.connections:
#                 host = connection[1][0]
#                 if not ping(host):
#                     print('Testing connection to %s... Failed!!!' % host)
#                     time.sleep(2)
#                     if not ping(host):
#                         raise Exception("Host disconnected: %s" % host)
#                 print('Testing connection to %s... Success!' % host)
#             time.sleep(self.sleep)


# Client Server
class ExchangeThread(Thread):
    def __init__(self, server,conn, addr):
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
