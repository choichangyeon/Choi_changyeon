import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout,
                             QVBoxLayout, QApplication, QLabel,
                             QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt


class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()

    def initUI(self):
        global result_val, age_val, name_val, score_val, amount_val, key_val
        name = QLabel('Name:')
        age = QLabel('Age:')
        score = QLabel('Score:')

        name_val = QLineEdit()
        age_val = QLineEdit()
        score_val = QLineEdit()

        amount = QLabel('Amount:')
        key = QLabel('Key:')
        result = QLabel('Result:')

        add = QPushButton('Add')
        de = QPushButton('Del')
        find = QPushButton('Find')
        inc = QPushButton('Inc')
        show = QPushButton('Show')

        amount_val = QLineEdit()
        key_val = QComboBox()

        result_val = QTextEdit()

        key_val.addItem('name')
        key_val.addItem('score')
        key_val.addItem('age')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(name)
        hbox1.addWidget(name_val)
        hbox1.addWidget(age)
        hbox1.addWidget(age_val)
        hbox1.addWidget(score)
        hbox1.addWidget(score_val)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(3)
        hbox2.addWidget(amount)
        hbox2.addWidget(amount_val)
        hbox2.addWidget(key)
        hbox2.addWidget(key_val)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(add)
        hbox3.addWidget(de)
        hbox3.addWidget(find)
        hbox3.addWidget(inc)
        hbox3.addWidget(show)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(result)
        hbox4.addStretch(8)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(result_val)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)



        add.clicked.connect(self.addbtn)
        de.clicked.connect(self.delbtn)
        find.clicked.connect(self.findbtn)
        inc.clicked.connect(self.incbtn)
        show.clicked.connect(self.showbtn)


        self.setLayout(vbox)

        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Assignment6')
        self.show()

    def closeEvent(self, event):
        self.writeScoreDB()

    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH)

        except:
            pass
        else:
            pass
        fH.close()


    # write the data into person db
    def addbtn(self):
        age = int(age_val.text())
        name = name_val.text()
        score = int(score_val.text())
        add = {'Name': name, 'Age': age, 'Score': score}
        self.scoredb.append(add)                             # self.scoredb 는 list이다.
        result_val.clear()
        self.showScoreDB()

    def delbtn(self):
        name = name_val.text()
        for i in range(len(self.scoredb)):
            if self.scoredb[i]['Name'] == name:
                self.scoredb[i] = 0
        while 0 in self.scoredb:
            self.scoredb.remove(0)
        result_val.clear()
        self.showScoreDB()

    def findbtn(self):
        wait = []
        name = name_val.text()
        for i in range(len(self.scoredb)):
            if self.scoredb[i]['Name'] == name:
                wait.append(self.scoredb[i])
        result_val.clear()
        for i in range(len(wait)):
            store = "Age=%d \t Name=%s \t\t Score=%d" %(wait[i]['Age'],wait[i]['Name'],wait[i]['Score'])
            result_val.append(store)

    def incbtn(self):
        if amount_val.text() == '':
            result_val.clear()
            result_val.append("값을 넣어라")
        else:
            amount = int(amount_val.text())
            name = name_val.text()
            for i in range(len(self.scoredb)):
                if self.scoredb[i]['Name'] == name:
                    self.scoredb[i]['Score'] += amount
            result_val.clear()
            self.showScoreDB()

    def showbtn(self):
        key = key_val.currentText()
        if key == "age":
            self.scoredb = sorted(self.scoredb, key=lambda x: x['Age'])
            result_val.clear()
            self.showScoreDB()
        elif key == "score":
            self.scoredb = sorted(self.scoredb, key=lambda x: x['Score'])
            result_val.clear()
            self.showScoreDB()
        elif key == "name":
            self.scoredb = sorted(self.scoredb, key=lambda x: x['Name'])
            result_val.clear()
            self.showScoreDB()



    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    def showScoreDB(self):
        for i in range(len(self.scoredb)):
            store = "Age=%d \t Name=%s \t\t Score=%d" %(self.scoredb[i]['Age'],self.scoredb[i]['Name'],self.scoredb[i]['Score'])
            if len(self.scoredb[i]['Name']) >= 5:
                store = "Age=%d \t Name=%s \t Score=%d" %(self.scoredb[i]['Age'], self.scoredb[i]['Name'], self.scoredb[i]['Score'])
            result_val.append(store)

        pass #아무것도 동작하지 않을때


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())
