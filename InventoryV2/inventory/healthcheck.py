import os
import sys,getpass
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets , QtGui
from PyQt5.QtGui import QPageSize,QPageLayout
from PyQt5.QtCore import *
import configparser
config = configparser.ConfigParser()
configfile = os.environ['AppData'] + '\\InventoryV2Config.ini'
config.read(configfile)
exportdirectory = config['defaults']['exportdirectory']
class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1600, 1000)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWebEngineWidgets.QWebEngineView(Form)
        self.widget.setObjectName("widget")
        self.widget.setZoomFactor(1)
        self.uname=getpass.getuser()
        self.htmlfile="C:/Users/{}/{}/{}_healthcheck.html".format(self.uname,exportdirectory,self.uname)
        self.PDFfile="C:/Users/{}/{}/{}_healthcheck.pdf".format(self.uname,exportdirectory,self.uname)
        self.widget.load(QtCore.QUrl(self.htmlfile))
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.savebtn = QtWidgets.QPushButton(Form)
        self.savebtn.setObjectName("savebtn")
        self.horizontalLayout.addWidget(self.savebtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        self.savebtn.clicked.connect(self.saveclicked)
        QtCore.QMetaObject.connectSlotsByName(Form)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "HealthCheck Report"))
        self.savebtn.setText(_translate("Form", "Save As PDF"))
    def saveclicked(self):
        ps = QPageSize(QtGui.QPageSize.A3)
        pl = QPageLayout(ps, QPageLayout.Portrait, QtCore.QMarginsF())
        self.widget.page().printToPdf(self.PDFfile, pageLayout=pl)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
