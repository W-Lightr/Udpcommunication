import sys

from PyQt5.QtWidgets import QApplication, QWidget
from main import Main_UI



# 启动类
class start:
    def __init__(self, F):
        self.Main = Main_UI()
        self.Main.init(F)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.move(550, 100)
    main = start(w)
    w.show()
    sys.exit(app.exec_())
