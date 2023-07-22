import socket
import sys

import select
import errno
import time


global received_message
received_message = ""

def run():
    print("trying")
    HEADER_LENGTH = 10

    # IP Address of the server
    IP = "192.168.1.42"
    PORT = 1234
    my_username = "Thomas"
    # my_username = input("Username: ")

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to a given ip and port
    client_socket.connect((IP, PORT))
    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(False)
    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    while True:
        print("listening...")
        time.sleep(2)
        try:
            # Now we want to loop over received messages (there might be more than one) and print them

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            global received_message
            received_message = message

            # Print message
            print(f'{username} > {message}')
        except:
            pass
