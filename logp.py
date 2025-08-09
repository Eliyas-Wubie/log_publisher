from log_publisher.main import LogPublisher
from log_publisher.modules.connection import connectChannel

con1=connectChannel("websocket","127.0.0.1",9002)
con2=connectChannel("TCP","127.0.0.1",9003)

connection_dict={
    "websocket":con1,
    "TCP":con2
}

log_publisher=LogPublisher(connection_dict)



