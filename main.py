from server import Server

if __name__ == '__main__':
    # Define neighbour hosts
    neighbourhood = ['10.3.6.18', '10.3.6.19', '10.3.6.20']

    # Create server
    serverinstance = Server(port=10000, neighbourhood=neighbourhood)

    # Print info
    print("Started server on %s:%s" % (serverinstance.ip, serverinstance.port))

    # Start listen
    serverinstance.listen()
