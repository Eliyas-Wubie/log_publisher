from log_publisher.log_publisher import LogPublisher, connectChannel

con1=connectChannel("websocket","127.0.0.1",9002)
con2=connectChannel("socketIO","127.0.0.1",9001)
# con2=connectChannel("TCP","127.0.0.1",9003)
con3=connectChannel("file","./mylog")
con4=connectChannel("REST","127.0.0.1",9000,"/hey")
con5=connectChannel("UDP","127.0.0.1",9004)

connection_dict={
    "websocket":con1,
    "socketIO":con2,
    "file":con3,
    "REST":con4,
    "UDP":con5
}

log_publisher=LogPublisher(connection_dict,console_logging=True)



