import websocket
import socketio
import socket
import threading
import requests
import os
import json
import time
import signal
import sys
from datetime import date,datetime

class connectChannel: #TESTED
    def __init__(self,connection_type,ip,port=None,other=None):
        self.io_con=None
        self.websocket_con=None
        self.general_ip=ip
        self.general_port=port
        if connection_type=="socketIO":
            try:
                self.connect_io()
            except Exception as e:
                print(f"error while establishing socketio connection : {e}")
        
        elif connection_type=="websocket":
            try:
                self.connect_websocket()
            except Exception as e:
                print(f"error while establishing websocket connection : {e}")
        
        elif connection_type=="REST":
            try:
                self.rest_ip=ip
                self.rest_port=port
                self.rest_route=other
            except Exception as e:
                print(f"error while defining Rest API : {e}")
        
        elif connection_type=="UDP":
            try:
                self.udp_ip=ip
                self.udp_port=port
            except Exception as e:
                print(f"error while Defining UDP : {e}")
        
        elif connection_type=="file":
            try:
                if not os.path.exists(ip):
                    os.makedirs(ip)
                self.file_path=ip
            except Exception as e:
                print(f"error while defining log path : {e}")
    
    def get_socketIO(self):
        if self.io_con:
            return self.io_con
        else:
            print("Trying to get uninitialized connection - Socketio connection - returned None")
            return None
        
    def get_websocket(self):
        if self.websocket_con:
            return self.websocket_con
        else:
            print("Trying to get uninitialized connection - websocket connection - returned None")
            return None
        
    def get_REST_api(self):
        if self.rest_ip and self.rest_port and self.rest_route:
            return {"ip":self.rest_ip, "port":self.rest_port, "route":self.rest_route}
        else:
            raise Exception("Trying to get undefined Rest api defination")
        
    def get_UDP(self):
        if self.udp_ip and self.udp_port:
            return {"ip":self.udp_ip, "port":self.udp_port}
        else:
            raise Exception("Trying to get undefined UDP defination")

    def get_file_path(self):
        if self.file_path:
            return self.file_path
        else:
            raise Exception("Trying to get undefined file logging")

    def is_connected(self):
        try:
            return self.io_con is not None and self.io_con.connected
        except:
            return False
        
    def connect_io(self):
        if self.io_con is not None:
            try:
                print("🔌 Cleaning up previous Socket.IO client...")
                self.io_con.disconnect()
            except Exception:
                pass
            self.io_con = None  # Clear it regardless
        self.io_ip=self.general_ip
        self.io_port=self.general_port
        def _on_io_disconnect():
            self.io_con=None
            print("❌ (LOG PUBLISHER) Socket IO - Disconnected")
        def _on_io_connect():
            print("✅ (LOG PUBLISHER) Socket IO - Connected")
        sio=socketio.Client()
        sio.on("connect",_on_io_connect)
        sio.connect(f"http://{self.io_ip}:{self.io_port}")
        self.io_con=sio
        sio.on("disconnect",_on_io_disconnect)
    
    def connect_websocket(self):
        if self.websocket_con is not None:
            try:
                print("🔌 Cleaning up previous WebSocket client...")
                self.websocket_con.disconnect()
            except Exception:
                pass
            self.websocket_con = None  # Clear it regardless
        self.websocket_ip=self.general_ip
        self.websocket_port=self.general_port
        def on_message(ws, message):
            pass
        def on_error(ws, error):
            pass
        def on_close(ws, close_status_code, close_msg):
            self.websocket_con=None
            print("❌ (LOG PUBLISHER) Web Socket - Disconnected")
        def on_open(ws):
            print("✅ (LOG PUBLISHER) Web Socket - Connected")
            ws.send("Hello server!")
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

def handle_connection(key,value,message):
    if key=="socketIO":
        try:
            con=value.get_socketIO()
            con.send(message)
        except Exception as e:
            print(f"Error sending socketio messege: {e}")
    
    if key=="websocket":
        try:
            con=value.get_websocket()
            con.send(message)
        except Exception as e:
            print(f"Error sending websocket messege: {e}")

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
            url=f"http://{ip_port.get("ip")}:{ip_port.get("port")}{ip_port.get("route")}"
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
            with open(full_path,"a") as log_file:
                log_file.write(json.dumps(log)+"\n")
        except Exception as e:
            print(f"Error saving messege to file: {e}")

def handle_reconnect(states):
    while not states._stop_event.is_set():
        print("30 sec??")
        try:
            if states.websocket_con.websocket_ip and states.websocket_con.websocket_port:
                if states.websocket_con.get_websocket()==None:
                    try:
                        print("Reconnecting websocket . . . ")
                        states.websocket_con.connect_websocket()
                    except Exception as e:
                        print(f"\t ❌ (LOG PUBLISHER) websocket reconnection failed")
        except Exception as e:
            pass
        try:
            if  states.io_con.io_ip and states.io_con.io_port:
                if not states.io_con.is_connected():
                    try:
                        print("Reconnecting socketio . . .x ",states.io_con)
                        states.io_con.connect_io()
                    except Exception as e:
                        print(f"\t ❌ (LOG PUBLISHER) socketio reconnection failed")
        except:
            pass
        states._stop_event.wait(30)


class LogPublisher:      # rename to log_channels
    def __init__(self,connection_dict,console_logging=False):
        self.io_con=connection_dict.get("socketIO")
        self.websocket_con=connection_dict.get("websocket")
        self.REST_con=connection_dict.get("REST")
        self.UDP_con=connection_dict.get("UDP")
        self.file_path=connection_dict.get("file")
        self.console=console_logging

        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=handle_reconnect, args=(self,), daemon=True)
        self.thread.start()
        # Register signal handlers INSIDE the class
        signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        signal.signal(signal.SIGTERM, self._handle_shutdown_signal)

    def set_connections(self,connection_dict):
        keys=list(connection_dict.keys())
        if "socketIO" in keys:
            self.io_con=connection_dict.get("socketIO")
        if "websocket" in keys:
            self.websocket_con=connection_dict.get("websocket")
        if "REST" in keys:
            self.REST_con=connection_dict.get("REST")
        if "UDP" in keys:
            self.UDP_con=connection_dict.get("UDP")
        if "file" in keys:
            self.UDP_con=connection_dict.get("file")
    
    def get_connections(self):
        return{
            "socketIO":self.io_con,
            "websocket":self.websocket_con,
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
    
    def _handle_shutdown_signal(self, signum, frame):
        print(f"\n🛑 Received shutdown signal ({signum}), cleaning up LogPublisher...")
        self._shutdown()
        sys.exit(0)

    def _shutdown(self):
        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join(timeout=5)

        # for conn in [self.io_con, self.websocket_con, self.REST_con, self.UDP_con]:
        #     try:
        #         if conn and hasattr(conn, "close"):
        #             conn.close()
        #     except Exception as e:
        #         print(f"⚠️ Error closing {conn}: {e}")