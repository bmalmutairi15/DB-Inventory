from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
#QMessageBox
import pyodbc
conn3 = pyodbc.connect("DSN=inventoryV2",timeout=1)
cursor3 = conn3.cursor()
class Ui_Dialog3(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(980, 754)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(750, 731, 220, 21))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Reset|QtWidgets.QDialogButtonBox.Save)#|QtWidgets.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 3, 700, 25))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit.setFocus()
        self.searchbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.searchbtn.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.searchbtn)
        self.deletebtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.deletebtn.setObjectName("deletebtn")
        self.horizontalLayout.addWidget(self.deletebtn)
        self.updatebtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.updatebtn.setObjectName("updatebtn")
        self.horizontalLayout.addWidget(self.updatebtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 29, 961, 701))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 346))
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(23)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        #self.buttonBox.accepted.connect(Dialog.accept)
        #self.buttonBox.accepted.connect(lambda: self.save())
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(lambda:self.resetall())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(lambda:self.save())
        #self.buttonBox.button(QtWidgets.QDialogButtonBox.Open).clicked.connect(lambda:self.show())
        self.tableWidget.clicked.connect(lambda:self.rowchange())
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.searchbtn.setText(_translate("Dialog", "Search"))
        self.deletebtn.setText(_translate("Dialog", "Delete"))
        self.updatebtn.setText(_translate("Dialog", "Update"))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText(_translate("Dialog", "New"))
        #self.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setText(_translate("Dialog", "Show"))
        self.searchbtn.clicked.connect(self.refresh)
        self.deletebtn.clicked.connect(self.delete)
        self.deletebtn.setEnabled(False)
        self.updatebtn.clicked.connect(self.update)
        self.updatebtn.setEnabled(False)
        self.lineEdit.returnPressed.connect(self.searchbtn.click)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "TAGS"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Description"))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        #self.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setEnabled(False)
    def errmsg(self, TYPE, msg):
        if TYPE == 'Warning':
            QMessageBox.warning(QtWidgets.QDialog(), "Warning", msg)
        elif TYPE == 'Information':
            QMessageBox.information(QtWidgets.QDialog(), "Information", msg)
    def refresh(self):
        try:
            del self.ID
            del self.TAGS
            del self.DESC
            del self.SCRIPTS
        except:
            pass
        try:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
            #self.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setEnabled(True)
            self.deletebtn.setEnabled(True)
            self.updatebtn.setEnabled(False)
            self.textEdit.clear()
            serachword=self.lineEdit.text().strip()
            self.tableWidget.setRowCount(0)
            cursor3.execute('sp_searchscripts ?',serachword)
            output = cursor3.fetchall()
            x=len(output)
            self.tableWidget.setRowCount(x)
            self.ID=[]
            self.TAGS=[]
            self.DESC=[]
            self.SCRIPTS=[]
            row_num=0
            for row in output:
                self.ID.append(row[0])
                self.TAGS.append(row[1])
                self.tableWidget.setItem(row_num , 0, QtWidgets.QTableWidgetItem(row[1]))
                self.DESC.append(row[2])
                self.tableWidget.setItem(row_num , 1, QtWidgets.QTableWidgetItem(row[2]))
                self.SCRIPTS.append(row[3])
                row_num=row_num+1
        except:
            self.errmsg('Warning', 'Something went wrong! Please close Script library and open it again.')
    """
    def show(self):
        #self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        try:
            self.textEdit.setText(self.SCRIPTS[self.tableWidget.currentRow()])
            self.updatebtn.setEnabled(True)
        except:
            self.errmsg('Information', 'Please highlight the script to be shown.')
    """
    def rowchange(self):
        try:
            self.textEdit.setText(self.SCRIPTS[self.tableWidget.currentRow()])
            self.updatebtn.setEnabled(True)
        except:
            self.updatebtn.setEnabled(False)
            self.textEdit.clear()
            pass
    def update(self):
        try:
            del col0
            del doc1
            del col1
            del col2
            del col3
        except:
            pass
        try :
            col0=self.ID[self.tableWidget.currentRow()]
            col1=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
            col2=self.tableWidget.item(self.tableWidget.currentRow(),1).text()
            doc1=self.textEdit.document().toPlainText()
            col3=str(doc1)
            self.SCRIPTS[self.tableWidget.currentRow()]=doc1
            conn4 = pyodbc.connect("DSN=inventory",timeout=1)
            cursor4 = conn4.cursor()
            cursor4.execute('''exec SP_updatescript @col0=?,@col1=?,@col2=?,@col3=?;''',col0,col1,col2,col3)
            conn4.commit()
            conn4.close()
            del cursor4
            self.errmsg('Information', 'The script updated successfully.')
        except:
            self.errmsg('Warning', 'Unable to update the script.')
            
    def delete(self):
        try:

            col0=self.ID[self.tableWidget.currentRow()]
            conn4 = pyodbc.connect("DSN=inventory",timeout=1)
            cursor4 = conn4.cursor()
            cursor4.execute('''exec SP_deletescript @col0=?;''',col0)
            conn4.commit()
            conn4.close()
            del cursor4
            self.errmsg('Information', 'The script deleted successfully.')
        except:
            self.errmsg('Warning', 'Unable to delete the script.')
        self.refresh()
    def save(self):
        try:
            
            del doc
            del co1
            del co2
            del co3
        except:
            pass
        
        try:
            co1=self.tableWidget.item(0,0).text()
            co2=self.tableWidget.item(0,1).text()
            doc=self.textEdit.document().toPlainText()
            co3=str(doc)
            conn4 = pyodbc.connect("DSN=inventory",timeout=1)
            cursor4 = conn4.cursor()
            cursor4.execute('''exec sp_insertscript @col1=?,@col2=?,@col3=?;''',co1, co2, co3)
            conn4.commit()
            conn4.close()
            del cursor4
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(1)
            self.textEdit.clear()
            self.errmsg('Information', 'The script saved successfully.')
        except:
            self.errmsg('Warning', 'Unable to save the script.')

    def resetall(self):
        #print('reset all')
        try:
            #self.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setEnabled(False)
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
            self.deletebtn.setEnabled(False)
            self.updatebtn.setEnabled(False)
            self.textEdit.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(1)
            del self.ID
            del self.TAGS
            del self.DESC
            del self.SCRIPTS
        except:
            pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QDialog()
    ui = Ui_Dialog3()
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
