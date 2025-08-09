import socket

def start_tcp_server(host='127.0.0.1', port=9003):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the address and port
        s.bind((host, port))
        print(f"Server started at {host}:{port}")

        # Listen for incoming connections (max 1 connection in queue)
        s.listen(1)

        while True:
            print("Waiting for a connection...")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                while True:
                    try:
                        print("000000000000000000000000")
                        data = conn.recv(1024)  # Receive up to 1024 bytes
                        print("_____", data)
                        if not data:
                            print("Client disconnected")
                            break
                        print(f"Received data: {data.decode()}")
                        # Echo the received data back to the client
                        conn.sendall(data)
                    except Exception as e:
                        print(f"Exception in recv/send loop: {e}")
                        break


if __name__ == "__main__":
    start_tcp_server()
