import socket
from Config import Config


class UDP:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.UDPConfig = Config()
        self.Clientsocket = None
        self.Servicesocket = None
        self.SvFromAddr = None
        self.ClFromAddr = None
        

    def ServiceUDP(self):
        self.Servicesocket = socket.socket(type=socket.SOCK_DGRAM)
        try:
            self.Servicesocket.bind(("", int(self.UDPConfig.port)))
        except BaseException as msg:
            print(f"服务端error:{msg}")
        # 接收数据:data
        data, self.SvFromAddr = self.Servicesocket.recvfrom(1024)
        self.Servicesocket.sendto(b"Service01", self.SvFromAddr)
        return [data, self.SvFromAddr]

    def ClientUDP(self):
        self.Clientsocket = socket.socket(type=socket.SOCK_DGRAM)
        try:
            self.Clientsocket.sendto(b"Client01", (self.UDPConfig.ip, int(self.UDPConfig.port)))
        except BaseException as msg:
            print(f"客户端error:{msg}")
        data, self.ClFromAddr = self.Clientsocket.recvfrom(1024)
        return [data, self.ClFromAddr]

    def ServiceReceive(self):
        s = self.Servicesocket.recvfrom(1024)
        return s[0].decode()

    def ClinentReceive(self):
        s = self.Clientsocket.recvfrom(1024)
        return s[0].decode()

    def Clientsend(self, msg):
        try:
            self.Clientsocket.sendto(bytes(msg, encoding='utf-8'), self.ClFromAddr)
        except BaseException as ms:
            print(ms)

    def Servicesend(self, msg):
        try:
            self.Servicesocket.sendto(bytes(msg, encoding='utf-8'), self.SvFromAddr)
        except BaseException as ms:
            print(ms)

    def Cancel(self):
        if self.Clientsocket is not None:
            with self.Clientsocket as sock:
                sock.shutdown(2)

        elif self.Servicesocket is not None:
            with self.Servicesocket as sock:
                sock.shutdown(2)

        self.Servicesocket = None
        self.Clientsocket = None
        self.UDPConfig.isConnect = False
