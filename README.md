# DB-Inventory
Centralized Database Servers inventory 
A: Minimum required steps to get started:
1. Copy InventoryV2 to C: drive
2. Create the database using C:\InventoryV2\deployment\InventoryV2Database.sql
3. Create User DSN for ODBC Connection:
	-name: InventoryV2
	-driver:SQL Native Client 11
	-Server:SQL Server 2016 or higher
	-default database: InventoryV2
	-Windows authentication
B:Additional Steps:
fields = ID,Name,Domain,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14
1. Above option "fields" is kept in %appdata% folder "C:\Users\UserName\AppData\Roaming\InventoryV2Config.ini"
	-it represents the dataframe columns and should match the columns names in the table and all stored procedures
	-there should not be any white spaces between the columns
	-ID is the dataframe index and should not be renamed. it will not be displayed on the application.
	-'Name' + 'col3' are the database uniqe constraint Ex: (Name is the service name and col3 the node1 hostname) to prevent users from inserting duplicates
	-third column "col2" should be the domain name as it will be used for RDP button to fill in the username automatically
	-fifteenth column "col14" should be the port number. it will be used to connect to remote servers for healthcheck and status
2. when the application start, it will look for the config file in %Appdata%, if it's not there a new copy will be taken from C:InventoryV2\deployment\ folder

Finally, please report any issues you face using this app. by default inventoryV2.log will be located in Documents folder.
