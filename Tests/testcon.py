from log_publisher.modules.connection import connect
import socket

def test_rest():
    import requests
    con=connect("REST","127.0.0.1",9000)
    ip_port=con.register_REST_api()

    data={"message":"hi"}
    url=f"http://{ip_port.get("ip")}:{ip_port.get("port")}/"
    requests.post(url=url,json=data)

def test_socketio():
    con=connect("socketIO","127.0.0.1",9001)
    sio=con.connect_socketIO()
    sio.send("hello")

def test_websocket():
    con=connect("websocket","127.0.0.1",9002)
    websoc=con.connect_websocket()
    websoc.send("hello")

def test_tcp(): # problem, connection is force closing by the cliend
    con=connect("TCP","127.0.0.1",9003)
    tcp_con=con.connect_TCP()
    tcp_con.sendall("hello".encode())

con=connect("UDP","127.0.0.1",9004)
ip_port=con.register_UDP()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("hello".encode('utf-8'), (ip_port.get("ip"), ip_port.get("port")))