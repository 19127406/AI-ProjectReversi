import socket, re

from CustomBot import callCustomBot

HOST, PORT = input("Input server IP: "), 14003
match_num = int(input("Input number of match: "))
win_match = 0
color = ""

for i in range(match_num):
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        while True:
            ret = str(sock.recv(1024), "ASCII")
            print(ret)
            if re.match("^victory_cell", ret):
                color = (ret.split('\n'))[12]
            if re.match("^victory_cell", ret) is None:
                win_color = (ret.split('\n'))[3]
                if win_color == color:
                    win_match += 1
                break
            else:
                sock.sendall(bytes(callCustomBot(ret), "ASCII"))

print("Win rate: ", win_match * 100 / match_num, "%")