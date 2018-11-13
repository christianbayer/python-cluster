import errno
import socket
import os
import time
from subprocess import check_output

from thread import ServerThread


class Server:

    def __init__(self, port=10000, neighbourhood=None):
        self.name = self.gethostname()
        self.ip, self.mask = self.getnetwork()
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(10)
        self.neighbourhood = self.neighbourhood if neighbourhood is None else neighbourhood
        self.connections = []
        self.leader = None

    def listen(self):
        while True:
            print('Waiting for connection...')
            conn, addr = self.sock.accept()
            self.connections.append((conn, addr))

            # After connect, pass to thread
            t = ServerThread(self, conn, addr)
            t.setDaemon(True)
            t.start()

    def start(self):
        while True:
            try:
                self.sock.send(bytes('hello', 'UTF-8'))
            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    print('disconect?:', e)
                else:
                    raise
            time.sleep(1)

    def gethostname(self):
        return socket.gethostname()

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

    def getneighbourhood(self):
        base = self.ip.rsplit('.', 1)[0]
        neighbourhood = []
        for i in range(1, 254):
            host = base + '.' + str(i)
            print('Ping to {}...'.format(host))
            if host != self.ip and ping(host):
                print('Success!')
                neighbourhood.append(host)

        return neighbourhood


def ping(ip):
    import os
    from subprocess import DEVNULL, STDOUT, call

    # If windows
    if os.name == 'nt':
        command = ['ping', '-n', '1', '-w', '10', ip]
    # If Linux
    else:
        command = ['ping', '-c', '1', '-W', '10', ip]

    return call(command, stdout=DEVNULL, stderr=STDOUT) == 0
