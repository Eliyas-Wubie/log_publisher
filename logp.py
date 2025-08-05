from log_publisher.main import LogPublisher
from log_publisher.modules.connection import connectionPool,connect
import threading




# con1=connect("socketIO","127.0.0.1",9001)
# con1.connect_socketIO()
# con_pool=connectionPool().add_connection("socketIO",con1).get_connection()
# log_publisher=LogPublisher(con_pool)

#________________________________________________
# con2=connect("REST","127.0.0.1",9000,"/hey")
# apiclient=con2.register_REST_api()
# con_pool=connectionPool().add_connection("REST",apiclient).get_connection()
# log_publisher=LogPublisher(con_pool)

#________________________________________________
# con3=connect("websocket","127.0.0.1",9002)
# con4=con3.connect_websocket()
# # print("########3",con3,con4)
# con_pool=connectionPool().add_connection("websocket",con4).get_connection()
# log_publisher=LogPublisher(con_pool)

#________________________________________________
con3=connect("TCP","127.0.0.1",9003)
con4=con3.connect_TCP()
con_pool=connectionPool().add_connection("TCP",con4).get_connection()
log_publisher=LogPublisher(con_pool)



