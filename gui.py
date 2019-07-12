from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QLabel
import sys

class Dialer(QWidget):

    def __init__(self, sip):
        super(Dialer, self).__init__()
        self.sip = sip
        self.call = None
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
        self.buttonCall = QPushButton("Call", self)
        self.buttonCall.move(270, 200)
        self.buttonClear = QPushButton("Clear", self)
        self.buttonClear.move(30, 200)

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
        self.buttonCall.clicked.connect(self.make_call)
        self.buttonClear.clicked.connect(self.clear)

        self.setGeometry(300, 300, 400, 300)
        self.show()
        #self.showFullScreen()

    def on_button_click(self, pressed):
        
        sender = self.sender()
        self.num_to_dial.append(sender.text())
        dial = ''.join(self.num_to_dial)
        self.num_bar.setText(dial)
        self.num_bar.adjustSize()

    def make_call(self, pressed):
        if self.buttonCall.text() == "Call":
            self.call = self.sip.invite("sip:" + self.num_bar.text() + "@shookke.fl.3cx.us")
            self.buttonCall.setText('End')
        else:
            self.end_call()

    def end_call(self):
        self.sip.terminate_call(self.call)
        self.buttonCall.setText('Call')
        self.clear()
        self.buttonCall.clicked.connect(self.make_call)
        self.buttonClear.clicked.connect(self.clear)

    def clear(self):
        self.num_bar.setText('')
        self.num_to_dial = []

    def call_incoming(self):
        self.buttonClear.setText('Ignore')
        self.buttonClear.clicked.connect(self.endcall)
        self.buttonCall.setText('Answer')
        self.buttonCall.clicked.connect(self.make_call)

    

