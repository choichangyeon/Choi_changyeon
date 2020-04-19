from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import threading
import time

from Manager import Manager

from Mario import Mario
from Block import Block
from Map import Map

class Scene(QMainWindow):

    ed = False
    key = []
    uis = []
    uip = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Super Mario')

        self.left = 10
        self.top = 10
        self.width = 640 + 200
        self.height = 640
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initWorld()        
        self.initUI()
        self.show()
        self.mouseX = 0
        self.mouseY = 0
        self.mouseDown = False
        Manager.main = self

#        self.mario = Mario()
        #t = threading.Thread(target = self.Update)
        #t.start()
        
        self.marios = []
        for i in range(10):
            self.marios.append(Mario())

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Update)
        self.timer.start(0)
        
    def Update(self):
        for mario in self.marios:
            mario.UpdateFixed()
            mario.UpdateAI()
            mario.UpdateSprite()

        if(self.mouseDown):
            self.map.Change(self.mouseX, (self.mouseY + 16), Manager.blockID)

    def initWorld(self):
        self.map = Map(self)
        Manager.map = self.map

        self.map.CreateMap([[0] * 40 for i in range(40)])

    def initUI(self):
        btn_speed = QPushButton("Speed", self)
        btn_speed.setGeometry(self.width - 220, 10, 70, 30)
        btn_speed.clicked.connect(self.SpeedBtn)
        self.uis.append({"ui" : btn_speed, "pos" : [220, 10, 70, 30]})

        btn_jump = QPushButton("Jump", self)
        btn_jump.setGeometry(self.width - 220, 50, 70, 30)
        btn_jump.clicked.connect(self.JumpBtn)
        self.uis.append({"ui" : btn_jump, "pos" : [220, 50, 70, 30]})

        btn_gravity = QPushButton("Gravity", self)
        btn_gravity.setGeometry(self.width - 220, 90, 70, 30)
        btn_gravity.clicked.connect(self.GravityBtn)
        self.uis.append({"ui" : btn_gravity, "pos" : [220, 90, 70, 30]})

        self.line_speed = QLineEdit(str(Manager.speed), self)
        self.line_speed.setGeometry(self.width - 145, 10, 50, 30)
        self.line_speed.setValidator(QIntValidator())
        self.uis.append({"ui" : self.line_speed, "pos" : [145, 10, 50, 30]})

        self.line_jump = QLineEdit(str(Manager.jump), self)
        self.line_jump.setGeometry(self.width - 145, 50, 50, 30)
        self.line_jump.setValidator(QIntValidator())
        self.uis.append({"ui" : self.line_jump, "pos" : [145, 50, 50, 30]})

        self.line_gravity = QLineEdit(str(Manager.gravity), self)
        self.line_gravity.setGeometry(self.width - 145, 90, 50, 30)
        self.line_gravity.setValidator(QDoubleValidator())
        self.uis.append({"ui" : self.line_gravity, "pos" : [145, 90, 50, 30]})

        self.btn_marioSelect = QPushButton(self)
        self.btn_marioSelect.setGeometry(self.width - 90, 10, 80, 110)
        self.btn_marioSelect.setIcon(QtGui.QIcon("Textures/StateL_11.png"))
        self.btn_marioSelect.clicked.connect(self.MarioSelectBtn)
        self.uis.append({"ui" : self.btn_marioSelect, "pos" : [90, 10, 80, 110]})

        label_divLine1 = QLabel("-"*70, self)
        label_divLine1.setGeometry(self.width - 230, 130, 300, 10)
        self.uis.append({"ui" : label_divLine1, "pos" : [230, 130, 300, 10]})
#------------------------------------------------------------------------------------------
        btn_save = QPushButton("Save", self)
        btn_save.setGeometry(self.width - 90, 150, 80, 30)
        btn_save.clicked.connect(self.SaveBtn)
        self.uis.append({"ui" : btn_save, "pos" : [90, 150, 80, 30]})

        btn_load = QPushButton("불러오기", self)
        btn_load.setGeometry(self.width - 90, 190, 80, 30)
        btn_load.clicked.connect(self.LoadBtn)
        self.uis.append({"ui" : btn_load, "pos" : [90, 190, 80, 30]})

        self.filename = QLineEdit(self)
        self.filename.setGeometry(self.width - 220, 150, 120, 30)
        self.uis.append({"ui" : self.filename, "pos" : [220, 150, 120, 30]})

        self.takefile = QLineEdit(self)
        self.takefile.setGeometry(self.width - 220, 190, 120, 30)
        self.uis.append({"ui" : self.takefile, "pos" : [220, 190, 120, 30]})

        label_divLine2 = QLabel("-" * 70, self)
        label_divLine2.setGeometry(self.width - 220, 230, 300, 10)
        self.uis.append({"ui" : label_divLine2, "pos" : [220, 230, 300, 10]})
#------------------------------------------------------------------------------------------
        btn_mapSize = QPushButton('Size', self)
        btn_mapSize.setGeometry(self.width - 220, 250, 70, 70)
        btn_mapSize.clicked.connect(self.SetMapSize)
        self.uis.append({"ui" : btn_mapSize, "pos" : [220, 250, 70, 70]})

        self.line_width = QLineEdit("40", self)
        self.line_width.setGeometry(self.width - 140, 250, 120, 30)
        self.line_width.setValidator(QIntValidator())
        self.uis.append({"ui" : self.line_width, "pos" : [140, 250, 120, 30]})

        self.line_height = QLineEdit("40", self)
        self.line_height.setGeometry(self.width - 140, 290, 120, 30)
        self.line_height.setValidator(QIntValidator())
        self.uis.append({"ui" : self.line_height, "pos" : [140, 290, 120, 30]})

        self.btn_blockSelect = QPushButton('', self)
        self.btn_blockSelect.setGeometry(self.width - 290, 10, 60, 60)
        self.btn_blockSelect.setIcon(QtGui.QIcon("Textures/Block_1.png"))
        self.btn_blockSelect.setIconSize(QtCore.QSize(50, 50))
        self.btn_blockSelect.clicked.connect(self.BlockSelectBtn)
        self.uis.append({"ui" : self.btn_blockSelect, "pos" : [290, 10, 60, 60]})

    def SpeedBtn(self):
        Manager.speed = int(self.line_speed.text())
        print("Set speed : %d" %(Manager.speed))

    def JumpBtn(self):
        Manager.jump = int(self.line_jump.text())
        print("Set jump : %d" %(Manager.jump))

    def GravityBtn(self):
        Manager.gravity = float(self.line_gravity.text())
        print("Set gravity : %f" %(Manager.gravity))

    def MarioSelectBtn(self):
        Manager.charactorID = (Manager.charactorID) % 7 + 1
        self.btn_marioSelect.setIcon(QtGui.QIcon("Textures/StateL_1%d.png" % (Manager.charactorID)))
        print("Set marioID : %d" %(Manager.charactorID))
        
    def BlockSelectBtn(self):
        Manager.blockID = (Manager.blockID + 1) % 6
        self.btn_blockSelect.setIcon(QtGui.QIcon("Textures/Block_%d.png" % (Manager.blockID)))
        print("Set blockID : %d" %(Manager.blockID))

    def SaveBtn(self):
        self.map.Save(self.filename.text())
        print("Set Size %d %d" %(self.map.mx, self.map.my))

    def LoadBtn(self):
        self.map.Load(self.takefile.text())
        #self.mario.sprite.deleteLater()
        #self.mario = Mario(self, self.map)
        for mario in self.marios:
            mario.x = self.width * 0.5
            mario.y = 10
            mario.velocity = -0.1
            mario.sprite.raise_()
        for ui in self.uis:
            ui["ui"].raise_()
            ui["ui"].setGeometry(self.width - ui["pos"][0], ui["pos"][1], ui["pos"][2], ui["pos"][3])

    def SetMapSize(self):

        d = [[0] * int(self.line_width.text()) for i in range(int(self.line_height.text()))]
        for x in range(int(self.line_width.text())):
            d[0][x] = 1
        self.map.CreateMap(d)
        #self.mario.sprite.deleteLater()
        #self.mario = Mario(self, self.map)
        for mario in self.marios:
            mario.x = self.width * 0.5
            mario.y = 10
            mario.velocity = -0.1
            mario.sprite.raise_()
        for ui in self.uis:
            ui["ui"].raise_()
            ui["ui"].setGeometry(self.width - ui["pos"][0], ui["pos"][1], ui["pos"][2], ui["pos"][3])

    def keyPressEvent(self, e):
        self.key.append(e.key())
        #self.mario.KeyPressEvent(e)

        if(e.key() == Qt.Key_Q):
            for ui in self.uis:
                ui["ui"].setVisible(True)
        if(e.key() == Qt.Key_E):
            for ui in self.uis:
                ui["ui"].setVisible(False)

    def keyReleaseEvent(self, e):
        if(e.key() in self.key):
            self.key.remove(e.key())

    def mousePressEvent(self, e):
        self.mouseX = e.pos().x()
        self.mouseY = e.pos().y()
        if(e.button() == Qt.RightButton):
            self.BlockSelectBtn()
        elif(e.button() == Qt.LeftButton):
            self.mouseDown = True
    
    def mouseMoveEvent(self, e):
        self.mouseX = e.pos().x()
        self.mouseY = e.pos().y()

    def mouseReleaseEvent(self, e):
        if(e.button() == Qt.LeftButton):
            self.mouseDown = False

    def closeEvent(self, e):
        self.ed = True