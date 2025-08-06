

import websocket
import socketio
import socket
import threading
import requests


class connect: #TESTED
    def __init__(self,connection_type,ip,port,other=None):
        self.io_con=""
        self.websocket_con=""
        self.tcp_con=""
        if connection_type=="socketIO":
            self.io_ip=ip
            self.io_port=port
            sio=socketio.Client()
            sio.connect(f"http://{self.io_ip}:{self.io_port}")
            self.io_con=sio
        elif connection_type=="websocket":
            self.websocket_ip=ip
            self.websocket_port=port
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
        elif connection_type=="TCP":
            self.tcp_ip=ip
            self.tcp_port=port
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.tcp_ip, self.tcp_port))
            self.tcp_con=client_socket
        elif connection_type=="REST":
            self.rest_ip=ip
            self.rest_port=port
            self.rest_route=other
        elif connection_type=="UDP":
            self.udp_ip=ip
            self.udp_port=port
    def get_socketIO(self):
        return self.io_con
    def get_websocket(self):
        return self.websocket_con
    def get_TCP(self):
        return self.tcp_con
    def get_REST_api(self):
        return {"ip":self.rest_ip, "port":self.rest_port, "route":self.rest_route}
    def get_UDP(self):
        return {"ip":self.udp_ip, "port":self.udp_port}

def handle_connection(key,value,message):
    if key=="socketIO":
        try:
            con=value.get_sokcetIO()
            con.send(message)
        except Exception as e:
            print("could not send socket io")
    if key=="websocket":
        try:
            con=value.get_websocket()
            con.send(message)
        except Exception as e:
            print("could not send websocket")
    if key=="TCP":
        try:
            con=value.get_TCP()
            print("sending")
            con.sendall(message.encode("utf-8"))
            print("sent")

        except Exception as e:
            print("could not send TCP",e)
    if key=="UDP":
        try:
            ip_port=value.get_UDP()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message.encode('utf-8'), (ip_port.get("ip"), ip_port.get("port")))
        except Exception as e:
            print("Could not send UDP")
    if key=="REST":
        try:
            ip_port=value.get_REST_api()
            print("..............",ip_port)
            url=f"http://{ip_port.get("ip")}:{ip_port.get("port")}/"
            requests.post(url=url,json={"message":message})
        except Exception as e:
            print("Could not send REST API")