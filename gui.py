from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QLabel
import sys

class Dialer(QWidget):

    def __init__(self):
        super(Dialer, self).__init__()
        
        self.initUI()

    def initUI(self):
        
        self.num_to_dial = []
        self.num_bar = QLabel(''.join(self.num_to_dial), self)
        button1 = QPushButton(str(1), self)
        button1.move(30, 50)
        button2 = QPushButton(str(2), self)
        button2.move(150, 50)
        button3 = QPushButton(str(3), self)
        button3.move(270, 50)
        button4 = QPushButton(str(4), self)
        button4.move(30, 100)
        button5 = QPushButton(str(5), self)
        button5.move(150, 100)
        button6 = QPushButton(str(6), self)
        button6.move(270, 100)
        button7 = QPushButton(str(7), self)
        button7.move(30, 150)
        button8 = QPushButton(str(8), self)
        button8.move(150, 150)
        button9 = QPushButton(str(9), self)
        button9.move(270, 150)
        button0 = QPushButton(str(0), self)
        button0.move(150, 200)

        button1.clicked.connect(self.on_button_click)
        button2.clicked.connect(self.on_button_click)
        button3.clicked.connect(self.on_button_click)
        button4.clicked.connect(self.on_button_click)
        button5.clicked.connect(self.on_button_click)
        button6.clicked.connect(self.on_button_click)
        button7.clicked.connect(self.on_button_click)
        button8.clicked.connect(self.on_button_click)
        button9.clicked.connect(self.on_button_click)
        button0.clicked.connect(self.on_button_click)

        self.setGeometry(300, 300, 300, 300)
        self.show()
        #self.showFullScreen()

    def on_button_click(self, pressed):
        
        sender = self.sender()
        self.num_to_dial.append(sender.text())
        dial = ''.join(self.num_to_dial)
        self.num_bar.setText(dial)
        self.num_bar.adjustSize()

