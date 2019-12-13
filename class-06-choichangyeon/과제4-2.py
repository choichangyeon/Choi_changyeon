from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLineEdit, QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout

from keypad1 import numPadList, operatorList



class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calculator(QWidget):


    def __init__(self, parent=None):
        super().__init__(parent)

        # Display Window
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        # Button Creation and Placement
        numLayout = QGridLayout()
        opLayout = QGridLayout()

        buttonGroups = {
            'num': {'buttons': numPadList, 'layout': numLayout, 'columns': 3},
            'op': {'buttons': operatorList, 'layout': opLayout, 'columns': 2}
        }

        for label in buttonGroups.keys():
            r = 0; c = 0
            buttonpad =buttonGroups[label]
            for btnText in buttonpad['buttons']:
                button = Button(btnText, self.buttonClicked)
                buttonpad['layout'].addWidget(button,r,c)
                c += 1
                if c >= buttonpad['columns']:
                    c = 0; r += 1

        # r = 0; c = 0
        # for btnText in numPadList:
        #     button = Button(btnText, self.buttonClicked)
        #     numLayout.addWidget(button, r, c)
        #     c += 1
        #     if c > 2:
        #         c = 0; r += 1
        #
        # # Operator Buttons
        # r = 0; c = 0
        # for btnText in operatorList:
        #     button = Button(btnText, self.buttonClicked)
        #     opLayout.addWidget(button, r, c)
        #     c += 1
        #     if c > 1:
        #         c = 0; r += 1

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 2)
        mainLayout.addLayout(numLayout, 1, 0)
        mainLayout.addLayout(opLayout, 1, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("My Calculator")


    def buttonClicked(self):

        button = self.sender()
        key = button.text()
        if key == '=':
            try:
                result = str(eval(self.display.text()))
            except Exception as e:
                print(e)
                result = 'Error!'
            self.display.setText(result)
        elif key == 'C':
            self.display.setText('')
        else:
            self.display.setText(self.display.text() + key)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

