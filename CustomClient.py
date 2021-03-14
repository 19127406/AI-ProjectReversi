import socket, re

from CustomBot import CustomBot

#HOST, PORT = "209.97.169.233", 14003
HOST, PORT = "localhost", 14003

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    while True:
        ret = str(sock.recv(1024), "ASCII")
        print(ret)
        if re.match("^victory_cell", ret) is None:
            break
        else:
            sock.sendall(bytes(CustomBot(ret), "ASCII"))
