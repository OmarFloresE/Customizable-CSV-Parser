from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTableWidget,\
    QVBoxLayout, QDialog, QTabWidget, QTableWidgetItem, QLineEdit, QAction, \
    QAbstractItemView, QHeaderView, QPushButton, QHBoxLayout, QLabel, QMainWindow, QFileDialog, \
    QInputDialog
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon

import typing
import sys
import csv


class MyWindow(QMainWindow):
    def __init__(self, Form):
        QDialog.__init__(self)


        self.setWindowTitle("Load CSV File")

        Form.setObjectName("Form")
        # Form.resize(519, 344)
        self.loadButton = QPushButton(Form)
        self.input = QLineEdit()
        # self.input.textChanged.connect(self.setText)

        layout = QHBoxLayout()
        
        layout.addWidget(self.input)
        layout.addWidget(self.loadButton)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form","Form"))
        self.loadButton.setText(_translate("Form", "Browse File"))
        self.loadButton.clicked.connect(self.loadButton_handler)

    def loadButton_handler(self):
        print("Load Initiated")
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        print(path)

        self.data = []
        with open(path, 'r') as infile:
            csv_reader = csv.reader(infile, delimiter=",")
            self.data = list(csv_reader)    # Easier to work with as a list for some reason.
        return self.data



def main():
    app = QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    w = MyWindow(Form)
    w.resize(1100,900)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
