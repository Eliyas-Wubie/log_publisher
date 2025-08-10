from log_publisher.main import LogPublisher, connectChannel

con1=connectChannel("websocket","127.0.0.1",9002)
con2=connectChannel("TCP","127.0.0.1",9003)
con3=connectChannel("file","./ls/ls/ls")

connection_dict={
    "websocket":con1,
    "TCP":con2
}

log_publisher=LogPublisher(connection_dict,console_logging=True)



