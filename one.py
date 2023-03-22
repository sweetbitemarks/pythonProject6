import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mainW import mainW
import os

# 登录窗口的定义
class loginW(QWidget):
    #构造函数
    def __init__(self):
        super().__init__()
        self.resize(1146,710)
        self.setWindowTitle("opencv车流识别系统")
        self.setWindowIcon(QIcon("D:/python_work/opencv/img/x_智能.png"))
        #设置背景
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap("D:/python_work/opencv/img/shou.jpg")))
        self.setPalette(palette)
        #给窗口添加控件

        #控件
        self.userLab=QLabel("用户名：",self)
        self.userLab.setGeometry(30,300,70,30)#x,y,w,h
        self.userLab.setStyleSheet("color:blue")

        self.pwdLab = QLabel("密 码：", self)
        self.pwdLab.setGeometry(30, 340, 70, 30)  # x,y,w,h
        self.pwdLab.setStyleSheet("color:blue")

        #编辑框
        self.userEdit=QLineEdit(self)
        self.userEdit.setGeometry(90,300,130,30)
        self.pwdEdit = QLineEdit(self)
        self.pwdEdit.setGeometry(90, 340, 130, 30)
        self.pwdEdit.setEchoMode(QLineEdit.Password)
        #按钮
        self.loginBtr=QPushButton("登录",self)
        self.loginBtr.setGeometry(30,400,100,30)

        self.quitBtr = QPushButton("退出", self)
        self.quitBtr.setGeometry(150, 400, 100, 30)
        #给按钮挂链接
        self.loginBtr.clicked.connect(self.login)
        self.quitBtr.clicked.connect(self.quit)
        self.userslist = [["root", "123456"], ["niuniu", "123456"]]


    def login(self):
        #登录事件
        print("login")
        userName=self.userEdit.text()
        userPwd=self.pwdEdit.text()#获取输入框的数据
        for (name, pwd) in self.userslist:
            if (userName == name and userPwd == pwd):
                print("登录成功")

                QMessageBox.about(self,"提示框","登录成功")
                os.system("start python mainW.py")
                sys.exit()
                break
            else:
                print("登录失败")
                QMessageBox.about(self, "提示框", "登录失败")
                break
    def quit(self):
        sys.exit()



if __name__=="__main__":
    app=QApplication(sys.argv)  #实例化QApplication应用程序对象
    loginWin=loginW()#实例化一个登录窗
    lt=mainW()
    loginWin.show()#显示窗口
    sys.exit(app.exec_())