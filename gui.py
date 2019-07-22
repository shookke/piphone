from PyQt5.QtWidgets import QStyle, QWidget, QPushButton, QFrame, QLabel, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
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
        self.button_size = QtCore.QSize()
        self.button_size.setHeight(80)
        self.button_size.setWidth(80)
        self.createGridLayout()

        self.windowLayout = QVBoxLayout()
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.windowLayout)

        self.show()
        #self.showFullScreen()
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)
        #lcd = QLCDNumber(self)
        self.ui_font = QtGui.QFont("Arial", 25, QtGui.QFont.Bold)
        self.num_to_dial = []
        self.num_bar = QLabel(''.join(self.num_to_dial), self)
        self.num_bar.setAlignment(QtCore.Qt.AlignRight)
        self.num_bar.setFont(self.ui_font)
        self.cursor = QtGui.QCursor(QtCore.Qt.BlankCursor)
        layout.addWidget(self.num_bar, 0,0,1,3, self.num_bar.alignment())
        button1 = QPushButton('1', self)
        button1.setMinimumSize(120,80)
        layout.addWidget(button1,1,0)
        button2 = QPushButton('2', self)
        button2.setMinimumSize(120,80)
        layout.addWidget(button2,1,1)
        button3 = QPushButton('3', self)
        button3.setMinimumSize(120,80)
        layout.addWidget(button3,1,2)
        button4 = QPushButton('4', self)
        button4.setMinimumSize(80,80)
        layout.addWidget(button4,2,0)
        button5 = QPushButton('5', self)
        button5.setMinimumSize(80,80)
        layout.addWidget(button5,2,1)
        button6 = QPushButton('6', self)
        button6.setMinimumSize(80,80)
        layout.addWidget(button6,2,2)
        button7 = QPushButton('7', self)
        button7.setMinimumSize(80,80)
        layout.addWidget(button7,3,0)
        button8 = QPushButton('8', self)
        button8.setMinimumSize(80,80)
        layout.addWidget(button8,3,1)
        button9 = QPushButton('9', self)
        button9.setMinimumSize(80,80)
        layout.addWidget(button9,3,2)
        button_astr = QPushButton('*', self)
        button_astr.setMinimumSize(80,80)
        layout.addWidget(button_astr,4,0)
        button0 = QPushButton('0', self)
        button0.setMinimumSize(80,80)
        layout.addWidget(button0,4,1)
        button_hash = QPushButton('#', self)
        button_hash.setMinimumSize(80,80)
        layout.addWidget(button_hash,4,2)

        self.buttonCall = QPushButton("Call", self)
        self.buttonCall.setMinimumSize(80,80)
        layout.addWidget(self.buttonCall,5,2)
        self.buttonClear = QPushButton("Clear", self)
        self.buttonClear.setMinimumSize(80,80)
        layout.addWidget(self.buttonClear,5,0)

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
            #self.sip.start_dtmf_stream()
            self.sip.play_dtmf(int(sender.text()), 1000)
            #print (int(sender.text()))
            #self.sip.stop_dtmf_stream()



    def make_call(self):
        self.call = self.sip.invite("sip:" + self.num_bar.text() + "@shookke.fl.3cx.us")
        self.buttonCall.setText('End')
        
    def answer_call(self):
        self.sip.accept_call(self.call)
        self.buttonCall.setText('End')
        self.buttonClear.setText('Clear')

    def end_call(self):
        self.sip.terminate_call(self.call)
        self.call = None
        self.call_state = 0
        self.clear()
        self.buttonCall.setText('Call')
        
    
    def decline_call(self):
        self.sip.decline_call(self.call, linphone.Reason.Declined)

    def clear(self):
        sender = self.sender()
        if sender.text() == 'Ignore':
            self.decline_call()
        self.num_bar.setText('')
        self.num_to_dial = []

    def call_incoming(self, call):
        self.call = call
        self.call_state = self.call.state
        self.num_bar.setText(self.call.user_data)
        self.num_bar.adjustSize()
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
        elif self.call_state == 3:
            self.end_call()
        elif self.call_state == 6:
            self.end_call()
        else:
            return
