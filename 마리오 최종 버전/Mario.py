from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
import time
import threading
from random import *
from Manager import Manager

class Mario:

    def __init__(self):        
        self.x = Manager.main.width / 2
        self.y = 10
        self.velocity = -0.1
        self.direct = "L"
        self.lastTime = time.time()
        self.spriteTime = time.time()
        self.spriteIndex = 0

        self.sprite = QLabel(Manager.main)  
        self.sprite.setPixmap(QPixmap("Textures/StateR_11.png"))
        self.sprite.show()
        self.sprite.setGeometry(self.x, self.y, 16, 32)
        self.textureFile = "Textures/StateR_11.png"
        
        self.aiState = 1
        self.aiTime = 0
        self.lastTime = time.time()
        self.aiMoveTime = time.time()
        self.aiJumpTime = time.time()
        self.aiMoveRange = 0
        self.aiJumpRange = 0

    def UpdateFixed(self):
        #deltaTime 계산
        deltaTime = time.time() - self.lastTime
        self.lastTime = time.time()

        if(not Manager.map.IsBlock(self.x + 14, self.y + self.velocity)):
            self.velocity = -0.1
            Manager.map.Change((self.x + 14), (self.y + self.velocity), 0)
        if(not Manager.map.IsBlock(self.x + 1, self.y + self.velocity)):
            self.velocity = -0.01
            Manager.map.Change((self.x + 1), (self.y + self.velocity), 0)

        #velocity 계산 (중력 계산)
        if(Manager.map.IsBlock(self.x + 14, self.y + self.velocity + 31) and Manager.map.IsBlock(self.x + 1, self.y + self.velocity + 31)):   #장애물 되돌리기
            self.velocity += 9.8 * Manager.gravity * 0.00001 
            self.y += self.velocity
        else:
            self.velocity = 0

        speed = Manager.speed * deltaTime
        if(Qt.Key_S in Manager.main.key):
            pass
        elif(Qt.Key_D in Manager.main.key):
            self.direct = "L"
            if(Manager.map.IsBlock(self.x + 16 + speed, self.y + 30) and Manager.map.IsBlock(self.x + 16 + speed, self.y) and Manager.map.IsBlock(self.x + 16 + speed, self.y + 15)):
                self.x += speed
        elif(Qt.Key_A in Manager.main.key):
            self.direct = "R"
            if(Manager.map.IsBlock(self.x - speed, self.y + 30) and Manager.map.IsBlock(self.x - speed, self.y) and Manager.map.IsBlock(self.x - speed, self.y + 15)):
                self.x -= speed
        elif(self.aiState == 1):
            self.direct == "L"
            if(Manager.map.IsBlock(self.x + 16 + speed, self.y + 30) and Manager.map.IsBlock(self.x + 16 + speed, self.y) and Manager.map.IsBlock(self.x + 16 + speed, self.y + 15)):
                self.x += speed
        elif(self.aiState == 2):
            self.direct = "R"
            if(Manager.map.IsBlock(self.x - speed, self.y + 30) and Manager.map.IsBlock(self.x - speed, self.y) and Manager.map.IsBlock(self.x - speed, self.y + 15)):
                self.x -= speed
        self.sprite.setGeometry(self.x, self.y, 16, 32)

    def UpdateSprite(self):
        if(time.time() - self.spriteTime > 0.1):
            self.spriteIndex = (self.spriteIndex + 1) % 3
            self.spriteTime += 0.1
        textureFile = "Textures/"
        if(Qt.Key_S in Manager.main.key and self.direct == "L"):
            textureFile += "DownL_1%d" %(Manager.charactorID)
        elif(Qt.Key_S in Manager.main.key):
            textureFile += "DownR_1%d" %(Manager.charactorID)
        elif(self.aiState == 1 and self.velocity != 0):
            textureFile += "JumpL_1%d.png" %(Manager.charactorID)
        elif(self.aiState == 2 and self.velocity != 0):
            textureFile += "JumpR_1%d.png" %(Manager.charactorID)
        elif(Qt.Key_D in Manager.main.key or self.aiState == 1):
            textureFile += "RunL_1%d_%d.png" %(Manager.charactorID ,self.spriteIndex)
        elif(Qt.Key_A in Manager.main.key or self.aiState == 2):
            textureFile += "RunR_1%d_%d.png" %(Manager.charactorID, self.spriteIndex)
        elif(self.direct == "L"):
            textureFile += "StateL_1%d.png" %(Manager.charactorID)
        else:#(self.direct == "R"):
            textureFile += "StateR_1%d.png" %(Manager.charactorID)

        try:
            if(self.textureFile != textureFile):
               self.sprite.setPixmap(QPixmap(textureFile))
               self.textureFile = textureFile
        except:
            print("b")
        
    def UpdateAI(self):
        if(time.time() - self.aiMoveTime > self.aiMoveRange):
            self.aiMoveRange =  randrange(5, 30) * 0.1
            self.aiMoveTime = time.time()
            self.aiState += 1
            if(self.aiState == 3):
                self.aiState = 1
        
        if(time.time() - self.aiJumpTime > self.aiJumpRange):
            self.aiJumpRange = randrange(5, 20) * 0.1
            self.aiJumpTime = time.time()
            #if(self.velocity == 0):
            #    self.velocity = -Manager.jump

    def KeyPressEvent(self, e):
        #점프
        if(e.key() == Qt.Key_F and self.velocity == 0):
            self.velocity = -Manager.jump
        if(e.key() == Qt.Key_R):
            self.x = self.Manager.width / 2
            self.y = 10
            self.velocity = -0.1