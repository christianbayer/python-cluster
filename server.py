import os
import socket
from subprocess import check_output

from thread import ServerThread
from utils import ping


class Server:

    def __init__(self, port=10000, neighbourhood=None):
        self.name = self.gethostname()
        self.ip, self.mask = self.getnetwork()
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.neighbourhood = self.getneighbourhood() if neighbourhood is None else neighbourhood
        self.connections = []
        self.leader = None

    def listen(self, isleader):

        # Start listen
        self.sock.listen(10)

        if isleader:
            self.leader = (self.ip, self.port)
            print('\n\nI am the leader! %s \n\n' % str(self.leader))

        while True:
            print('Waiting for connection...')

            # Get conn data
            conn, addr = self.sock.accept()

            # Print current connections
            self.connections.append(addr)
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
                if 'inet addr' in line and 'Bcast' in line:
                    ip = line.split(':')[1].strip().split(' ').strip()
                    mask = line.split('Mask:')[1].strip()
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
