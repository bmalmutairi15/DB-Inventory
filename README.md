# DB-Inventory
By Bandar M. Almutairi "bmalmutairi15@gmail.com"<br/>
Centralized Database Servers inventory.<br/>
![alt text](https://github.com/bmalmutairi15/DB-Inventory/blob/main/Screenshots/dashboard.PNG?raw=true)
Minimum required steps to get started:<br/>
1. Copy InventoryV2 to C: drive<br/>
2. Create the sql database using C:\InventoryV2\deployment\InventoryV2Database.sql<br/>
3. Create User DSN for ODBC Connection:<br/>
	-name: InventoryV2<br/>
	-driver:SQL Native Client 11<br/>
	-Server:SQL Server 2016 or higher<br/>
	-default database: InventoryV2<br/>
	-Windows authentication<br/>
Additional Steps:<br/>
fields = ID,Name,Domain,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14<br/>
4. Above option "fields" is kept in %appdata% folder "C:\Users\UserName\AppData\Roaming\InventoryV2Config.ini"<br/>
	-it represents the dataframe columns and should match the columns names in the table and all stored procedures<br/>
	-there should not be any white spaces between the columns<br/>
	-ID is the dataframe index and should not be renamed. it will not be displayed on the application.<br/>
	-'Name' + 'col3' are the database uniqe constraint Ex: (Name is the service name and col3 the node1 hostname) to prevent users from inserting duplicates<br/>
	-third column "col2" should be the domain name as it will be used for RDP button to fill in the username automatically<br/>
	-fifteenth column "col14" should be the port number. it will be used to connect to remote servers for healthcheck and status<br/>
5. when the application start, it will look for the config file in %Appdata%, if it's not there a new copy will be taken from C:InventoryV2\deployment\ folder<br/>
<br/>
Finally, please report any issues you face using this app. by default inventoryV2.log will be located in Documents folder.<br/><br/>
----------------------------------
#pip list for this project:<br/>
configparser              5.0.2     >> https://pypi.org/project/configparser/<br/>
cryptography              3.4.8     >> https://pypi.org/project/cryptography/<br/>
pyodbc                    4.0.32    >> https://pypi.org/project/pyodbc/<br/>
PySide2                   5.15.2    >> https://pypi.org/project/PySide2/<br/>
qtmodern                  0.2.0     >> https://pypi.org/project/qtmodern/ <br/>
Healthcheck.sql >> is a modified copy of http://udayarumilli.com/sql-server-health-check-html-report/<br/>
splashscreen    >> is a modified copy of https://learndataanalysis.org/source-code-create-a-modern-style-flash-screen-pyqt5-tutorial/<br/>



