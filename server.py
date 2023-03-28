import socket
import threading
import logging


logging.basicConfig(level = logging.INFO)


# How many bytes of header msg
HEADER = 64
# What port server will use to connect with clients
PORT = 5050
# IP of server - in this case it would be IP of local network computer
# IP can be read automatically by socket library
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# What format will be used for decoding message from client
FORMAT = 'utf-8'
# What msg will be used for close connection with given client
DISCONNECT_MESSAGE = "!DISCONNECT"

# Define server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    logging.info(f'[NEW CONNECTION] Connected with {addr}')

    connected = True
    while connected:
        # Define msg length
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # Take real message load
            msg = conn.recv(msg_length).decode(FORMAT)

            # Check if connection should be closed
            if msg == DISCONNECT_MESSAGE:
                connected = False

            logging.info(f'[MESSAGE] Message from {addr}: {msg}')

    conn.close()


def start_server():
    # Start to listening by server
    server.listen()
    logging.info(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        # Accept msg from client and save his connection and address
        conn, addr = server.accept()
        # Handle this message with threading in parallel, need to be able for handling another client
        # Run function with arfuments in another thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        logging.info(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


if __name__ == '__main__':
    logging.info('[STARTING] Server is starting...')
    start_server()