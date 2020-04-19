from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QPixmap

class Block:
    def __init__(self, main, tex, x, y):
        self.sprite = QLabel(main)
        self.sprite.show()
        self.sprite.setGeometry(x, y, 16, 16)
        self.SetTexture(tex)

    def SetTexture(self, tex):
        self.sprite.setPixmap(tex)