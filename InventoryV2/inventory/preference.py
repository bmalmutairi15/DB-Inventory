'''
LGPL License
Copyright (c) [2021] [bmalmutairi15@gmail.com]
'''
from PySide2 import QtCore, QtWidgets
import configparser
import os
from cryptography.fernet import Fernet
config = configparser.ConfigParser()
global conffile
conffile=os.environ['AppData']+'\\InventoryV2Config.ini'


# noinspection PyArgumentList
class Ui_Dialog2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(567, 423)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 380, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 10, 541, 371))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        #self.themeinput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        #self.themeinput.setObjectName("themeinput")
        #self.gridLayout.addWidget(self.themeinput, 0, 1, 1, 1)
        themes=['light','dark','darkorange','darkblue']

        self.themeinput = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.themeinput.addItems(themes)
        self.themeinput.setObjectName("themeinput")
        self.gridLayout.addWidget(self.themeinput, 0, 1, 1, 1)
        # add editline for user entry
        self.winHinput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.winHinput.setObjectName("winHinput")
        self.gridLayout.addWidget(self.winHinput, 1, 1, 1, 1)
        self.winWinput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.winWinput.setObjectName("winWinput")
        self.gridLayout.addWidget(self.winWinput, 2, 1, 1, 1)
        self.tblHinput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.tblHinput.setObjectName("tblHinput")
        self.gridLayout.addWidget(self.tblHinput, 3, 1, 1, 1)
        self.tblWinput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.tblWinput.setObjectName("tblWinput")
        self.gridLayout.addWidget(self.tblWinput, 4, 1, 1, 1)
        self.pwdinputP = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.pwdinputP.setObjectName("pwdinputP")
        self.gridLayout.addWidget(self.pwdinputP, 5, 1, 1, 1)
        self.exportinput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.exportinput.setObjectName("exportinput")
        self.gridLayout.addWidget(self.exportinput, 6, 1, 1, 1)
        '''
        self.UseNativeBrowserinput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.UseNativeBrowserinput.setObjectName("exportinput")
        self.gridLayout.addWidget(self.UseNativeBrowserinput, 7, 1, 1, 1)
        '''
        # add labels
        self.themeoptionlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.themeoptionlabel.setObjectName("themeoptionlabel")
        self.gridLayout.addWidget(self.themeoptionlabel, 0, 0, 1, 1)
        self.winHoptionlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.winHoptionlabel.setObjectName("winHoptionlabel")
        self.gridLayout.addWidget(self.winHoptionlabel, 1, 0, 1, 1)
        self.WinWoptionlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.WinWoptionlabel.setObjectName("WinWoptionlabel")
        self.gridLayout.addWidget(self.WinWoptionlabel, 2, 0, 1, 1)
        self.tblHoptionlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.tblHoptionlabel.setObjectName("tblHoptionlabel")
        self.gridLayout.addWidget(self.tblHoptionlabel, 3, 0, 1, 1)
        self.tblWoptionlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.tblWoptionlabel.setObjectName("tblWoptionlabel")
        self.gridLayout.addWidget(self.tblWoptionlabel, 4, 0, 1, 1)
        self.PWDoptionlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.PWDoptionlabel.setObjectName("PWDoptionlabel")
        self.gridLayout.addWidget(self.PWDoptionlabel, 5, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 6, 0, 1, 1)
        '''
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        '''
        # add buttons
        self.themebtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.savetheme())
        self.themebtn.setObjectName("themebtn")
        self.gridLayout.addWidget(self.themebtn, 0, 2, 1, 1)
        self.winHbtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.savewinH())
        self.winHbtn.setObjectName("winHbtn")
        self.gridLayout.addWidget(self.winHbtn, 1, 2, 1, 1)
        self.winWbtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.savewinW())
        self.winWbtn.setObjectName("winWbtn")
        self.gridLayout.addWidget(self.winWbtn, 2, 2, 1, 1)
        self.tblHbtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.savetblH())
        self.tblHbtn.setObjectName("tblHbtn")
        self.gridLayout.addWidget(self.tblHbtn, 3, 2, 1, 1)
        self.tblWbtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.savetblW())
        self.tblWbtn.setObjectName("tblWbtn")
        self.gridLayout.addWidget(self.tblWbtn, 4, 2, 1, 1)
        self.PWDbtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.savePWD())
        self.PWDbtn.setObjectName("PWDbtn")
        self.gridLayout.addWidget(self.PWDbtn, 5, 2, 1, 1)
        self.Exportfilebtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.saveexportpath())
        self.Exportfilebtn.setEnabled(True)
        self.Exportfilebtn.setObjectName("Exportfilebtn")
        self.gridLayout.addWidget(self.Exportfilebtn, 6, 2, 1, 1)
        '''
        self.UseNativeBrowserbtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked= lambda : self.saveUseNativeBrowser())
        self.UseNativeBrowserbtn.setEnabled(True)
        self.UseNativeBrowserbtn.setObjectName("UseNativeBrowserbtn")
        self.gridLayout.addWidget(self.UseNativeBrowserbtn, 7, 2, 1, 1)
        '''
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.winHoptionlabel.setText(_translate("Dialog", "Window Height"))
        self.tblHoptionlabel.setText(_translate("Dialog", "Table Height"))
        self.label_8.setText(_translate("Dialog", "Default Directory"))
        #self.label_9.setText(_translate("Dialog", "Native Browser"))
        self.themeoptionlabel.setText(_translate("Dialog", "Theme"))
        self.WinWoptionlabel.setText(_translate("Dialog", "Window Width"))
        self.tblWoptionlabel.setText(_translate("Dialog", "Table Width"))
        self.PWDoptionlabel.setText(_translate("Dialog", "PWD"))
        self.themebtn.setText(_translate("Dialog", "Save"))
        self.winHbtn.setText(_translate("Dialog", "Save"))
        self.winWbtn.setText(_translate("Dialog", "Save"))
        self.tblHbtn.setText(_translate("Dialog", "Save"))
        self.tblWbtn.setText(_translate("Dialog", "Save"))
        self.PWDbtn.setText(_translate("Dialog", "Save"))
        #self.UseNativeBrowserbtn.setText(_translate("Dialog", "Save"))
        self.Exportfilebtn.setText(_translate("Dialog", "Save"))
        self.pwdinputP.setPlaceholderText('symmetric key cryptography is used')
        self.pwdinputP.setEchoMode(QtWidgets.QLineEdit.Password)
        self.themeinput.setPlaceholderText('dark/light')
        self.winHinput.setPlaceholderText('1030')
        self.winWinput.setPlaceholderText('1900')
        self.tblHinput.setPlaceholderText('930')
        self.tblWinput.setPlaceholderText('1870')
        self.exportinput.setPlaceholderText('Documents')
        #self.UseNativeBrowserinput.setPlaceholderText('1')

    def savetheme(self):
        #newval=self.themeinput.text()
        newval=str(self.themeinput.currentText())
        config.read(conffile)
        config['defaults']['theme']=newval
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)
    def savewinH(self):
        newval=self.winHinput.text()
        config.read(conffile)
        config['defaults']['winheight']=newval
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)
    def savewinW(self):
        newval=self.winWinput.text()
        config.read(conffile)
        config['defaults']['winwidth']=newval
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)
    def savetblH(self):
        newval=self.tblHinput.text()
        config.read(conffile)
        config['defaults']['tblframeheight']=newval
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)
    def savetblW(self):
        newval=self.tblWinput.text()
        config.read(conffile)
        config['defaults']['tblframewidth']=newval
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)
    #UseNativeBrowser
    '''
    def saveUseNativeBrowser(self):
        newval=self.UseNativeBrowserinput.text()
        config.read(conffile)
        config['defaults']['UseNativeBrowser']=newval
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)
    '''
    def savePWD(self):
        newval=self.pwdinputP.text()
        config.read(conffile)
        k=config['optional']['k']
        fernet = Fernet(k)
        newval1=str(fernet.encrypt(newval.encode()))
        config['optional']['pwd']=newval1
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)
    def saveexportpath(self):
        newval=self.exportinput.text()
        config.read(conffile)
        config['defaults']['exportdirectory']=newval
        with open(conffile, 'w') as configfile:    # save
             config.write(configfile)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui2 = Ui_Dialog2()
    ui2.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
