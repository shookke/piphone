from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QLabel
import sys

class Dialer(QWidget):

    def __init__(self):
        super(Dialer, self).__init__()
        
        self.initUI()

    def initUI(self):
        
        self.num_to_dial = []
        self.num_bar = QLabel(''.join(self.num_to_dial))
        button1 = QPushButton(str(1), self)
        button1.clicked.connect(self.on_button_click)
        button2 = QPushButton(str(2), self)
        button2.clicked.connect(self.on_button_click)
        button3 = QPushButton(str(3), self)
        button3.clicked.connect(self.on_button_click)
        button4 = QPushButton(str(4), self)
        button4.clicked.connect(self.on_button_click)
        button5 = QPushButton(str(5), self)
        button5.clicked.connect(self.on_button_click)
        button6 = QPushButton(str(6), self)
        button6.clicked.connect(self.on_button_click)
        button7 = QPushButton(str(7), self)
        button7.clicked.connect(self.on_button_click)
        button8 = QPushButton(str(8), self)
        button8.clicked.connect(self.on_button_click)
        button9 = QPushButton(str(9), self)
        button9.clicked.connect(self.on_button_click)
        button0 = QPushButton(str(0), self)
        button0.clicked.connect(self.on_button_click)

        self.show()
        #self.showFullScreen()

    def on_button_click(self, pressed):
        
        sender = self.sender()
        self.num_to_dial.append(sender.text())
        dial = ''.join(self.num_to_dial)
        self.num_bar.setText(dial)

