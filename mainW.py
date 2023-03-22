import os
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class mainW(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900,600)
        self.setWindowTitle("opencv车流识别系统")
        self.setWindowIcon(QIcon("./img/x_智能.png"))

        self.openFileBtn=QPushButton("打开文件",self)
        self.openFileBtn.setGeometry(20,20,100,30)

        self.imgCheckBtn=QPushButton("车辆图片识别",self)
        self.imgCheckBtn.setGeometry(260,20,120,30)

        self.videoCheckBtn=QPushButton("车辆视频",self)
        self.videoCheckBtn.setGeometry(400,20,100,30)

        self.collectFaceBtn = QPushButton("人脸采集", self)
        self.collectFaceBtn.setGeometry(520, 20, 100, 30)

        self.trainFaceBtn = QPushButton("人脸训练", self)
        self.trainFaceBtn.setGeometry(640, 20, 100, 30)

        self.checkFaceBtn = QPushButton("人脸识别", self)
        self.checkFaceBtn.setGeometry(760, 20, 100, 30)

        self.grabBtn=QPushButton("灰度处理",self)
        self.grabBtn.setGeometry(140,20,100,30)

        self.leftLab=QLabel("原图",self)
        self.leftLab.setGeometry(20,80,400,400)
        self.leftLab.setStyleSheet("background-color:white")

        self.rightLab = QLabel("新图", self)
        self.rightLab.setGeometry(440, 80, 400, 400)
        self.rightLab.setStyleSheet("background-color:white")

        self.openFileBtn.clicked.connect(self.openFile)
        self.grabBtn.clicked.connect(self.grayImg)
        self.imgCheckBtn.clicked.connect(self.imgCheck)
        self.videoCheckBtn.clicked.connect(self.videoCheck)
        self.collectFaceBtn.clicked.connect(self.collectFace)
        self.trainFaceBtn.clicked.connect(self.trainFace)
        self.checkFaceBtn.clicked.connect(self.checkFace)

    def openFile(self):
        #打开文件函数
        print("打开文件")
        self.img,imgType=QFileDialog.getOpenFileNames(self,"打开文件","","*.jpg;;*.png")#打开文件的弹窗
        self.s="".join(self.img)#生产正确路径
        self.leftLab.setPixmap(QPixmap(self.s))#s是路径
        self.leftLab.setScaledContents(True)#缩放


    def grayImg(self):
        #图片灰度处理
        print("图片灰度处理")
        img=cv2.imread(self.s)
        print(img)
        #灰度处理函数
        img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        print(img_gray)

        newImg="./img/gray1.jpg"
        cv2.imwrite(newImg,img_gray)#路径，图片
        print(newImg)
        self.rightLab.setPixmap(QPixmap(newImg))  # s是路径
        self.rightLab.setScaledContents(True)  # 缩放


    def imgCheck(self):
        #车辆识别
        print("车辆识别")
        #灰度处理
        img=cv2.imread(self.s)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #识别车辆
        car_detector=cv2.CascadeClassifier("./img/cars.xml")
        cars=car_detector.detectMultiScale(img_gray,1.1,1,cv2.CASCADE_SCALE_IMAGE,(50,50),(150,150))
        print(cars)
        #圈出车辆
        for (x,y,w,h) in cars:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        #保存+显示图片
        newImg = "./img/gray4.jpg"
        cv2.imwrite(newImg, img)  # 路径，图片
        self.rightLab.setPixmap(QPixmap(newImg))  # s是路径
        self.rightLab.setScaledContents(True)  # 缩放


    def videoCheck(self):
        #车辆识别
        print("打开车流视频")
        self.video,videoType=QFileDialog.getOpenFileNames(self,"打开视频","","*.mp4")
        self.v = "".join(self.video)  # 生产正确路径

        cap=cv2.VideoCapture(self.v)#加载视频
        print(cap)

         #加载级联分类器
        car_detector=cv2.CascadeClassifier("./img/cars.xml")
        while True:
            status, img = cap.read()  # 只读取视频的一帧数据
            if status:
                #灰度处理
                img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
                #检测车辆目标
                cars=car_detector.detectMultiScale(img_gray,1.1,2,cv2.CASCADE_SCALE_IMAGE,(40,40),(120,120))
                #把车框出来
                for (x, y, w, h) in cars:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0),2,cv2.LINE_AA)

                string="real time traffic flow:"+str(len(cars))
                #检测当下是几辆车
                cv2.putText(img,string,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255))
                #显示
                cv2.imshow("opencv(ESC-quit)",img)
            else:
                break
            key=cv2.waitKey(10)#返回键盘的键值
            if key==27:  #ESC键 退出键 键值27
                break

        #cap.release()
        #cv2.desstoryAllWindows()

    def collectFace(self):
        print("人脸识别")
        #打开摄像头
        cap=cv2.VideoCapture(0)
        face_detector=cv2.CascadeClassifier("./img/haarcascade_frontalface_default.xml")
        i=1
        while True:
            status,img=cap.read()
            if status:
                img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
                #识别人脸
                faces=face_detector.detectMultiScale(img_gray,1.1,2,cv2.CASCADE_SCALE_IMAGE,(200,200),(350,350))
                #把车框出来
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2, cv2.LINE_AA)
                    filename="./face_img/chen{}.jpg".format(i)
                    cv2.imwrite(filename,img_gray[y:y+h,x:w+x])
                    i=i+1

                cv2.imshow("opencv(ESC-quit)",img)
            else:
                break
            if i>300:
                break

            key=cv2.waitKey(2)
            if key==27:
                break

            #cap.release()
            #cv2.desstoryAllWindows()


    def trainFace(self):
        print("识别训练")
        path="./face_img/"
        recognizer= cv2.face.LBPHFaceRecognizer_create()#创建人脸识别器
        facedata=[]#储存人脸像素数据集合
        ids=[]
        file_list=os.listdir(path)#打开某个目录 返回路径下的所有文件名称
        for file in file_list:
            img=cv2.imread(path+file)
            img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            print(img_gray)
            facedata.append(img_gray)
            ids.append(0)


        recognizer.train(facedata,np.array(ids))
        recognizer.write("./train.yml")
        print("训练完毕")






    def checkFace(self):
        print("识别项目")
        cap=cv2.VideoCapture(0)
        face_detector=cv2.CascadeClassifier("./img/haarcascade_frontalface_default.xml")

        recognizer=cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("./train.yml")
        count = 0
        while True:
            status, img = cap.read()
            if status:
                img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                # 识别人脸
                faces = face_detector.detectMultiScale(img_gray, 1.1, 2, cv2.CASCADE_SCALE_IMAGE, (200, 200),
                                                       (350, 350))
                # 把车框出来
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    user_id,confidence=recognizer.predict(img_gray[y:y+h,x:x+w])#识别器准确率
                    print(user_id,confidence)
                    chance=round(100-confidence)

                    if chance>70 :   #后续改！
                        count+=1


                cv2.imshow("opencv(ESC-quit)", img)
            else:
                break

            if count>10:
                print("识别成功")
                break

            key = cv2.waitKey(2)
            if key == 27:
                break

            # cap.release()
            # cv2.desstoryAllWindows()
            # cv2.waitKey(1)






if __name__=="__main__":
    app=QApplication(sys.argv)
    mainWin=mainW()
    mainWin.show()
    sys.exit(app.exec_())