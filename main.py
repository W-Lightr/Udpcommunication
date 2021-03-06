import socket

from ui import Ui_Form, QtWidgets
from Config import Config
from Threadpools import ThreadSet
from SocketUDP import UDP


class Main_UI(Ui_Form):
    def __init__(self):
        self.Config = Config()
        self.Thread = ThreadSet()
        self.Sock = UDP()

    def init(self, F):
        self.setupUi(F)  # 初始化界面
        self.label_6.setText(socket.gethostbyname(socket.gethostname()))
        # 信号槽
        self.lineEdit_2.editingFinished.connect(self.setip)
        self.lineEdit_3.editingFinished.connect(self.setip)
        self.pushButton_2.clicked.connect(self.LinkAddress)
        self.radioButton.clicked.connect(self.con)
        self.pushButton_3.clicked.connect(self.Break)
        self.pushButton.clicked.connect(self.SendMessage)
        self.lineEdit_4.editingFinished.connect(self.setName)
        self.pushButton_4.clicked.connect(self.listWidget.clear)
        self.lineEdit.returnPressed.connect(self.SendMessage)
        self.Hideshow(0)

    # 设置名字
    def setName(self):
        self.Config.name = self.lineEdit_4.text()

    # 设置ip 端口
    def setip(self):
        self.Config.ip = self.lineEdit_2.text()
        self.Config.port = self.lineEdit_3.text()

    def con(self):
        self.Config.isService = not self.Config.isService

    # 开始连接
    def LinkAddress(self):
        self.Thread.Threadset.submit(self.LinkSon)

    # 连接
    def LinkSon(self):
        if self.Config.isService:  # 服务端
            if self.Config.port == "" or self.Config.port is None:
                self.label_3.setText("端口为空")
                return
            self.label_3.setText("等待连接")
            self.Hideshow(1)
            data = self.Sock.ServiceUDP()
            if data[0].decode(encoding='utf-8') == 'Client01':
                self.label_3.setText("连接成功")
                self.Config.isConnect = True
                self.Thread.Threadset.submit(self.RecvMessage(1))
            else:
                self.label_3.setText("连接失败")
                self.Hideshow(0)
                self.Sock.Cancel()
        else:
            # 客户端
            if not (self.Config.port == "" or self.Config.port is None) and not \
                    (self.Config.ip == "" or self.Config.ip is None):
                self.label_3.setText("连接中")
                self.Hideshow(1)
                data = self.Sock.ClientUDP()
                if data[0].decode(encoding='utf-8') == 'Service01':
                    self.label_3.setText("连接成功")
                    self.Config.isConnect = True
                    self.Thread.Threadset.submit(self.RecvMessage(0))
                else:
                    self.label_3.setText("连接失败")
                    self.Hideshow(0)
                    self.Sock.Cancel()
            else:
                self.label_3.setText("IP或端口为空")
                return

    # 聊天接收
    def RecvMessage(self, flag):
        msg = None
        while True:
            if flag == 1:  # 1 服务端 0 客户端
                msg = self.Sock.ServiceReceive()  # 接收消息
            elif flag == 0:
                msg = self.Sock.ClinentReceive()  # 接收消息
            # 设置消息
            if msg == "exit":
                self.Sock.Cancel()
                self.Hideshow(0)
                self.label_3.setText("未连接")
                self.listWidget.clear()
                break
            self.listWidget.addItem(f"{msg}")

    def Hideshow(self, t):
        if t == 1:
            self.pushButton_2.hide()  # 1 连接隐藏 0 断开隐藏
            self.pushButton_3.show()
        elif t == 0:
            self.pushButton_2.show()
            self.pushButton_3.hide()

    def Break(self):
        self.listWidget.clear()
        if self.Config.isConnect:
            if self.Config.isService:
                self.Sock.Servicesend("exit")
            else:
                self.Sock.Clientsend("exit")
        self.Hideshow(0)
        self.label_3.setText("未连接")
        self.Sock.Cancel()

    def SendMessage(self):
        if self.Config.isConnect:
            msg = self.lineEdit.text()
            if self.Config.isService:
                self.Thread.Threadset.submit(self.Sock.Servicesend(self.Config.name + ": " + msg))
            else:
                self.Thread.Threadset.submit(self.Sock.Clientsend(self.Config.name + ": " + msg))
            item = QtWidgets.QListWidgetItem(f"{msg} :{self.Config.name}", self.listWidget)
            item.setTextAlignment(2)
            self.lineEdit.setText("")
            
