from log_publisher.modules.connection import handle_connection

class LogPublisher:      # rename to log_channels
    def __init__(self,connection_dict):
        self.io_con=connection_dict.get("socketIO")
        self.webscoket_con=connection_dict.get("websocket")
        # self.TCP_con=connection_dict.get("TCP")
        self.REST_con=connection_dict.get("REST")
        self.UDP_con=connection_dict.get("UDP")
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
    def get_connections(self):
        return{
            "socketIO":self.io_con,
            "websocket":self.webscoket_con,
            # "TCP":self.TCP_con,
            "UDP":self.UDP_con,
            "REST":self.REST_con,
        }
    def log(self,message):
        cons=self.get_connections()
        for k,v in cons.items():
            if v!=None:
                handle_connection(k,v,message)
    

