from email.charset import QP
from tkinter import Button
from PyQt5.QtWidgets import *

def onButtonClicked():
    alert = QMessageBox()
    alert.setText("You clicked me!!")
    alert.exec_()

app = QApplication([])
window = QWidget()
button = QPushButton("Click Me!!")
button.clicked.connect(onButtonClicked)
layout = QVBoxLayout()
layout.addWidget(QPushButton("Top"))
layout.addWidget(QPushButton("Bottom"))
layout.addWidget(button)

window.setLayout(layout)
window.show()
app.exec_()