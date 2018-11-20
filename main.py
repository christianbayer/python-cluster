import socket

from server import Server
from thread import ExchangeThread

if __name__ == '__main__':

    # Define neighbour hosts
    neighbourhood = ['177.44.242.8', '177.44.242.20', '177.44.242.130', '192.168.56.1', '192.168.56.2']

    # Create server
    serverinstance = Server(port=10000, neighbourhood=neighbourhood)

    # Print info
    print("Started server on %s:%s" % (serverinstance.ip, serverinstance.port))

    # Hosts control
    # hostscount = 0

    # for host in serverinstance.neighbourhood:
    #     try:
    #         # Listening socket
    #         neighbour = (host, 10000)
    #         exchange_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         exchange_socket.settimeout(2)
    #         print('Trying to connect to %s port %s' % neighbour)
    #         exchange_socket.connect(neighbour)
    #         t = ExchangeThread(serverinstance, exchange_socket, neighbour)
    #         t.setDaemon(True)
    #         t.start()
    #         hostscount += 1
    #     except socket.error as socketerror:
    #         continue

    serverinstance.listen()
