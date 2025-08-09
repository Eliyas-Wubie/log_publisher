

import websocket
import socketio
import socket
import threading
import requests


class connectChannel: #TESTED rename to connectChannel
    def __init__(self,connection_type,ip,port,other=None):
        self.io_con=None
        self.websocket_con=None
        # self.tcp_con=None
        if connection_type=="socketIO":
            try:
                self.io_ip=ip
                self.io_port=port
                sio=socketio.Client()
                sio.connect(f"http://{self.io_ip}:{self.io_port}")
                self.io_con=sio
            except Exception as e:
                print(f"encountered issue while establishing socketio connection : {e}")
        elif connection_type=="websocket":
            try:
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
            except Exception as e:
                print(f"encountered issue while establishing websocket connection : {e}")
        # elif connection_type=="TCP":
        #     try:
        #         self.tcp_ip=ip
        #         self.tcp_port=port
        #         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #         client_socket.connect((self.tcp_ip, self.tcp_port))
        #         self.tcp_con=client_socket
        #     except Exception as e:
        #         print(f"encountered issue while establishing TCP connection : {e}")
        elif connection_type=="REST":
            try:
                self.rest_ip=ip
                self.rest_port=port
                self.rest_route=other
            except Exception as e:
                print(f"encountered issue while defining Rest API : {e}")
        elif connection_type=="UDP":
            try:
                self.udp_ip=ip
                self.udp_port=port
            except Exception as e:
                print(f"encountered issue while Defining UDP : {e}")
    
    def get_socketIO(self):
        if self.io_con:
            return self.io_con
        else:
            raise Exception("trying to get uninitialized connection - Socketio connection")
        
    def get_websocket(self):
        if self.websocket_con:
            return self.websocket_con
        else:
            raise Exception("trying to get uninitialized connection - websocket connection")
        
    # def get_TCP(self):
    #     if self.tcp_con:
    #         return self.tcp_con
    #     else:
    #         raise Exception("trying to get uninitialized connection - TCP connection")
        
    def get_REST_api(self):
        if self.rest_ip and self.rest_port and self.rest_route:
            return {"ip":self.rest_ip, "port":self.rest_port, "route":self.rest_route}
        else:
            raise Exception("trying to get uninitialized connection - Rest api defination")
        
    def get_UDP(self):
        if self.udp_ip and self.udp_port:
            return {"ip":self.udp_ip, "port":self.udp_port}
        else:
            raise Exception("trying to get uninitialized connection - UDP defination")

def handle_connection(key,value,message):
    if key=="socketIO":
        try:
            con=value.get_sokcetIO()
            con.send(message)
        except Exception as e:
            print(f"Error sending socketio messege: {e}")
    if key=="websocket":
        try:
            con=value.get_websocket()
            con.send(message)
        except Exception as e:
            print(f"Error sending websocket messege: {e}")
    # if key=="TCP":
    #     try:
    #         con=value.get_TCP()
    #         con.sendall(b"heyyyyyyy man")
    #     except Exception as e:
    #         print(f"Error sending TCP messege: {e}")
    if key=="UDP":
        try:
            ip_port=value.get_UDP()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message.encode('utf-8'), (ip_port.get("ip"), ip_port.get("port")))
        except Exception as e:
            print(f"Error sending UDP messege: {e}")
    if key=="REST":
        try:
            ip_port=value.get_REST_api()
            url=f"http://{ip_port.get("ip")}:{ip_port.get("port")}/"
            requests.post(url=url,json={"message":message})
        except Exception as e:
            print(f"Error sending Rest API messege: {e}")