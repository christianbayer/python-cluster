import socket
import sys
import time
import Queue
import random
import threading

if __name__ == '__main__':

    # Listen out for the leader!
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', 10000)
    server_sock.bind(server_address)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_address = ('192.168.1.255', 10000)

    messages = Queue.Queue()


    def listener():
        while True:
            data, address = server_sock.recvfrom(4096)
            messages.put((data, address))


    t = threading.Thread(target=listener)
    t.setDaemon(True)
    t.start()

    ident = random.randint(0, 1000)
    print(ident)

    start_time = time.time()

    state = "follower"
    leader = None


    def send_message(msg):
        message = "%d-%s" % (ident, msg)
        sent = sock.sendto(message, server_address)


    def get_message(msg):
        return msg.split('-')


    while True:
        time.sleep(1)
        try:
            data, address = messages.get(block=False)
        except Queue.Empty:
            data = None
        else:
            message = get_message(data)
            denti = int(message[0])
            action = message[1]

            if denti == ident:
                # skip our own messages
                pass
            elif denti < ident and action == "elect":
                print("Recieved elect from lower ID rejecting")
                print("starting new election")
                print("broadcasting my candidadacy")
                send_message("reject")
                state = "candidate"
                send_message("elect")
                start_time = time.time()
            elif denti > ident and action == "reject":
                print("Rejected as leader by higher ID")
                print("returning to follower state")
                state = "follower"
                start_time = time.time()
            elif action == "victory":
                print("A new leader has appeared")
                print("returning to follower state")
                state = "follower"
                leader = denti
                start_time = time.time()
            elif action == "heartbeat":
                print("leader is")
                print(denti)
                leader = denti
                start_time = time.time()

        if time.time() - start_time > 2:
            if state == "leader":
                send_message("heartbeat")
                start_time = time.time()

        if time.time() - start_time > 4:
            if state == "follower":
                print("timed out waiting for a leader")
                print("broadcasting my candidadacy")
                state = "candidate"
                send_message("elect")
                start_time = time.time()
            elif state == "candidate":
                print("Timed out waiting for a response from a higher ident")
                print("claiming victory")
                state = "leader"
                send_message("victory")
