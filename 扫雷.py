import queue
from random import randint
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal

dx = [1, -1, 0, 0, -1, 1, -1, 1]  # 坐标
dy = [0, 0, 1, -1, -1, 1, 1, -1]


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(583, 476)

        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(150, 130, 251, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.la_r = QtWidgets.QLabel(self.gridLayoutWidget)
        self.la_r.setStyleSheet("font: 14pt \"Arial\";")
        self.la_r.setObjectName("la_r")
        self.gridLayout.addWidget(self.la_r, 0, 0, 1, 1)

        self.la_c = QtWidgets.QLabel(self.gridLayoutWidget)
        self.la_c.setStyleSheet("font: 14pt \"Arial\";")
        self.la_c.setObjectName("la_c")
        self.gridLayout.addWidget(self.la_c, 1, 0, 1, 1)

        self.line_c = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_c.setObjectName("line_c")
        self.gridLayout.addWidget(self.line_c, 0, 1, 1, 1)

        self.line_r = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_r.setObjectName("line_r")
        self.gridLayout.addWidget(self.line_r, 1, 1, 1, 1)

        self.linker = QtWidgets.QCommandLinkButton(Form)
        self.linker.setGeometry(QtCore.QRect(440, 407, 101, 51))
        self.linker.setObjectName("linker")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.la_r.setText(_translate("Form", "请输入列数"))
        self.la_c.setText(_translate("Form", "请输入列数"))
        self.linker.setText(_translate("Form", "继续"))


class Mybutton(QtWidgets.QPushButton):

    def set(self, x, y):
        self.x = x
        self.y = y

    def send(self):
        # print(self.x, self.y)
        # self.hide()
        deal(int(self.x), int(self.y))
        pass


class game(object):
    # def __init__(self, Form,r,c):
    #     Form.setObjectName("Form")
    #     Form.resize(r*50, c*50)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # self.hide()
        Form.resize(583, 476)
        self.r = -1
        self.c = -1
        self.buttons = []
        self.la_c = QtWidgets.QLabel(self)
        self.la_c.setStyleSheet("font: 14pt \"Arial\";")
        self.la_c.setObjectName("la_c")

    def set(self, r, c, Form):
        print(r, c)
        Form.resize(int(r) * 50, int(c) * 50)
        self.r = r
        self.c = c
        self.buttons = []
        for i in range(int(r)):
            # print(i)
            tmp = []
            for j in range(int(c)):
                # print(i, "  ", j)
                tmp.append(Mybutton(self))
                # tmp[j].move(i*20+50,j*20+50)
                tmp[j].set(i, j)
                tmp[j].clicked.connect(tmp[j].send)
                # tmp[j].send.connect(self.deal)
                tmp[j].setGeometry(i * 20 + 50, j * 20 + 50, 20, 20)
            self.buttons.append(tmp)

    mine = 9999
    no_mine = 0
    n_mine = 10
    width = 10
    height = 10

    def set_init(self, width=10, height=10, nMines=10, vis={}):  # 初始化
        self.map = []
        for _ in range(height):
            t_line = []
            for _ in range(width):
                t_line.append(self.no_mine)
            self.map.append(t_line)
        self.vis = vis
        self.width = width
        self.height = height
        self.n_mine = nMines
        self.remix()
        self.restart()

    def reset(self):  # 重新设置，但是高度和炸弹的数目是不变的
        self.map.clear()
        self.vis.clear()
        for _ in range(self.height):
            t_line = []
            for _ in range(self.width):
                t_line.append(self.no_mine)
            self.map.append(t_line)
        self.remix()
        self.restart()  # 初始化标记

    # 打乱布局重新随机编排

    def remix(self):  # 设置炸弹的位置，以及各种数字的序号

        for y in range(self.height):
            for x in range(self.width):
                self.map[y][x] = self.no_mine

        def add_mark(x, y):
            # 如果不是雷的标记就+1
            if self.map[y][x] + 1 < self.mine:
                self.map[y][x] += 1
        mine_count = 0

        while mine_count < self.n_mine:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)

            if self.map[y][x] != self.mine:
                self.map[y][x] = self.mine

                mine_count += 1

                # 雷所在的位置的8个方位的数值+1
                ## 上下左右
                if y - 1 >= 0: add_mark(x, y - 1)
                if y + 1 < self.height: add_mark(x, y + 1)
                if x - 1 >= 0: add_mark(x - 1, y)
                if x + 1 < self.width: add_mark(x + 1, y)
                ## 四个角: 左上角、左下角、右上角、右下角
                if x - 1 >= 0 and y - 1 >= 0: add_mark(x - 1, y - 1)
                if x - 1 >= 0 and y + 1 < self.height: add_mark(x - 1, y + 1)
                if x + 1 < self.width and y - 1 >= 0: add_mark(x + 1, y - 1)
                if x + 1 < self.width and y + 1 < self.height: add_mark(x + 1, y + 1)

    def restart(self):
        for y in range(self.height):
            for x in range(self.width):
                 print(self.map[y][x], end=" ")
            print()

        for i in range(self.width):  # 初始化标记
            tmp = {}
            for j in range(self.height):
                tmp[j] = 0
            self.vis[i] = tmp

    def Search(self, x, y):  # 搜索
        q = queue.Queue()

        if self.map[y][x] == self.mine:
            print("炸弹")
        elif self.map[y][x] != 0:
            self.vis[y][x] = 1
            # self.buttons[x][y].setText(str(self.map[y][x]))
        else:

            q.put((x, y))
            self.vis[y][x] = 1

            while not q.empty():
                top = q.get()
                for i in range(8):
                    xx = top[0] + dx[i]
                    yy = top[1] + dy[i]
                    if 0 <= xx < self.width and 0 <= yy < self.height and self.vis[yy][xx] == 0:
                        if self.map[yy][xx] != 0:
                            self.vis[yy][xx] = 1
                            self.buttons[xx][yy].setText(str(self.map[yy][xx]))
                        else:
                            self.vis[yy][xx] = 1
                            q.put((xx, yy))
                            self.buttons[xx][yy].hide()

    def show(self):
        for i in range(self.width):
            for j in range(self.height):
                print(self.vis[i][j], end=" ")
            print()

    def __getitem__(self, key):
        return self.map[key]

    def __str__(self):
        format_str = ""
        for y in range(self.height):
            format_str += str(self[y]) + "\n"
        return format_str

    __repr__ = __str__

def deal(x, y):
    print(myWin.tmp.buttons[x][y].x, myWin.tmp.buttons[x][y].y)
    if (myWin.tmp.map[y][x] == 0):
        myWin.tmp.buttons[x][y].hide()
        myWin.tmp.Search(x, y)
    elif myWin.tmp.map[y][x] == 9999:
        myWin.tmp.buttons[x][y].setText("*")
    else:
        myWin.tmp.buttons[x][y].setText(str(myWin.tmp.map[y][x]))








class MynextForm(QMainWindow, game):
    def __init__(self, parent=None):
        super(MynextForm, self).__init__(parent)
        self.setupUi(self)
        # self.pushButton.clicked.connect(self.showMsg)

        self.r = 0
        self.c = 0


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # self.pushButton.clicked.connect(self.showMsg)
        self.linker.clicked.connect(self.read)
        self.tmp = MynextForm()
        self.r = 0
        self.c = 0

    def showMsg(self):
        QMessageBox.information(self, "信息提示框", "OK,内置信号与自定义槽函数！")

    def p(self):
        print(123)

    def read(self):
        print(self.line_c.text())
        print(self.line_r.text())
        self.hide()
        self.tmp.set(self.line_c.text(), self.line_r.text(), self.tmp)
        self.tmp.show()
        self.tmp.set_init(int(self.line_c.text()), int(self.line_r.text()), 100)
        # res.Search(0, 0)
        # self.game = game(self)
        # self.game = game(self,)
        # self.game.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())