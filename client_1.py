import socket
import threading
import logging


logging.basicConfig(level = logging.INFO)


# How many bytes of header msg
HEADER = 64
# What port server will use to connect with clients
PORT = 5050
# IP of server that you need to connect with - in this case it would be IP of local network computer
SERVER = '192.168.56.1'
ADDR = (SERVER, PORT)
# What format will be used for decoding message from client
FORMAT = 'utf-8'
# What msg will be used for close connection with given client
DISCONNECT_MESSAGE = "!DISCONNECT"


# Defice client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send_msg(msg: str):
    # Encode string message into byte object representation that cen be send by socket
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # Prepare correct padding for message
    # E.G: '10                                    '
    # There must be number and padding, that whole message need to have 64 bytes of length
    # First number in this string seys how long is real msg load
    send_length += b' ' * (HEADER - len(send_length))
    # Send message to server with info how long is message
    client.send(send_length)
    # Send real msg load
    client.send(message)


if __name__ == '__main__':
    load = 'This is message from client 1!'
    send_msg(load)
    send_msg(DISCONNECT_MESSAGE)
