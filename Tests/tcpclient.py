# client_test.py
import socket

HOST = '127.0.0.1'
PORT = 9003

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello server!')  # ACTUALLY SEND DATA
    # Optional: receive echo
    # print("Server says:", s.recv(1024).decode())
