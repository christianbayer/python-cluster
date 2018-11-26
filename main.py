from server import Server

if __name__ == '__main__':
    # Define neighbour hosts
    neighbourhood = ['192.168.137.160', '192.168.137.13', '192.168.137.1', '192.168.56.2', '192.168.56.1', '177.44.242.130']

    # Create server
    serverinstance = Server(port=10000, neighbourhood=neighbourhood)

    # Print info
    print("Started server on %s:%s" % (serverinstance.ip, serverinstance.port))

    # Start listen
    serverinstance.listen()
