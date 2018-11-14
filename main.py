import socket

from server import Server
from thread import ExchangeThread


# def init():
#     print('aqui')
#
    # myList = []


if __name__ == '__main__':

    neighbourhood = ['177.44.242.8', '177.44.242.20', '177.44.242.130']

    serverinstance = Server(port=8000, neighbourhood=neighbourhood)

    # Define neighbour hosts
    # neighbourhood = ['192.168.1.1', '192.168.1.5','192.168.1.50']

    print("Started server on %s:%s with neighbourhood %s" % (serverinstance.ip, serverinstance.port, serverinstance.neighbourhood))

    # # Server socket
    # server_address = (server.ip, 10000)
    # # server_address = ('0.0.0.0', randint(2000,9999))
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind(server_address)
    # server_socket.listen(10)

    hostscount = 0

    for host in serverinstance.neighbourhood:
        try:
            # Listening socket
            neighbour = (host, 10000)
            exchange_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            exchange_socket.settimeout(2)
            print('Trying to connect to %s port %s' % neighbour)
            exchange_socket.connect(neighbour)
            t = ExchangeThread(serverinstance, exchange_socket, neighbour)
            t.setDaemon(True)
            t.start()
            hostscount += 1
        except socket.error as socketerror:
            continue

    serverinstance.listen(True if hostscount == 0 else False)

    # while True:
    #     a = 1
    #     server.start()
    # while True:
    #     print('waiting for connection...')
    #     connection, client_address = server_socket.accept()
    #
    #     t = ConnectionThread(connection, client_address)
    #     # t = threading.Thread(target=listener, args=(connection, client_address,))
    #     t.setDaemon(True)
    #     t.start()
