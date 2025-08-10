import websocket
import socketio
import socket
import threading
import requests
import os
import json
from datetime import date,datetime

class connectChannel: #TESTED rename to connectChannel
    def __init__(self,connection_type,ip,port=None,other=None):
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
                sio.on("disconnect", self._on_io_disconnect()) # define
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
                    self.websocket_con=None
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
        elif connection_type=="file":
            try:
                if not os.path.exists(ip):
                    os.makedirs(ip)
                self.file_path=ip
            except Exception as e:
                print(f"encountered issue while establishing socketio connection : {e}")
    
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

    def get_file_path(self):
        if self.file_path:
            return self.file_path
        else:
            raise Exception("trying to get uninitialized file path - file logging")

    def reconnect(self):
        con=""

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
    if key=="file":
        try:
            path=value.get_file_path()
            today = date.today()
            formatted_date = f"{today.year}-{today.month}-{today.day}"
            file_name=formatted_date+".log"
            full_path = os.path.join(path, file_name)
            log={
                "timestamp":datetime.now().isoformat(),
                "message":message
            }
            with open(full_path) as log_file:
                log_file.write(json.dumps(log)+"\n")
        except Exception as e:
            print(f"Error sending socketio messege: {e}")

def handle_reconnect():
    # opern a thread and attemt reconnect on all passed connection, and if connected exit
    pass

class LogPublisher:      # rename to log_channels
    def __init__(self,connection_dict,console_logging=False):
        self.io_con=connection_dict.get("socketIO")
        self.webscoket_con=connection_dict.get("websocket")
        # self.TCP_con=connection_dict.get("TCP")
        self.REST_con=connection_dict.get("REST")
        self.UDP_con=connection_dict.get("UDP")
        self.file_path=connection_dict.get("file")
        self.console=console_logging
        handle_reconnect()
        # initiate reconnection handler - 
        # where all the connection objects that are not none but, do not have a socket connected
        # will be handled in a thread where a reconnect will be attempted every 20 sec
    def set_connections(self,connection_dict):
        keys=list(connection_dict.keys())
        if "socketIO" in keys:
            self.io_con=connection_dict.get("socketIO")
        if "websocket" in keys:
            self.webscoket_con=connection_dict.get("websocket")
        # if "TCP" in keys:
        #     self.TCP_con=connection_dict.get("TCP")
        if "REST" in keys:
            self.REST_con=connection_dict.get("REST")
        if "UDP" in keys:
            self.UDP_con=connection_dict.get("UDP")
        if "file" in keys:
            self.UDP_con=connection_dict.get("file")
    def get_connections(self):
        return{
            "socketIO":self.io_con,
            "websocket":self.webscoket_con,
            # "TCP":self.TCP_con,
            "UDP":self.UDP_con,
            "REST":self.REST_con,
            "file":self.file_path,
        }
    def log(self,message):
        if self.console:
            print("prefix",message,"suffix")
        cons=self.get_connections()
        for k,v in cons.items():
            if v!=None:
                handle_connection(k,v,message)
    

