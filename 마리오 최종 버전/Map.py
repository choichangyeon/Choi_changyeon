from Block import Block
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QPixmap

class Map:
    def __init__(self, main):
        self.main = main

        self.pixmaps = []
        for i in range(7):
            self.pixmaps.append(QPixmap("Textures/Block_%d.png" %(i)))
        
        self.data = [[0] * 20 for i in range(20)]
        self.blocks = [[0] * 0 for i in range(0)]
        self.CreateMap(self.data)


    def CreateMap(self, data):
        self.data = data
        self.SetGeometry(len(data[0]), len(data))

        for col in self.blocks:
            for block in col:
                block.sprite.deleteLater()

        self.blocks = [[0] * self.mx for i in range(self.my)]
        for y in range(self.my):
            for x in range(self.mx):
                self.blocks[y][x] = Block(self.main, self.pixmaps[self.data[y][x]], x * 16, self.main.height - 16 - (y * 16))

    def SetGeometry(self, x, y):
        self.mx = x
        self.my = y
        self.main.width = x * 16
        self.main.height = y * 16
        self.main.setGeometry(10, 10, self.main.width, self.main.height)
        #SetGeometry End

    def Change(self, x, y, id):
        ix = int(x / 16)
        iy = int(y / 16)

        if(ix < 0 or ix >= self.mx or iy <= 0 or iy > self.my):
            return

        self.data[self.my - iy][ix] = id
        self.blocks[self.my - iy][ix].SetTexture(self.pixmaps[id])

    def IsBlock(self, x, y):
        ix = int(x / 16)
        iy = int((self.main.height - y) / 16)

        if(ix < 0 or ix >= self.mx or iy < 0 or iy >= self.my):
            return True

        if(iy < 0):
            return False

        if(self.data[iy][ix] == 0):
            return True
        else:
            return False

    def Save(self, name):
        mariomap = open("Map/%s.map" %(name), "w+")
        mariomap.write("%d %d\n" %(self.mx, self.my))
        for y in range(self.my):
            for x in range(self.mx):
                mariomap.write(str(self.data[y][x]))
            mariomap.write("\n")
        mariomap.close()
        print("Save : %s" %(name))

    def Load(self, name):
        mariomap = open("Map/%s.map" %(name), "r")

        data = mariomap.readline().split()
        self.mx = int(data[0])
        self.my = int(data[1])
        data = [[0] * self.mx for i in range(self.my)]
        
        for y in range(self.my):
            line = mariomap.readline()
            for x in range(self.mx):
                data[y][x] = int(line[x])

        self.CreateMap(data)
        print("Load : %s" %(name))