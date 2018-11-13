import socket

from Server import Server
from thread import ExchangeThread

neighbourhood = ['192.168.1.1', '192.168.1.5','192.168.1.50']

server = Server(port=9000,neighbourhood=neighbourhood)

print(server.name)
print(server.ip)
print(server.neighbourhood)

# # Server socket
# server_address = (server.ip, 10000)
# # server_address = ('0.0.0.0', randint(2000,9999))
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(server_address)
# server_socket.listen(10)

for host in server.neighbourhood:
    try:
        # Listening socket
        neighbour = (host, 10000)
        exchange_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        exchange_socket.settimeout(2)
        print('Trying to connect to %s port %s' % neighbour)
        exchange_socket.connect(neighbour)
        print('a')
        t = ExchangeThread(exchange_socket, neighbour)
        t.setDaemon(True)
        t.start()

    except socket.error as socketerror:
        print("Failed to connect: ", socketerror)
        continue

server.listen()
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
