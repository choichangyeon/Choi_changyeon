import sys
from Scene import Scene
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Scene()
    sys.exit(app.exec_())