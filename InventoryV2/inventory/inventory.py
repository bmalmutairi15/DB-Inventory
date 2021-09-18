'''
LGPL License
Copyright (c) [2021] [bmalmutairi15@gmail.com]
'''
from PySide2.QtCharts import QtCharts#QPieSeries
from PySide2.QtGui import  QPen, QColor, QBrush ,QPainter,QIcon
from PySide2.QtWidgets import  (QTableView, QWidget, QProgressBar, QFrame, QVBoxLayout, QLabel
    , QMessageBox,QApplication,QMainWindow,QHBoxLayout,QLineEdit,QPushButton,QToolButton
    ,QGridLayout,QStatusBar, QHeaderView, QDialog, QFileDialog)
from PySide2.QtCore import QAbstractTableModel, Qt, QTimer,QRect,QCoreApplication,QMetaObject
import sys,os,csv,time
import shutil
from cryptography.fernet import Fernet
import pyodbc
import styles
import windows
#import qtmodern2.styles2
#import qtmodern2.windows2
import getpass
import subprocess
import gc 
import logging
from logging.handlers import RotatingFileHandler
import configparser
config = configparser.ConfigParser()
configfile = os.environ['AppData'] + '\\InventoryV2Config.ini'
if os.path.isfile(configfile):
    config.read(configfile)
else:
    shutil.copy("../deployment/InventoryV2Config.ini", configfile)
    config.read(configfile)
from inputwin import Ui_Dialog
from preference import Ui_Dialog2
#from healthcheck import Ui_Form
from scriptlibrary import *
import webbrowser
username = getpass.getuser()
theme = config['defaults']['theme']
fields = config['defaults']['fields']
fields = fields.split(',')
winHeight = int(config['defaults']['winHeight'])
winWidth = int(config['defaults']['winWidth'])
tblFrameHeight = int(config['defaults']['tblFrameHeight'])
tblFrameWidth = int(config['defaults']['tblFrameWidth'])
UseNativeBrowser = int(config['defaults']['UseNativeBrowser'])
exportdirectory = config['defaults']['exportdirectory']
UseCurrentUser = int(config['defaults']['UseCurrentUser'])
sqlcmdpath = config['defaults']['sqlcmdpath']
logger = logging.getLogger(":")
logger.setLevel(logging.ERROR)
user_profile = os.environ['USERPROFILE']
log_file : str =user_profile + '/' + exportdirectory + '/inventoryV2.log'
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        #if role == Qt.DisplayRole:
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value=self._data[index.row()][index.column()]
            return str(value)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return fields[col]
        return None
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            # Set the value into the frame.
            self._data[index.row()][index.column()] = value
            NewValue = value
            co0 = index.sibling(index.row(), 0).data()  # .strip()
            # self.co2=index.sibling(index.row(),2).data()
            # self.co3=index.sibling(index.row(),3).data()
            ToBeUpdated = fields[int(index.column())]  # .strip()
            try:

                ucursor = conn.cursor()
                ucursor.execute('''exec SP_Update @col0=?,@ToBeUpdated=?,@NewVal=?;''', co0, ToBeUpdated, NewValue)
                ucursor.commit()
                ucursor.close()
                del ucursor
                Ui_MainWindow.errmsg(mw, 'Information', 'Sucessfully Updated One Record')
            except:
                Ui_MainWindow.errmsg(mw, 'Warning', 'Unable To Update The Record In The Backend SQL Server')
            return True

        return False
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.errmsg('About', 'Welcome to Database Inventory!<br/>Version: 2.1.0.4<br/>Owner: Bandar Almutairi!<br/>Email:bmalmutairi15@gmail.com')
        # time.sleep(10)
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1600, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 1200, 20))
        # self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 931, 20))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.SearchEntry = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        # self.SearchEntry.returnPressed.connect(self.Searchbtn.click)
        self.SearchEntry.setObjectName("SearchEntry")
        self.horizontalLayout.addWidget(self.SearchEntry)
        self.Searchbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Searchbtn.setObjectName("Searchbtn")
        self.Searchbtn.setAutoDefault(True)
        self.horizontalLayout.addWidget(self.Searchbtn)
        self.SearchEntry.returnPressed.connect(self.Searchbtn.click)
        self.Deletebtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Deletebtn.setObjectName("Deletebtn")
        self.horizontalLayout.addWidget(self.Deletebtn)
        self.Exportbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Exportbtn.setObjectName("Exportbtn")
        self.horizontalLayout.addWidget(self.Exportbtn)
        self.Newbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget, clicked=lambda: self.insertnew())
        self.Newbtn.setObjectName("Newbtn")
        self.horizontalLayout.addWidget(self.Newbtn)
        self.RDPbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.RDPbtn.setObjectName("RDPbtn")
        self.horizontalLayout.addWidget(self.RDPbtn)
        self.SSHbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.SSHbtn.setObjectName("SSHbtn")
        self.horizontalLayout.addWidget(self.SSHbtn)

        self.HealthCheckbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.HealthCheckbtn.setObjectName("HealthCheckbtn")
        self.horizontalLayout.addWidget(self.HealthCheckbtn)
        #self.HealthCheckbtn.setEnabled(False)

        self.Statusbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Statusbtn.setObjectName("Statusbtn")
        #self.Statusbtn.setEnabled(False)
        self.horizontalLayout.addWidget(self.Statusbtn)

        self.Dashboardbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Dashboardbtn.setObjectName("Dashboardbtn")
        self.horizontalLayout.addWidget(self.Dashboardbtn)

        self.Failoverbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Failoverbtn.setObjectName("Failoverbtn")
        self.horizontalLayout.addWidget(self.Failoverbtn)
        self.Failoverbtn.setEnabled(False)

        self.Librarybtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Librarybtn.setObjectName("Librarybtn")
        self.horizontalLayout.addWidget(self.Librarybtn)
        self.Librarybtn.setEnabled(True)

        self.InstallSQLbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.InstallSQLbtn.setObjectName("InstallSQLbtn")
        self.horizontalLayout.addWidget(self.InstallSQLbtn)
        self.InstallSQLbtn.setEnabled(False)
        # spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        # self.horizontalLayout.addItem(spacerItem)
        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget, clicked=lambda: self.pref())
        self.toolButton.setObjectName("toolButton")
        self.toolButton.setIcon(QIcon('C:/InventoryV2/icons/icon_settings.png'))
        self.horizontalLayout.addWidget(self.toolButton)

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 35, tblFrameWidth, tblFrameHeight))
        # self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 931, 521))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.connect(self.Searchbtn, SIGNAL("clicked()"),self.search)
        self.Searchbtn.clicked.connect(self.search)
        self.Deletebtn.clicked.connect(self.delete)
        self.Exportbtn.clicked.connect(self.export)
        self.RDPbtn.clicked.connect(self.RDP)
        self.SSHbtn.clicked.connect(self.SSH)
        self.HealthCheckbtn.clicked.connect(self.HealthCheck)
        self.Dashboardbtn.clicked.connect(self.dashboard)
        self.Statusbtn.clicked.connect(self.checkstatus)
        self.Librarybtn.clicked.connect(self.openlibrary)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Inventory"))
        self.Searchbtn.setText(_translate("MainWindow", "Search"))
        self.Deletebtn.setText(_translate("MainWindow", "Delete"))
        self.Exportbtn.setText(_translate("MainWindow", "Export"))
        self.Newbtn.setText(_translate("MainWindow", "New"))
        self.RDPbtn.setText(_translate("MainWindow", "RDP"))
        self.SSHbtn.setText(_translate("MainWindow", "SSH"))
        self.HealthCheckbtn.setText(_translate("MainWindow", "Health Check"))
        self.Statusbtn.setText(_translate("MainWindow", "Status"))
        self.Dashboardbtn.setText(_translate("MainWindow", "DashBoard"))
        self.Failoverbtn.setText(_translate("MainWindow", "Failover"))
        self.Librarybtn.setText(_translate("MainWindow", "Script Library"))
        self.InstallSQLbtn.setText(_translate("MainWindow", "Install SQL"))
        self.SearchEntry.setFocus()

    def errmsg(self, TYPE, msg):
        if TYPE == 'Warning':
            QMessageBox.warning(mw, "Warning", msg)
        elif TYPE == 'Information':
            QMessageBox.information(mw, "Information", msg)
        elif TYPE == 'About':
            QMessageBox.about(mw, "Inventory", msg)
            # QMessageBox.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def dashboard(self):
        try:

            self.Deletebtn.setEnabled(False)
            self.Exportbtn.setEnabled(False)
            self.RDPbtn.setEnabled(False)
            self.SSHbtn.setEnabled(False)
            self.HealthCheckbtn.setEnabled(False)
            self.Statusbtn.setEnabled(False)
            self.gridLayout.removeWidget(self.Outputtbl)
            self.Outputtbl.deleteLater()
            self.Outputtbl = None
            del self.model

        except:

            pass
        try:

            self.gridLayout.removeWidget(self.chartView)
            self.chartView.deleteLater()
            self.chartView = None
            self.gridLayout.removeWidget(self.chartView2)
            self.chartView2.deleteLater()
            self.chartView2 = None
            self.gridLayout.removeWidget(self.chartView3)
            self.chartView3.deleteLater()
            self.chartView3 = None
            del self.chart
            del self.series
            del self.chart2
            del self.series2
            del self.chart3
            del self.series3
            gc.collect()
            del self.currentcell
            del self.col0
            #del self.col1
            del self.col2
            #del self.col3
        except:
            pass
        try:
            conn1 = pyodbc.connect('DSN=inventoryV2', timeout=1)
            cursor1 = conn1.cursor()
        except  Exception as e:
            logger.error(str(e))
            self.errmsg('Warning',
                        'Unable to connect to inventory database.<br/> Make sure the DSN is configured properly!')
            return
        if theme == 'dark':
            QCColor = 'dimgray'
        else:
            QCColor = 'light gray'
        cursor1.execute('sp_instancecount')
        instancecount1 = cursor1.fetchone()
        instancecount = str(instancecount1[0])

        cursor1.execute('sp_servercount')
        servercount1 = cursor1.fetchone()
        servercount = str(servercount1[0])

        cursor1.execute('sp_servicecount')
        servicecount1 = cursor1.fetchone()
        servicecount = str(servicecount1[0])

        SP_Name1 = 'sp_countbysqlversion'
        SP_Name2 = 'sp_countbyosversion'
        SP_Name3 = 'sp_countbycategory'
        self.series = QtCharts.QPieSeries()
        self.series2 = QtCharts.QPieSeries()
        self.series3 = QtCharts.QPieSeries()

        cursor1.execute(SP_Name1)
        ROW = cursor1.fetchone()
        Column = []
        Count = []
        while ROW:
            self.series.append('"' + str(ROW[0]) + '",', int(ROW[1]))
            Column.append(str(ROW[0]))
            Count.append(str(ROW[1]))
            ROW = cursor1.fetchone()

        cursor1.execute(SP_Name2)
        ROW2 = cursor1.fetchone()
        Column2 = []
        Count2 = []
        while ROW2:
            self.series2.append('"' + str(ROW2[0]) + '",', int(ROW2[1]))
            Column2.append(str(ROW2[0]))
            Count2.append(str(ROW2[1]))
            ROW2 = cursor1.fetchone()
        cursor1.execute(SP_Name3)
        ROW3 = cursor1.fetchone()
        Column3 = []
        Count3 = []
        while ROW3:
            self.series3.append('"' + str(ROW3[0]) + '",', int(ROW3[1]))
            Column3.append(str(ROW3[0]))
            Count3.append(str(ROW3[1]))
            ROW3 = cursor1.fetchone()
        cursor1.close()
        del cursor1
        self.chart = QtCharts.QChart()
        self.chart2 = QtCharts.QChart()
        self.chart3 = QtCharts.QChart()
        self.chart.addSeries(self.series)
        self.chart2.addSeries(self.series2)
        self.chart3.addSeries(self.series3)
        self.chart.setTitle(
            "<strong>SQL Server Versions <br> <br> </strong>" + "<center>{} Instance Total </center>".format(
                instancecount))
        # self.chart.setTitle("<strong>SQL Server <br> Versions</strong>")
        self.chart2.setTitle(
            "<strong>Windows Server Versions <br> <br> </strong>" + "<center>{} node Total </center>".format(
                servercount))
        self.chart3.setTitle(
            "<strong>Category</strong> <br> <br> </strong>" + "<center>{} Service Total </center>".format(servicecount))
        self.chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.chart2.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.chart3.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.chart.setBackgroundBrush(QBrush(QColor(QCColor)))
        self.chart2.setBackgroundBrush(QBrush(QColor(QCColor)))
        self.chart3.setBackgroundBrush(QBrush(QColor(QCColor)))
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart2.legend().setAlignment(Qt.AlignBottom)
        self.chart3.legend().setAlignment(Qt.AlignBottom)
        # transparent
        self.series.setLabelsPosition(QtCharts.QPieSlice.LabelInsideHorizontal)
        self.series2.setLabelsPosition(QtCharts.QPieSlice.LabelInsideHorizontal)
        self.series3.setLabelsPosition(QtCharts.QPieSlice.LabelInsideHorizontal)
        i = 0
        for slice in self.series.slices():
            slice.setLabel(Column[i] + ' : ' + Count[i])
            slice.setPen(QPen(QColor(QCColor), 1))
            i += 1
        i = 0
        for slice in self.series2.slices():
            slice.setLabel(Column2[i] + ' : ' + Count2[i])
            slice.setPen(QPen(QColor(QCColor), 1))
            i += 1
        i = 0
        for slice in self.series3.slices():
            slice.setLabel(Column3[i] + ' : ' + Count3[i])
            slice.setPen(QPen(QColor(QCColor), 1))
            i += 1
        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView2 = QtCharts.QChartView(self.chart2)
        self.chartView3 = QtCharts.QChartView(self.chart3)
        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.chartView.resize(640, 480)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.addWidget(self.chartView, 0, 0, 1, 1)

        self.chartView2.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.chartView2.resize(640, 480)
        self.gridLayout.addWidget(self.chartView2, 0, 1, 1, 1)

        self.chartView3.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.chartView3.resize(640, 480)
        self.gridLayout.addWidget(self.chartView3, 0, 2, 1, 1)
        del conn1
        del ROW
        del ROW2
        del ROW3
        del Column
        del Count
        del Column2
        del Count2
        del Count3
        del Column3

    dashboard1 = dashboard

    def search(self):

        searchinput = self.SearchEntry.text()

        # try deleteing output table view if it exists
        try:
            self.Deletebtn.setEnabled(True)
            self.Exportbtn.setEnabled(True)
            self.RDPbtn.setEnabled(True)
            self.SSHbtn.setEnabled(True)
            self.HealthCheckbtn.setEnabled(True)
            self.Statusbtn.setEnabled(True)
            self.gridLayout.removeWidget(self.Outputtbl)
            self.Outputtbl.deleteLater()
            self.Outputtbl = None
            del self.model
            self.gridLayout.removeWidget(self.chartView)
            self.chartView.deleteLater()
            self.chartView = None
            self.gridLayout.removeWidget(self.chartView2)
            self.chartView2.deleteLater()
            self.chartView2 = None
            self.gridLayout.removeWidget(self.chartView3)
            self.chartView3.deleteLater()
            self.chartView3 = None
            del self.chart
            del self.series
            gc.collect()
            del self.currentcell
            del self.col0
            del self.col1
            del self.col2
            del self.col3
        except:

            pass

        cursor = conn.cursor()
        cursor.execute('sp_search ?',searchinput)
        self.output = cursor.fetchall()
        x=len(self.output)
        if x == 0:
            self.Deletebtn.setEnabled(False)
            self.Exportbtn.setEnabled(False)
            self.RDPbtn.setEnabled(False)
            self.SSHbtn.setEnabled(False)
            self.HealthCheckbtn.setEnabled(False)
            self.Statusbtn.setEnabled(False)
            self.errmsg('Information', 'No record matched your search! please try again.')
        else:
   
            self.model=TableModel(self.output)
            self.Outputtbl = QTableView(self.gridLayoutWidget)
            self.header = self.Outputtbl.horizontalHeader()
            self.header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.Outputtbl.setModel(self.model)
            self.Outputtbl.setColumnHidden(0, True)
            self.gridLayout.addWidget(self.Outputtbl, 0, 0, 1, 3)
            self.Outputtbl.clicked.connect(self.Selected)
    def Selected(self):
        index = (self.Outputtbl.selectionModel().currentIndex())
        value = index.sibling(index.row(), index.column()).data()
        # get the service name of selected row
        self.col0 = int(index.sibling(index.row(), 0).data().strip())
        #self.col1 = index.sibling(index.row(), 1).data()
        self.col2 = index.sibling(index.row(), 2).data()
        # get node1 hostname of selected row
        self.col14 = index.sibling(index.row(), 14).data()
        self.currentcell = index.sibling(index.row(), index.column()).data().strip()

    def insertnew(self):
        self.insertwin = QtWidgets.QDialog()
        self.insertwin.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.insertwin)
        self.insertwin.show()
    def openlibrary(self):
        #librarywin=mw
        self.librarywin = QtWidgets.QDialog()
        self.librarywin.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ui = Ui_Dialog3()
        self.ui.setupUi(self.librarywin)
        self.librarywin.show()
    def pref(self):
        self.prefwin = QtWidgets.QDialog()
        self.prefwin.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self.prefwin)
        self.prefwin.show()

    def delete(self):
        # self.errors('One record deleted')

        try:
            #
            dcursor = conn.cursor()
            dcursor.execute('''exec sp_delete @col0=?;''', self.col0)
            dcursor.commit()
            dcursor.close()
            del dcursor
            self.errmsg('Information', 'One Record Deleted')
            self.search()
        except Exception as e:
            logger.error(str(e))

            self.errmsg('Warning', 'Operation Failed! please check inventoryV2.log for more details.')

    def RDP(self):
        #try:
        username = self.col2.strip() + '\\' + getpass.getuser()
        print(os.getcwd())
        k = config['optional']['k']
        fernet = Fernet(k)
        step1 = config['optional']['pwd']
        step2 = bytes(step1[1:], "utf8")
        PWD = (fernet.decrypt(step2).decode()).strip()
        #mstsc=r'C:\Windows\System32\mstsc.exe'
        #print(len(PWD))
        if len(PWD) > 2:
            subprocess.Popen([r'..\bin\RDPwithPWD.bat', self.currentcell, username,PWD])
            #os.system(f'cmdkey /generic:{self.currentcell} /user:{username} /pass:{PWD}')
            #time.sleep(1)
            #p=subprocess.Popen([mstsc,f'/v:{self.currentcell}'] )
            #time.sleep(5)
            #os.system(f'cmdkey /delete:{self.currentcell}')    
        else:# needs to be tested
            subprocess.Popen([r'..\bin\RDP.bat', self.currentcell, username])

        try:
            del PWD
            PWD=None
        except:
            pass
    def checkstatus(self):
        #username = self.col2.strip() + '\\' + getpass.getuser()
        
        try:
            uname=getpass.getuser()
            server=self.currentcell
            port=self.col14.strip()
            sServer='Server={},{};'.format(server,port)
            remoteconn=pyodbc.connect('Driver={SQL Server Native Client 11.0};'+sServer+'DATABASE=master;''Trusted_Connection=yes;',timeout=15)
            cur = remoteconn.cursor()
            with open('../bin/status.sql') as script:
                query=script.read()
            cur.execute(query)
            results=cur.fetchone()
            role=results[0]
            hostname=results[1]
            st=hostname+' is '+role
            self.errmsg('About', st)
        except Exception as e:
            logger.error(str(e))
            self.errmsg('Warning', 'Operation Failed! please check inventoryV2.log for more details.')
    def HealthCheck(self):

        try:
            username = self.col2.strip() + '\\' + getpass.getuser()
            uname=getpass.getuser()
            server=self.currentcell
            hcreportname=user_profile+'\\'+exportdirectory
        except Exception as e:
            logger.error(str(e))
            logger.error('Must select the server IP to perform a healthcheck')
            self.errmsg('Warning', 'Please select Server or Virtual IP')
            return
        
        
        try:
            port=self.col14.strip()
            sServer='{},{}'.format(server,port)
            script=r'..\bin\healthcheck.sql'
            hcreportname=user_profile+'\\'+exportdirectory
            result=r'{}\{}_healthcheck.html'.format(hcreportname,uname)
            sqlcmd=sqlcmdpath.strip('"')+'SQLCMD.EXE'
            p=subprocess.Popen([sqlcmd,'-S', sServer, '-i', script, '-o',result, '-y', '0', '-b'])
            p_status=p.wait()
            if p_status == 0:
                self.errmsg('About', 'If The Browser doesn\'t open after dismissing this message, you\'ll find the _healthcheck.html file in the default exportdirectory')
                if UseNativeBrowser==1:
                    webbrowser.open('file://{}/{}_healthcheck.html'.format(hcreportname,uname),new=2)
                elif UseNativeBrowser==0:
                    print('to be removed line 626')
                else:
                    self.errmsg('Warning', 'Unable to open HealthCheck Report')            
            else:
                self.errmsg('Warning', 'Unable to generate the healthcheck report!')
            try:
                del uname
                del username
                gc.collect()

            except:
                pass
        except Exception as e:
            logger.error(str(e))
            self.errmsg('Warning', 'Operation Failed! please check inventoryV2.log for more details.')
            

    def SSH(self):
        try:
            #subprocess.Popen([r'..\bin\putty.bat', self.currentcell])
            p=subprocess.Popen(['../bin/putty.exe', '-ssh', self.currentcell])
            #p.wait()
        except Exception as e:
            logger.error(str(e))

    # noinspection PyTypeChecker
    def export(self):
        try:
            path = QtWidgets.QFileDialog.getSaveFileName(
                self.Outputtbl, 'Save File', 'DB-inventory', 'CSV (*.csv)')
            with open(path[0], 'w') as stream:
                writer = csv.writer(stream)
                writer.writerow(fields)
                for row in range(self.model.rowCount(None)):
                    rowdata = []
                    #rowdata.append(fields)
                    for col in range(self.model.columnCount(None)):
                        #item = self.Outputtbl.item(row, column)
                        item=self.model.data(self.model.index(row, col), Qt.DisplayRole)

                        if item is not None:
                            rowdata.append(item)#.text())#.encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
        except Exception as e:
                logger.error(str(e))
                self.errmsg('Warning', 'An error occured while exporting your file!')


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spash Screen')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300  # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40)  # x, y
        self.labelTitle.setText('DB Inventory')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Loading Application Components</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('Loading...')

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Loading Configuration Files</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Connecting to the Backend Database</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

        self.counter += 1

    def finish(self, QWidget):

        self.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.setStyleSheet('''
        #LabelTitle {
            font-size: 60px;
            color: #93deed;
        }

        #LabelDesc {
            font-size: 30px;
            color: #c2ced1;
        }

        #LabelLoading {
            font-size: 30px;
            color: #e8e8eb;
        }

        QFrame {
            background-color: #2F4454;
            color: rgb(220, 220, 220);
        }

        QProgressBar {
            background-color: #93deed;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }

        QProgressBar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }
    ''')
    splash.show()
    app.processEvents()

    MainWindow = QMainWindow()
    MainWindow.resize(winWidth, winHeight)
    if theme == 'light':
        styles.light(app)
        mw = windows.ModernWindow(MainWindow,theme='light')
    elif theme == 'dark':
        styles.dark(app)
        mw = windows.ModernWindow(MainWindow,theme='dark')
    elif theme == 'darkblue':
        styles.darkblue(app)
        mw = windows.ModernWindow(MainWindow,theme='darkblue')
    elif theme == 'darkorange':
        styles.darkorange(app)
        mw = windows.ModernWindow(MainWindow,theme='darkorange')
    else:
        styles.darkorange(app)
        mw = windows.ModernWindow(MainWindow,theme='darkorange')

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # MainWindow.show()
    try:
        conn = pyodbc.connect("DSN=inventoryV2", timeout=1)
    except Exception as e:
        logger.error(str(e))
        mw.errmsg('Warning', 'unable to connect to the SQL')
    mw.show()
    ui.dashboard1()
    splash.finish(mw)

    sys.exit(app.exec_())
