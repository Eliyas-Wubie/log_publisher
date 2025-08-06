from log_publisher.main import LogPublisher
from log_publisher.modules.connection import connect

con1=connect("websocket","127.0.0.1",9002)
con2=connect("TCP","127.0.0.1",9003)

connection_dict={
    "websocket":con1,
    "TCP":con2
}

log_publisher=LogPublisher(connection_dict)



