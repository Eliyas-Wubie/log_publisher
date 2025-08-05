

import websocket
import socketio
import socket
import threading


class connect: #TESTED
    def __init__(self,connection_type,ip,port,other=None):
        self.io_con=""
        self.websocket_con=""
        self.tcp_con=""
        if connection_type=="socketIO":
            self.io_ip=ip
            self.io_port=port
        elif connection_type=="websocket":
            self.websocket_ip=ip
            self.websocket_port=port
        elif connection_type=="TCP":
            self.tcp_ip=ip
            self.tcp_port=port
        elif connection_type=="REST":
            self.rest_ip=ip
            self.rest_port=port
            self.rest_route=other
        elif connection_type=="UDP":
            self.udp_ip=ip
            self.udp_port=port
    def connect_socketIO(self):
        sio=socketio.Client()
        sio.connect(f"http://{self.io_ip}:{self.io_port}")
        self.io_con=sio
        return self
    def get_socketIO(self):
        return self.io_con
    def connect_websocket(self):
        def on_message(ws, message):
            print("📨 Received:", message)
        def on_error(ws, error):
            print("❗ Error:", error)
        def on_close(ws, close_status_code, close_msg):
            print("❌ Disconnected")
        def on_open(ws):
            print("✅ Connected")
            ws.send("Hello server!")
        # Create and run WebSocket
        ws = websocket.WebSocketApp(
            f"ws://{self.websocket_ip}:{self.websocket_port}",  # Replace with your WebSocket server URL
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        def run_ws():
            ws.run_forever() 
        thread = threading.Thread(target=run_ws)
        thread.daemon = True  # This makes the thread exit when the main program exits
        thread.start()
        self.websocket_con=ws
        return self
    def get_websocket(self):
        return self.websocket_con
    def connect_TCP(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.tcp_ip, self.tcp_port))
        self.tcp_con=client_socket
        return self
    def get_TCP(self):
        return self.tcp_con
    def register_REST_api(self):
        return {"ip":self.rest_ip, "port":self.rest_port, "route":self.rest_route}
    def register_UDP(self):
        return {"ip":self.udp_ip, "port":self.udp_port}

class connectionPool:
    def __init__(self,connections=[]):
        self.con_list=connections
    def add_connection(self,con_type,connection):
        self.con_list.append({con_type:connection})
        return self
    def get_connection(self):
        return self.con_list