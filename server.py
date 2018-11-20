import os
import socket
import time
from subprocess import check_output

from thread import ServerThread, ConnectionThread, ExchangeThread
from utils import ping


class Server:

    def __init__(self, port=10000, neighbourhood=None):
        self.name = self.gethostname()
        self.ip, self.mask = self.getnetwork()
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (self.ip, self.port)
        self.sock.bind(self.address)
        self.neighbourhood = self.getneighbourhood() if neighbourhood is None else neighbourhood
        self.connections = []
        self.leader = None

    def listen(self):

        # Start listen
        self.sock.listen(10)

        # Try connect to another server
        self.connectotoneighbourhood()

        # Wait 10 second for the leader response inside the "ExchangeThread"
        time.sleep(10)

        # If no leader, i am the leader
        if self.leader is None:
            self.leader = self.address
            print('\n\nI am the leader! %s \n\n' % str(self.leader))

        # Start thread that continuous try to connect
        # t = ConnectionThread(self)
        # t.setDaemon(True)
        # t.start()

        while True:
            print('Waiting for connection...')

            # Get conn data
            conn, addr = self.sock.accept()

            # Print current connections
            self.connections.append(addr)

            # Try connect to host
            self.connecttoneighbour((addr[0], 10000))

            print('Current connections:', self.connections)

            # After connect, pass to thread
            t = ServerThread(self, conn, addr)
            t.setDaemon(True)
            t.start()

    # Remove the closed connection from array
    def closeconnection(self, addr):
        if addr in self.connections:
            self.connections.remove(addr)

    # Get server hostname
    def gethostname(self):
        return socket.gethostname()

    # Get server ip and maks
    def getnetwork(self):
        ip = None
        mask = None

        # If windows
        if os.name == 'nt':
            out = check_output(["ipconfig"], universal_newlines=True)
            for line in out.split('\n'):
                if 'IPv4' in line:
                    ip = line.split(' : ')[1].strip()
                if 'Sub-rede' in line or 'Subnet' in line:
                    mask = line.split(' : ')[1].strip()
        # If Linux
        else:
            out = check_output(["ifconfig"], universal_newlines=True)
            for line in out.split('\n'):
                if 'inet' in line and ('Bcast' in line or 'broadcast' in line):
                    info = line.strip().split(' ')
                    ip = info[1]
                    mask = info[4]
        # If could not find address
        return [ip, mask]

    # As it has no broadcast, get neighbourhood the old and fashion way
    def getneighbourhood(self):
        base = self.ip.rsplit('.', 1)[0]
        neighbourhood = []
        for i in range(1, 254):
            host = base + '.' + str(i)
            print('Pinging to %s...' % host)
            if host != self.ip and ping(host):
                print('Success!')
                neighbourhood.append(host)

        return neighbourhood

    def connectotoneighbourhood(self):

        for host in self.neighbourhood:
            # Listening socket
            neighbour = (host, 10000)

            # If host is me
            if host == self.ip:
                print("First if")
                continue

            # If the host is already connected
            if self.checkhostinconnections(host):
                print("Second if")
                continue

            self.connecttoneighbour(neighbour)

    def checkhostinconnections(self, host):
        print('self connections:', self.connections, 'host:', host)
        for connection in self.connections:
            print("Checking connection:", connection[0], host)
            if connection[0] == host:
                return True
        return False

    def connecttoneighbour(self, neighbour):
        try:
            exchange_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            exchange_socket.settimeout(2)
            exchange_socket.connect(neighbour)
            t = ExchangeThread(self, exchange_socket, neighbour)
            print("\n\n\nCONECTOU COM SUCESSSSSSOOOOOOOOOOOO\n\n\n")
            t.setDaemon(True)
            t.start()
            return True
        except socket.error as socketerror:
            return False
