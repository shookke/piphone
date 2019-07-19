from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QLabel, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5 import QtGui, QtCore
import sys
import linphone

class Dialer(QWidget):

    def __init__(self, sip):
        super(Dialer, self).__init__()
        self.sip = sip
        self.call = None
        self.call_state = 0
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createGridLayout()

        self.windowLayout = QVBoxLayout()
        #self.windowLayout.addWidget(self.displayBox)
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.windowLayout)

        self.show()
        #self.showFullScreen()
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        #lcd = QLCDNumber(self)

        self.num_to_dial = []
        self.num_bar = QLabel(''.join(self.num_to_dial), self)
        self.cursor = QtGui.QCursor(QtCore.Qt.BlankCursor)

        button1 = QPushButton('1', self)
        layout.addWidget(button1,0,0)
        button2 = QPushButton('2', self)
        layout.addWidget(button2,0,1)
        button3 = QPushButton('3', self)
        layout.addWidget(button3,0,2)
        button4 = QPushButton('4', self)
        layout.addWidget(button4,1,0)
        button5 = QPushButton('5', self)
        layout.addWidget(button5,1,1)
        button6 = QPushButton('6', self)
        layout.addWidget(button6,1,2)
        button7 = QPushButton('7', self)
        layout.addWidget(button7,2,0)
        button8 = QPushButton('8', self)
        layout.addWidget(button8,2,1)
        button9 = QPushButton('9', self)
        layout.addWidget(button9,2,2)
        button_astr = QPushButton('*', self)
        layout.addWidget(button_astr,3,0)
        button0 = QPushButton('0', self)
        layout.addWidget(button0,3,1)
        button_hash = QPushButton('#', self)
        layout.addWidget(button_hash,3,2)

        self.buttonCall = QPushButton("Call", self)
        layout.addWidget(self.buttonCall,4,2)
        self.buttonClear = QPushButton("Clear", self)
        layout.addWidget(self.buttonClear,4,0)

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
        button_astr.clicked.connect(self.on_button_click)
        button_hash.clicked.connect(self.on_button_click)

        self.buttonCall.clicked.connect(self.call_handler)
        self.buttonClear.clicked.connect(self.clear)

        self.horizontalGroupBox.setLayout(layout)

    def on_button_click(self, pressed):
        sender = self.sender()
        self.num_to_dial.append(sender.text())
        dial = ''.join(self.num_to_dial)
        self.num_bar.setText(dial)
        self.num_bar.adjustSize()
        if self.call_state == 6:
            self.call.send_dtmf(sender.text())



    def make_call(self):
        self.call = self.sip.invite("sip:" + self.num_bar.text() + "@shookke.fl.3cx.us")
        #self.buttonCall.clicked.connect(self.end_call)
        self.buttonCall.setText('End')
        
    def answer_call(self):
        self.sip.accept_call(self.call)
        #self.buttonCall.clicked.connect(self.end_call)
        self.buttonCall.setText('End')
        self.buttonClear.setText('Clear')

    def end_call(self):
        self.sip.terminate_call(self.call)
        self.call = None
        self.call_state = 0
        self.clear()
        #self.buttonCall.clicked.connect(self.make_call)
        #self.buttonClear.clicked.connect(self.clear)
        self.buttonCall.setText('Call')
        
    
    def decline_call(self):
        self.sip.decline_call(self.call, linphone.Reason.Declined)

    def clear(self):
        self.num_bar.setText('')
        self.num_to_dial = []

    def call_incoming(self, call):
        self.call = call
        self.call_state = self.call.state
        self.num_bar.setText(self.call.user_data)
        self.num_bar.adjustSize()
        #self.buttonClear.clicked.connect(self.decline_call)
        #self.buttonCall.clicked.connect(self.answer_call)
        self.buttonClear.setText('Ignore')
        self.buttonCall.setText('Answer')

    def incoming_terminated(self):
        self.call = None
        self.call_state = 0
        self.buttonCall.setText('Call')
        self.buttonClear.setText('Clear')

    def call_handler(self):
        if self.call_state == 1:
            self.answer_call()
        elif self.call_state == 0 and self.num_bar != '':
            self.make_call()
        elif self.call_state == 6:
            self.end_call()
        else:
            return
