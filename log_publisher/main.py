from log_publisher.modules.connection import connectionPool,connect
import socket
import requests


class LogPublisher:
    def __init__(self,connection_pool=[]):
        self.con_pool = connection_pool
    def log(self,message):
        for item in self.con_pool:
            con_type=list(item.keys())[0]
            con=list(item.values())[0]
            if con_type=="socketIO":
                sio=con.get_socketIO()
                sio.send(message)
            if con_type=="websocket":
                websoc=con.get_websocket()
                websoc.send(message)
            if con_type=="REST":
                ip_port= con
                print("..............",ip_port)
                url=f"http://{ip_port.get("ip")}:{ip_port.get("port")}/"
                requests.post(url=url,json={"message":message})
            if con_type=="TCP":
                tcpcon=con.get_TCP()
                print("****************",tcpcon)
                try:
                    tcpcon.sendall(message.encode())
                except Exception as e:
                    print("Send failed:", e)
            if con_type=="UDP":
                ip_port=con.register_UDP()
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(message.encode('utf-8'), (ip_port.get("ip"), ip_port.get("port")))
