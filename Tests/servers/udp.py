import socket

# Define the IP and port to listen on
UDP_IP = "127.0.0.1"  # listen on all interfaces
UDP_PORT = 9004

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")

while True:
    # Receive data from client
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print(f"Received message from {addr}: {data.decode('utf-8')}")
