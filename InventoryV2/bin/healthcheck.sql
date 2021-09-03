BEGIN TRY
SET ANSI_NULLS ON

SET QUOTED_IDENTIFIER ON
BEGIN  
SET NOCOUNT ON;  
SET ARITHABORT ON; 
DECLARE @TableHTML  VARCHAR(MAX),
 @ServerName VARCHAR(100);  
SET @ServerName = @@SERVERNAME; 

IF OBJECT_ID('tempdb..#RebootDetails') IS NOT NULL DROP TABLE #RebootDetails;
IF OBJECT_ID('tempdb..#errorlogs') IS NOT NULL DROP TABLE #errorlogs;
IF OBJECT_ID('tempdb..#CPU') IS NOT NULL DROP TABLE #CPU;
IF OBJECT_ID('tempdb..#Memory_BPool') IS NOT NULL DROP TABLE #Memory_BPool;
IF OBJECT_ID('tempdb..#Memory_sys') IS NOT NULL DROP TABLE #Memory_sys;
IF OBJECT_ID('tempdb..#Memory_process') IS NOT NULL DROP TABLE #Memory_process;
IF OBJECT_ID('tempdb..#Memory') IS NOT NULL DROP TABLE #Memory;
IF OBJECT_ID('tempdb..#perfmon_counters') IS NOT NULL DROP TABLE #perfmon_counters;
IF OBJECT_ID('tempdb..#PerfCntr_Data') IS NOT NULL DROP TABLE #PerfCntr_Data;
IF OBJECT_ID('tempdb..#Backup_Report') IS NOT NULL DROP TABLE #Backup_Report;
IF OBJECT_ID('tempdb..#DBSize') IS NOT NULL DROP TABLE #DBSize;
IF OBJECT_ID('tempdb..#JOBSTATUS') IS NOT NULL DROP TABLE #JOBSTATUS;
IF OBJECT_ID('tempdb..#fixeddrives') IS NOT NULL DROP TABLE #fixeddrives;
IF OBJECT_ID('tempdb..#LogSpace') IS NOT NULL DROP TABLE #LogSpace;
IF OBJECT_ID('tempdb..#AGStatus') IS NOT NULL DROP TABLE #AGStatus;
IF OBJECT_ID('tempdb..#tempdbfileusage') IS NOT NULL DROP TABLE #tempdbfileusage;

CREATE TABLE #RebootDetails                                
(                                
 LastRecycle datetime,                                
 CurrentDate datetime,                                
 UpTimeInDays varchar(100)                          
)                        
Insert into #RebootDetails          
SELECT sqlserver_start_time 'Last Recycle',GetDate() 'Current Date', DATEDIFF(DD, sqlserver_start_time,GETDATE())'Up Time in Days'  
FROM sys.dm_os_sys_info;  



Create table #CPU(               
servername varchar(100),                           
EventTime2 datetime,                            
SQLProcessUtilization varchar(50),                           
SystemIdle varchar(50),  
OtherProcessUtilization varchar(50),  
load_date datetime                            
)      
DECLARE @ts BIGINT;  DECLARE @lastNmin TINYINT;  
SET @lastNmin = 240;  
SELECT @ts =(SELECT cpu_ticks/(cpu_ticks/ms_ticks) FROM sys.dm_os_sys_info);   
insert into #CPU  
SELECT TOP 10 * FROM (  
SELECT TOP(@lastNmin)  
  @ServerName AS 'ServerName',  
  DATEADD(ms,-1 *(@ts - [timestamp]),GETDATE())AS [Event_Time],   
  SQLProcessUtilization AS [SQLServer_CPU_Utilization],   
  SystemIdle AS [System_Idle_Process],   
  100 - SystemIdle - SQLProcessUtilization AS [Other_Process_CPU_Utilization],  
  GETDATE() AS 'LoadDate'  
FROM (SELECT record.value('(./Record/@id)[1]','int')AS record_id,   
record.value('(./Record/SchedulerMonitorEvent/SystemHealth/SystemIdle)[1]','int')AS [SystemIdle],   
record.value('(./Record/SchedulerMonitorEvent/SystemHealth/ProcessUtilization)[1]','int')AS [SQLProcessUtilization],   
[timestamp]        
FROM (SELECT[timestamp], convert(xml, record) AS [record]               
FROM sys.dm_os_ring_buffers               
WHERE ring_buffer_type =N'RING_BUFFER_SCHEDULER_MONITOR'AND record LIKE'%%')AS x )AS y   
ORDER BY SystemIdle ASC) d  
 
   
/*************************************************************/  
/************* SQL Server Memory Usage Details ***************/  
/*************************************************************/  
  
CREATE TABLE #Memory_BPool (  
BPool_Committed_MB VARCHAR(50),  
BPool_Commit_Tgt_MB VARCHAR(50),  
BPool_Visible_MB VARCHAR(50));  

/****  
  
-- SQL server 2008 / 2008 R2  
INSERT INTO #Memory_BPool    
SELECT  
     (bpool_committed*8)/1024.0 as BPool_Committed_MB,  
     (bpool_commit_target*8)/1024.0 as BPool_Commit_Tgt_MB,  
     (bpool_visible*8)/1024.0 as BPool_Visible_MB  
FROM sys.dm_os_sys_info;  
****/  

-- SQL server 2012 / 2014 / 2016  
INSERT INTO #Memory_BPool   
SELECT  
      CAST((committed_kb)/1024.0 as decimal(18,0)) as BPool_Committed_MB,  
      CAST((committed_target_kb)/1024.0 as decimal(18,0))as BPool_Commit_Tgt_MB,  
      CAST((visible_target_kb)/1024.0 as decimal(18,0))as BPool_Visible_MB  
FROM  sys.dm_os_sys_info;  

CREATE TABLE #Memory_sys (  
total_physical_memory_mb VARCHAR(50),  
available_physical_memory_mb VARCHAR(50),  
total_page_file_mb VARCHAR(50),  
available_page_file_mb VARCHAR(50),  
Percentage_Used VARCHAR(50),  
system_memory_state_desc VARCHAR(50));  
  
INSERT INTO #Memory_sys  
select  
      total_physical_memory_kb/1024 AS total_physical_memory_mb,  
      available_physical_memory_kb/1024 AS available_physical_memory_mb,  
      total_page_file_kb/1024 AS total_page_file_mb,  
      available_page_file_kb/1024 AS available_page_file_mb,  
      CAST(100 - (100 * CAST(available_physical_memory_kb AS DECIMAL(18,3))/CAST(total_physical_memory_kb AS DECIMAL(18,3)))AS DECIMAL(18,2))   
      AS 'Percentage_Used',  
      system_memory_state_desc  
from  sys.dm_os_sys_memory;  
  
  
CREATE TABLE #Memory_process(  
physical_memory_in_use_GB VARCHAR(50),  
locked_page_allocations_GB VARCHAR(50),  
virtual_address_space_committed_GB VARCHAR(50),  
available_commit_limit_GB VARCHAR(50),  
page_fault_count VARCHAR(50))  
  
INSERT INTO #Memory_process  
select  
      CAST(physical_memory_in_use_kb/1048576.0 as decimal(18,2)) AS 'Physical_Memory_In_Use(GB)',  
       CAST(locked_page_allocations_kb/1048576.0 as decimal(18,2)) AS 'Locked_Page_Allocations(GB)',  
       CAST(virtual_address_space_committed_kb/1048576.0 as decimal(18,2))AS 'Virtual_Address_Space_Committed(GB)',  
      CAST( available_commit_limit_kb/1048576.0 as decimal(18,2))AS 'Available_Commit_Limit(GB)',  
      page_fault_count as 'Page_Fault_Count'  
from  sys.dm_os_process_memory;  
  
  
CREATE TABLE #Memory(  
ID INT IDENTITY NOT NULL,
Parameter VARCHAR(200),  
Value VARCHAR(100));  
  
INSERT INTO #Memory   
SELECT 'BPool_Committed_MB',BPool_Committed_MB FROM #Memory_BPool  
UNION  
SELECT 'BPool_Commit_Tgt_MB', BPool_Commit_Tgt_MB FROM #Memory_BPool  
UNION   
SELECT 'BPool_Visible_MB', BPool_Visible_MB FROM #Memory_BPool  
UNION  
SELECT 'Total_Physical_Memory_MB',total_physical_memory_mb FROM #Memory_sys  
UNION  
SELECT 'Available_Physical_Memory_MB',available_physical_memory_mb FROM #Memory_sys
UNION  
SELECT 'Percentage_Used',Percentage_Used FROM #Memory_sys  
UNION
SELECT 'System_memory_state_desc',system_memory_state_desc FROM #Memory_sys  
UNION  
SELECT 'Total_page_file_mb',total_page_file_mb FROM #Memory_sys  
UNION  
SELECT 'Available_page_file_mb',available_page_file_mb FROM #Memory_sys  
UNION  
SELECT 'Physical_memory_in_use_GB',physical_memory_in_use_GB FROM #Memory_process  
UNION  
SELECT 'Locked_page_allocations_GB',locked_page_allocations_GB FROM #Memory_process  
UNION  
SELECT 'Virtual_Address_Space_Committed_GB',virtual_address_space_committed_GB FROM #Memory_process  
UNION  
SELECT 'Available_Commit_Limit_GB',available_commit_limit_GB FROM #Memory_process  
UNION  
SELECT 'Page_Fault_Count',page_fault_count FROM #Memory_process;  
------------------------------------------------------------------------------
 

   /****bACKUP ****/
CREATE TABLE #Backup_Report(  
DBName VARCHAR(50),  
recovery_model VARCHAR(50),  
[Last Full Backup] Datetime,  
[Last Differential Backup] Datetime,
[Last log Backup] Datetime)  

INSERT INTO #Backup_Report (DBName,recovery_model,[Last Full Backup],[Last Differential Backup],[Last log Backup] )

SELECT  name as DBName ,
            recovery_model_desc as recovery_model ,
            
            d AS 'Last Full Backup' ,
            i AS 'Last Differential Backup' ,
            l AS 'Last log Backup'
    FROM    ( SELECT    db.name ,
                        db.state_desc ,
                        db.recovery_model_desc ,
                        type ,
                        backup_finish_date
              FROM      master.sys.databases db
                        LEFT OUTER JOIN msdb.dbo.backupset a ON a.database_name = db.name
						where db.name !='tempdb'
						--where db.recovery_model_desc ='FULL' --Comment this out to include Simple recovery
            ) AS Sourcetable 
        PIVOT 
            ( MAX(backup_finish_date) FOR type IN ( D, I, L ) ) AS MostRecentBackup
      --where l  < DATEADD(day, -1, CAST(GETDATE() AS date)
	  
/******************************************************************/  
/*************** Job Status **********************/  
/******************************************************************/  
CREATE TABLE #JOBSTATUS(
job_name varchar(50),
job_status varchar(50),
last_run_status varchar(50),
last_run_dt datetime,
duration varchar(50),
next_scheduled_dt datetime,
step_description varchar(2000)
)
insert into #JOBSTATUS
SELECT --Convert(varchar(20),SERVERPROPERTY('ServerName')) AS ServerName, 
j.name AS job_name, 
CASE j.enabled WHEN 1 THEN 'Enabled' Else 'Disabled' END AS job_status, 
CASE jh.run_status WHEN 0 THEN 'Error Failed' 
                WHEN 1 THEN 'Succeeded' 
                WHEN 2 THEN 'Retry' 
                WHEN 3 THEN 'Cancelled' 
                WHEN 4 THEN 'In Progress' ELSE 
                'Status Unknown' END AS 'last_run_status', 
ja.run_requested_date as last_run_date, 
CONVERT(VARCHAR(10),CONVERT(DATETIME,RTRIM(19000101))+(jh.run_duration * 9 + jh.run_duration % 10000 * 6 + jh.run_duration % 100 * 10) / 216e4,108) AS run_duration, 
ja.next_scheduled_run_date, 
CONVERT(VARCHAR(500),jh.message) AS step_description 
FROM 
(msdb.dbo.sysjobactivity ja LEFT JOIN msdb.dbo.sysjobhistory jh ON ja.job_history_id = jh.instance_id) 
join msdb.dbo.sysjobs_view j on ja.job_id = j.job_id 
WHERE ja.session_id=(SELECT MAX(session_id)  from msdb.dbo.sysjobactivity)
--and  ja.run_requested_date >= dateadd(day, 0, (cast(cast(getdate() as varchar(12)) as datetime))) --To filter the timing
and j.name not like 'syspolicy_purge_history'
and j.enabled =1 and jh.run_status !=1
ORDER BY job_name,job_status 


  ---------------------------------------------------------------------------------------------------------------
/******************************************************************/  
/*************** Performance Counter Details **********************/  
/******************************************************************/  
  
CREATE TABLE #PerfCntr_Data(
ID INT IDENTITY NOT NULL,
Parameter VARCHAR(300),  
Value VARCHAR(100));  
  
-- Get size of SQL Server Page in bytes  
DECLARE @pg_size INT, @Instancename varchar(50)  
SELECT @pg_size = low from master..spt_values where number = 1 and type = 'E'  
  
-- Extract perfmon counters to a temporary table  
IF OBJECT_ID('tempdb..#perfmon_counters') is not null DROP TABLE #perfmon_counters  
SELECT * INTO #perfmon_counters FROM sys.dm_os_performance_counters;  
  
-- Get SQL Server instance name as it require for capturing Buffer Cache hit Ratio  
SELECT  @Instancename = LEFT([object_name], (CHARINDEX(':',[object_name])))   
FROM    #perfmon_counters   
WHERE   counter_name = 'Buffer cache hit ratio';  
  
INSERT INTO #PerfCntr_Data  
SELECT CONVERT(VARCHAR(300),Cntr) AS Parameter, CONVERT(VARCHAR(100),Value) AS Value  
FROM  
(  
SELECT  'Page Life Expectency in seconds' as Cntr,  
        cntr_value  AS Value 
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Buffer Manager'   
        and counter_name = 'Page life expectancy'  
UNION ALL  
SELECT  'BufferCache HitRatio'  as Cntr,  
        CAST((a.cntr_value * 1.0 / b.cntr_value) * 100.0 as decimal(18,2))  AS Value 
FROM    sys.dm_os_performance_counters a  
        JOIN (SELECT cntr_value,OBJECT_NAME FROM sys.dm_os_performance_counters  
              WHERE counter_name = 'Buffer cache hit ratio base' AND   
                    OBJECT_NAME = @Instancename+'Buffer Manager') b ON   
                    a.OBJECT_NAME = b.OBJECT_NAME WHERE a.counter_name = 'Buffer cache hit ratio'   
                    AND a.OBJECT_NAME = @Instancename+'Buffer Manager'
UNION ALL
SELECT  'Total Server Memory (GB)' as Cntr,  
       CAST( (cntr_value/1048576.0)as decimal(18,2)) AS Value   
FROM    #perfmon_counters   
WHERE   counter_name = 'Total Server Memory (KB)'  
UNION ALL  
SELECT  'Target Server Memory (GB)',   
        CAST((cntr_value/1048576.0) as decimal(18,2))  
FROM    #perfmon_counters   
WHERE   counter_name = 'Target Server Memory (KB)'  
UNION ALL  
SELECT  'Connection Memory (MB)',   
       CAST( (cntr_value/1024.0)as decimal(18,2))   
FROM    #perfmon_counters   
WHERE   counter_name = 'Connection Memory (KB)'  
UNION ALL  
SELECT  'Lock Memory (MB)',   
       CAST( (cntr_value/1024.0) as decimal(18,2))  
FROM    #perfmon_counters   
WHERE   counter_name = 'Lock Memory (KB)'  
UNION ALL  
SELECT  'SQL Cache Memory (MB)',   
       CAST( (cntr_value/1024.0)  as decimal(18,2)) 
FROM    #perfmon_counters   
WHERE   counter_name = 'SQL Cache Memory (KB)'  
UNION ALL  
SELECT  'Optimizer Memory (MB)',   
       CAST( (cntr_value/1024.0)   as decimal(18,2))
FROM    #perfmon_counters   
WHERE   counter_name = 'Optimizer Memory (KB) '  
UNION ALL  
SELECT  'Granted Workspace Memory (MB)',   
       CAST( (cntr_value/1024.0)  as decimal(18,2)) 
FROM    #perfmon_counters   
WHERE   counter_name = 'Granted Workspace Memory (KB) '  
UNION ALL  
SELECT  'Cursor memory usage (MB)',   
        CAST((cntr_value/1024.0)  as decimal(18,2)) 
FROM    #perfmon_counters   
WHERE   counter_name = 'Cursor memory usage' and instance_name = '_Total'  
UNION ALL  
SELECT  'Total pages Size (MB)',   
       CAST( (cntr_value*@pg_size)/1048576.0    as decimal(18,2))
FROM    #perfmon_counters   
WHERE   object_name= @Instancename+'Buffer Manager'   
        and counter_name = 'Total pages'  
UNION ALL  
SELECT  'Database pages (MB)',   
        CAST((cntr_value*@pg_size)/1048576.0   as decimal(18,2))
FROM    #perfmon_counters   
WHERE   object_name = @Instancename+'Buffer Manager' and counter_name = 'Database pages'  
UNION ALL  
SELECT  'Free pages (MB)',   
       CAST( (cntr_value*@pg_size)/1048576.0   as decimal(18,2))
FROM    #perfmon_counters   
WHERE   object_name = @Instancename+'Buffer Manager'   
        and counter_name = 'Free pages'  
UNION ALL  
SELECT  'Reserved pages (MB)',   
       CAST( (cntr_value*@pg_size)/1048576.0   as decimal(18,2))
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Buffer Manager'   
        and counter_name = 'Reserved pages'  
UNION ALL  
SELECT  'Stolen pages (MB)',   
       CAST( (cntr_value*@pg_size)/1048576.0   as decimal(18,2))
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Buffer Manager'   
        and counter_name = 'Stolen pages'  
UNION ALL  
SELECT  'Cache Pages (MB)',   
       CAST( (cntr_value*@pg_size)/1048576.0   as decimal(18,2))
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Plan Cache'   
        and counter_name = 'Cache Pages' and instance_name = '_Total'  
UNION ALL  
SELECT  'Free list stalls/sec',  
        cntr_value   
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Buffer Manager'   
        and counter_name = 'Free list stalls/sec'  
UNION ALL  
SELECT  'Checkpoint pages/sec',  
        cntr_value   
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Buffer Manager'   
        and counter_name = 'Checkpoint pages/sec'  
UNION ALL  
SELECT  'Lazy writes/sec',  
        cntr_value   
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Buffer Manager'   
        and counter_name = 'Lazy writes/sec'  
UNION ALL  
SELECT  'Memory Grants Pending',  
        cntr_value   
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Memory Manager'   
        and counter_name = 'Memory Grants Pending'  
UNION ALL  
SELECT  'Memory Grants Outstanding',  
        cntr_value   
FROM    #perfmon_counters   
WHERE   object_name=@Instancename+'Memory Manager'   
        and counter_name = 'Memory Grants Outstanding'  
UNION ALL  
SELECT  'Process_Physical_Memory_Low',  
        process_physical_memory_low   
FROM    sys.dm_os_process_memory WITH (NOLOCK)  
UNION ALL  
SELECT  'Process_Virtual_Memory_Low',  
        process_virtual_memory_low   
FROM    sys.dm_os_process_memory WITH (NOLOCK)  
UNION ALL  
SELECT  'Max_Server_Memory (MB)' ,  
        [value_in_use]   
FROM    sys.configurations   
WHERE   [name] = 'max server memory (MB)'  
UNION ALL  
SELECT  'Min_Server_Memory (MB)' ,  
        [value_in_use]   
FROM    sys.configurations   
WHERE   [name] = 'min server memory (MB)') AS P;  

-------------------------------------------------------------------------------
/*******************************DB Size*********************************/


Create table #fixeddrives ([drive] varchar(1), [MB Free] int)
insert into #fixeddrives ([drive], [MB Free])
exec xp_fixeddrives

Create table #DBSize (
DBName varchar(50),
Drive varchar(2),
File_Size_MB int,
Disk_Free_GB int
)
insert into #DBSize
 select DB_NAME(F.dbid) as [DBName],
SUBSTRING (F.filename, 1, 1) as Drive
,sum((F.size*8)/1024) as [File_Size_MB]--,*
,D.[MB Free]/1024 as Disk_Free_GB
from sys.sysaltfiles F
left join #fixeddrives D 
on SUBSTRING (F.filename, 1, 1) =D.[drive]
where dbid>4 and groupid=1 --and growth>0 
and DB_NAME(dbid) is not null
group by DB_NAME(dbid), SUBSTRING (filename, 1, 1),D.[MB Free]
order by DB_NAME(dbid)
-------------------------------------------------------------------------------
/******************************log space***************************************/

CREATE TABLE #LogSpace(  
DBName VARCHAR(100),  
LogSize VARCHAR(50),  
LogSpaceUsed_Percent VARCHAR(100),   
LStatus CHAR(1));  
  
INSERT INTO #LogSpace  
EXEC ('DBCC SQLPERF(LOGSPACE) WITH NO_INFOMSGS;');  
------------------------------------------------------------
/*************************************************************/  
/****************** Tempdb File Info *************************/  
/*************************************************************/  
-- tempdb file usage  
Create table #tempdbfileusage(               
servername varchar(100),                           
databasename varchar(100),                           
filename varchar(100),                           
physicalName varchar(100),                           
filesizeMB varchar(100),                           
availableSpaceMB varchar(100),                           
percentfull varchar(100)   
)   
  
DECLARE @TEMPDBSQL NVARCHAR(4000);  
SET @TEMPDBSQL = ' USE Tempdb;  
SELECT  CONVERT(VARCHAR(100), @@SERVERNAME) AS [server_name]  
                ,db.name AS [database_name]  
                ,mf.[name] AS [file_logical_name]  
                ,mf.[filename] AS[file_physical_name]  
                ,convert(FLOAT, mf.[size]/128) AS [file_size_mb]               
                ,convert(FLOAT, (mf.[size]/128 - (CAST(FILEPROPERTY(mf.[name], ''SpaceUsed'') AS int)/128))) as [available_space_mb]  
                ,convert(DECIMAL(38,2), (CAST(FILEPROPERTY(mf.[name], ''SpaceUsed'') AS int)/128.0)/(mf.[size]/128.0))*100 as [percent_full]      
FROM   tempdb.dbo.sysfiles mf  
JOIN      master..sysdatabases db  
ON         db.dbid = db_id()';  
--PRINT @TEMPDBSQL;  
insert into #tempdbfileusage  
EXEC SP_EXECUTESQL @TEMPDBSQL;  

---------------------------------------------------------------------
/******************************Filtered Errorlogs******************************************/
declare @endtime datetime = (select getdate()),
@starttime datetime=(select dateadd(hh,-24,getdate()))
Create table #errorlogs ([LogDate] datetime, [ProcessInfo] varchar(10), [Text] Varchar(1000))
insert into #errorlogs ([LogDate], [ProcessInfo],[Text])
Exec xp_ReadErrorLog 0,1,null,null,@starttime,@endtime,N'asc'
--select top (20) [LogDate],[Text] from #errorlogs
--where ProcessInfo not in ('Backup','Logon') and [Text] not like '%No user action is required%'
--order by [LogDate] desc

-------------------------------------------AG Status-------------------------------------------------------

Create table #AGStatus(
ag_name varchar(50),
replica_server_name varchar(50),
database_name varchar(50),
database_state varchar(50),
synchronization_state varchar(50),
synchronization_health varchar(50),

replica_role varchar(50)


)
Insert into #AGStatus
SELECT  ag.name ag_name ,
        ar.replica_server_name ,
        adc.database_name ,
        hdrs.database_state_desc ,
        hdrs.synchronization_state_desc ,
        hdrs.synchronization_health_desc ,
        --agl.dns_name ,
 --       SERVERPROPERTY('productversion') as BuildNumber
 --,
 case 
 when is_primary_replica =1 then 'Primary'
 else 'Secondary'
 end as [Replica_Role]
 
 
FROM    sys.dm_hadr_database_replica_states hdrs
        LEFT JOIN sys.availability_groups ag ON hdrs.group_id =ag.group_id
        LEFT  JOIN sys.availability_replicas ar ON ag.group_id = ar.group_id
                                                   AND ar.replica_id = hdrs.replica_id
        LEFT  JOIN sys.availability_databases_cluster adc ON adc.group_id = ag.group_id
                                                             AND adc.group_database_id = hdrs.group_database_id
        LEFT  JOIN sys.availability_group_listeners agl ON agl.group_id = ag.group_id
where ar.replica_server_name=@@servername
ORDER BY ag.name , adc.database_name
-----------------------------------------------------------------------------------------------------------
/**********************************************************************************************************
*************************************HTML Prep*************************************************************
**********************************************************************************************************/
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
DECLARE                                    
  @StrSubject VARCHAR(100),                                    
  @Oriserver VARCHAR(100),                                
  @Version VARCHAR(100),                                
  @ISClustered VARCHAR(100),                                
  @AlwaysOn  VARCHAR(100),                            
  @Cnt int,           
  @URL varchar(1000),                                
  @Str varchar(1000),                                
  @NoofCriErrors varchar(3)       
  
-- Variable Assignment              
  
SELECT @Version = CONVERT(VARCHAR(100),serverproperty('ProductVersion') )                               
SET @Cnt = 0                                
IF serverproperty('IsClustered') = 0                                 
BEGIN                                
 SELECT @ISClustered = 'No'                                
END                                
ELSE        
BEGIN                                
 SELECT @ISClustered = 'YES'                                
END     
IF serverproperty('Ishadrenabled') = 0                                 
BEGIN                                
 SELECT @AlwaysOn = 'No'                                
END                                
ELSE        
BEGIN                                
 SELECT @AlwaysOn = 'YES'                                
END  

  
SET @TableHTML =
'
<!DOCTYPE html>
<html>
<head>
<style>
body {
  background-color: white;
  margin-left: 50px;
  margin-top: 50px;
}

h2 {
  color: Darkblue;
  margin-left: 30%;
}
h3 {
  color: Darkblue;
  margin-left: 5px;
}
table  {
  border: 1px solid black;
  width:80%;

page-break-inside: avoid;
}
th  {
  border: 1px solid black;
  background-color: lightblue;
  align-content: center;
}
td  {
  border: 1px solid black;
  align-content: center;
}
</style>
</head>
<body>
'  


SET @TableHTML = @TableHTML +                                     
 '<div><img align="right" src="C:\InventoryV2\icons\inventory.ico" style="height: 50px; width: 50px"/><font ><H2><bold>Database Health Check Report</bold></H2></font></div>                                  
 <table id="AutoNumber1">                                   
 <tr>                                  
 <th><b>                           
 <font>Server Name</font></b></th> 
  <th><b>                           
 <font>Build</font></b></th>
  <th><b>                           
 <font>IsClustered</font></b></th>
   <th><b>                           
 <font>AlwaysOn</font></b></th>
 </tr>                                  
 <tr>                                  
 <td >' + @ServerName +'</font></td>  
 <td align="center">' + @Version +'</font></td> 
 <td align="center">' + @ISClustered +'</font></td>
  <td align="center">' + @AlwaysOn +'</font></td>
 </tr>                                  
 </table>  
 <font><H3><bold>Instance last Recycled</bold></H3></font>                                  
 <table>                                      
 <tr>                                      
 <th width="33%">                                      
  <font>Last Recycle</font></th>                                      
 <th>                                      
  <font>Current DateTime</font></th>                                      
 <th>                                   
 <font>UpTimeInDays</font></th>                                      
  </tr>'                                  
 SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td width="33%" align="center">' + ISNULL(CONVERT(VARCHAR(100), LastRecycle ), '')  +'</font></td>' +                                        
 '<td align="center">' + ISNULL(CONVERT(VARCHAR(100),  CurrentDate ), '')  +'</font></td>' +                                   
 '<td align="center">' + ISNULL(CONVERT(VARCHAR(100),  UpTimeInDays ), '')  +'</font></td>' +                                        
  '</tr>'                                  
FROM                                   
 #RebootDetails 


 /***********************************suspect pages****************************************************/
  SELECT                                   
 @TableHTML = @TableHTML +                                     
 '</table>                                  
                                 
 <font><H3><bold>Suspect Pages</bold></H3></font>                                  
 <table>                                      
 <tr>                                      
 <th align="Center">                                      
  <font>Suspect Pages</font></th>                                                                           
  </tr>'  

 
 IF (select count(*) from msdb..suspect_pages) =0
       SELECT @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td align="center">' + 'No Suspect Pages'  +'</font></td>' +                                                                               
  '</tr>'   ;
else 
       SELECT @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td align="center" color="#FF0000">' + 'There are Suspect Pages in '+DB_NAME(database_id)  +'</font></td>' +                                                                               
  '</tr>'   
 
from msdb..suspect_pages;
  ---------------------------------------------------------------------------------------------------------------
  /****Backup ****/
  SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 2; margin-bottom: 2">&nbsp;</p>                                  
 <font ><H3><bold>Last Backup</bold></H3></font>                                  
 <table>                                  
   <tr>                
 <th>                                    
 <font>DBName</font></th>                              
  <th>               
 <font>Recovery Model</font></th>
  <th>               
 <font>Last Full Backup</font></th>
   <th>               
 <font>Last Differrential Backup</font></th>
   <th>               
 <font>Last LOG Backup</font></th>               
   </tr>' 
SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td ><font>' + ISNULL(CONVERT(VARCHAR(200),  DBName ), '')  +'</font></td>' +                                        
 '<td><font>' + ISNULL(CONVERT(VARCHAR(100),  recovery_model ), '')  +'</font></td>' +  
  '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(200),  [Last Full Backup] ), '')  +'</font></td>' +                                        
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  [Last Differential Backup] ), '')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(200),  [Last log Backup] ), '')  +'</font></td>' +                                      
  '</tr>'                                  
FROM                                   
 #Backup_Report;  




  
/**** CPU Usage *****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 2; margin-bottom: 2">&nbsp;</p>                                  
 <font ><H3><bold>CPU Usage</bold></H3></font>                                  
 <table>                                  
   <tr>                
 <th>                                    
 <font>System Time</font></th>               
 <th>                                    
 <font>SQLProcessUtilization</font></th>               
 <th align="Center" width="200" bgColor="#0000ff">                                    
 <font>SystemIdle</font></th>               
 <th align="Center" width="200" bgColor="#0000ff">                                    
 <font>OtherProcessUtilization</font></th>               
 <th align="Center" width="200" bgColor="#0000ff">               
 <font>load DateTime</font></th>               
   </tr>'                                  
SELECT                                   
 @TableHTML =  @TableHTML +                                     
 '<tr>' +                                      
 '<td align="Center"><font>' + ISNULL(CONVERT(VARCHAR(100), EventTime2 ), '')  +'</font></td>' +    
  '<td align="Center"><font>' + ISNULL(CONVERT(VARCHAR(100), SQLProcessUtilization ), '')  +'</font></td>' +    
   '<td align="Center"><font>' + ISNULL(CONVERT(VARCHAR(100), SystemIdle ), '')  +'</font></td>' +                              
   '<td align="Center"><font>' + ISNULL(CONVERT(VARCHAR(100), OtherProcessUtilization ), '')  +'</font></td>' +                              
  '<td align="Center"><font>' + ISNULL(CONVERT(VARCHAR(100), load_date ), '')  +'</font></td> </tr>'                                  
FROM                                   
 #CPU  ORDER BY EventTime2; 


  
/***** Memory Usage ****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 2; margin-bottom: 2">&nbsp;</p>                                  
 <font ><H3><bold>Memory Usage</bold></H3></font>                                  
 <table id="AutoNumber1" >                                  
   <tr>                
 <th align="left">                                    
 <font>Parameter</font></th>                              
  <th>               
 <font>Value</font></th>              
   </tr>'                                  
SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td><font>' + ISNULL(CONVERT(VARCHAR(200),  Parameter ), '')  +'</font></td>' +                                        
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  Value ), '')  +'</font></td>' +                                     
  '</tr>'                                  
FROM                                   
 #Memory ORDER BY ID;   

  ---------------------------------------------------------------------------------------------------------------
/***** Performance Counter Values ****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 2; margin-bottom: 2">&nbsp;</p>                                  
 <font ><H3><bold>Performance Counter Data</bold></H3></font>                                  
 <table id="AutoNumber1" >                                  
   <tr>                
 <th align="left">                                    
 <font>Performance_Counter</font></th>                              
  <th>               
 <font>Value</font></th>              
   </tr>'                                  
SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td><font>' + ISNULL(CONVERT(VARCHAR(300),  Parameter ), '')  +'</font></td>' +                                        
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  Value ), '')  +'</font></td>' +                                     
  '</tr>'                                  
FROM                                   
 #PerfCntr_Data ORDER BY ID;   
  
  
  /***** JOB STATUS ****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 2; margin-bottom: 2">&nbsp;</p>                                  
 <font ><H3><bold>SQL JOB Status</bold></H3></font>                                  
 <table id="AutoNumber1">                                  
   <tr>                
 <th align="left">                                    
 <font>job name</font></th>                              
  <th>               
 <font>job status</font></th>                              
  <th>               
 <font>last run status</font></th>   
   <th>               
 <font>last run datetime</font></th> 
   <th>               
 <font>last run duration</font></th> 
   <th>               
 <font>next run datetime</font></th> 
   <th>               
 <font>details</font></th>            
   </tr>'                                  
SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  job_name ), '')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  job_status ), '')  +'</font></td>' +  
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  last_run_status ), '')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  last_run_dt ), '')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  duration ), '')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  next_scheduled_dt ), '')  +'</font></td>' +  
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  step_description ), '')  +'</font></td>' +                                                                        
  '</tr>'                               
FROM                                   
 #JOBSTATUS

   /***** AG STATUS ****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 1; margin-bottom: 0">&nbsp;</p>                                  
 <font ><H3><bold>AG Status</bold></H3></font>                                  
 <table id="AutoNumber1" >                                  
   <tr>                
 <th align="left" width="136" bgColor="#0000ff">                                    
 <font>ag name</font></th>                              
  <th>               
 <font>replica_hostname</font></th>                              
  <th>               
 <font>DB Name</font></th>   
   <th>               
 <font>DB Status</font></th> 
   <th>               
 <font>synchronization state</font></th> 
   <th>               
 <font>synchronization health</font></th> 
   <th>               
 <font>replica role</font></th>            
   </tr>'                                  
SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  ag_name ), 'NA')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  replica_server_name ), 'NA')  +'</font></td>' +  
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  database_name ), 'NA')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  database_state ), 'NA')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  synchronization_state ), 'NA')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  synchronization_health ), 'NA')  +'</font></td>' +  
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  replica_role ), 'NA')  +'</font></td>' +                                                                        
  '</tr>'                               
FROM                                   
 #AGStatus

    /***** DB Size ****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 1; margin-bottom: 0">&nbsp;</p>                                  
 <font ><H3><bold>Datafiles space</bold></H3></font>                                  
 <table id="AutoNumber1" >                                  
   <tr>                
 <th align="left" >                                    
 <font>DBName</font></th>                              
  <th>               
 <font>Drive</font></th>                              
  <th>               
 <font>File_Size_MB</font></th>   
   <th>               
 <font>Disk_Free_GB</font></th>            
   </tr>'                                  
SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td><font>' + ISNULL(CONVERT(VARCHAR(100),  DBName ), 'NA')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  Drive ), 'NA')  +'</font></td>' +  
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  File_Size_MB ), 'NA')  +'</font></td>' + 
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  Disk_Free_GB ), 'NA')  +'</font></td>' +                                                                       
  '</tr>'                               
FROM                                   
 #DBSize

       
/***** Log Space Usage ****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 1; margin-bottom: 0">&nbsp;</p>                                  
 <font ><H3><bold>Database Log Space Usage</bold></H3></font>                                  
 <table id="AutoNumber1" >                                  
   <tr>                
 <th align="left" width="136" bgColor="#0000ff">                                    
 <font>DatabaseName</font></th>                              
  <th>               
 <font>Log_Space_Used_MB</font></th>                              
  <th>               
 <font>Log_Usage_%</font></th>              
   </tr>'                                  
SELECT                                   
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td><font>' + ISNULL(CONVERT(VARCHAR(100),  DBName ), '')  +'</font></td>' +                                        
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  CAST(LogSize as decimal (10,2)) ), '')  +'</font></td>' +   
 CASE WHEN CONVERT(DECIMAL(10,3),LogSpaceUsed_Percent) >80.00 THEN  
  '<td align="center"><font color="#FF0000"><b>' + ISNULL(CONVERT(VARCHAR(100),  CAST(LogSpaceUsed_Percent as decimal (10,2)) ), '')  +'</b></font></td>'  
 ELSE  
 '<td align="center"><font>' + ISNULL(CONVERT(VARCHAR(100),  CAST(LogSpaceUsed_Percent as decimal (10,2)) ), '')  +'</font></td>'   
 END +                                     
  '</tr>'                               
FROM                                   
 #LogSpace
 where DBName not in ('master','msdb','model')   
  
  
/**** Tempdb File Usage *****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <font><H3><bold>Tempdb File Usage</bold></H3></font>                                  
 <table id="AutoNumber1">                                  
   <tr>                
 <th >                                    
 <font >Database Name</font></th>               
 <th >                                    
 <font >File Name</font></th>               
 <th align="Center" width="250" bgColor="#000080">                                    
 <font >Physical Name</font></th>               
 <th align="Center" width="250" bgColor="#000080">                                
 <font >FileSize MB</font></th>               
 <th align="Center" width="200" bgColor="#000080">               
 <font >Available MB</font></th>               
 <th align="Center" width="200" bgColor="#000080">                                    
 <font >Percent_full </font></th>               
   </tr>'                                  
select                                   
@TableHTML =  @TableHTML +                                     
 '<tr>' +                                      
 '<td align="Center"><font>' + ISNULL(databasename, '') + '</font></td>' +                                      
 '<td align="Center"><font>' + ISNULL(FileName, '') +'</font></td>' +                                      
 '<td align="Center"><font>' + ISNULL(physicalName, '') +'</font></td>' +                                      
 '<td align="Center"><font>' + ISNULL(filesizeMB, '') +'</font></td>' +                                  
 '<td align="Center"><font>' + ISNULL(availableSpaceMB, '') +'</font></td>' +  
 CASE WHEN CONVERT(DECIMAL(10,3),percentfull) >80.00 THEN    
'<td align="Center"><font color="#FF0000"><b>' + ISNULL(percentfull, '') +'</b></font></td></tr>'                                               
 ELSE  
 '<td align="Center"><font>' + ISNULL(percentfull, '') +'</font></td></tr>' END                                
from                                   
 #tempdbfileusage   
  ---------------------------------------------------------------------
  /***** filtered errorlogs ****/  
SELECT                                   
 @TableHTML =  @TableHTML +                              
 '</table>                                  
 <p style="margin-top: 1; margin-bottom: 0">&nbsp;</p>                                  
 <font ><H3><bold>Filtered errorlogs</bold></H3></font>                                  
 <table id="AutoNumber1" >                                  
   <tr>                
 <th align="left" >                                    
 <font>Timestamp</font></th>                              
  <th>               
 <font>Details</font></th>                                            
   </tr>'                                  
SELECT   top (30)                                
 @TableHTML =  @TableHTML +                                       
 '<tr>                                    
 <td ><font>' + ISNULL(CONVERT(VARCHAR(100),  logdate ), '')  +'</font></td>' +                                        
 '<td ><font>' + ISNULL(CONVERT(VARCHAR(100),  [text] ), '')  +'</font></td>' +                                       
  '</tr>'                               
FROM                                   
 #errorlogs
 --sp_readerrorlog
where ProcessInfo not in ('Backup','Logon','Server') 
and [Text] not like '%No user action is required%' 
and [Text] != 'The Service Broker endpoint is in disabled or stopped state.'
and [Text] not like '%Microsoft Corporation%'
and [Text] not like '%UTC adjustment:%'
and [Text] not like '%All rights reserved%'
and [Text] not like '%Server process ID is%'
and [Text] not like '%System Manufacturer:%'
and [Text] not like '%Authentication mode is%'
and [Text] not like '%Logging SQL Server messages in file%'
and [Text] not like 'Default collation:%'
and [Text] not like 'Default collation:%'
and [Text] not like '%INFO%'
--order by [LogDate] desc
SELECT                              
 @TableHTML =  @TableHTML +  '</table>' +                                  
 '<p style="margin-top: 2; margin-bottom: 2">&nbsp;</p>                                  
 <p>&nbsp;</p>'  
 SELECT @TableHTML "SQL Health Check";  

IF OBJECT_ID('tempdb..#RebootDetails') IS NOT NULL DROP TABLE #RebootDetails;
IF OBJECT_ID('tempdb..#errorlogs') IS NOT NULL DROP TABLE #errorlogs;
IF OBJECT_ID('tempdb..#CPU') IS NOT NULL DROP TABLE #CPU;
IF OBJECT_ID('tempdb..#Memory_BPool') IS NOT NULL DROP TABLE #Memory_BPool;
IF OBJECT_ID('tempdb..#Memory_sys') IS NOT NULL DROP TABLE #Memory_sys;
IF OBJECT_ID('tempdb..#Memory_process') IS NOT NULL DROP TABLE #Memory_process;
IF OBJECT_ID('tempdb..#Memory') IS NOT NULL DROP TABLE #Memory;
IF OBJECT_ID('tempdb..#perfmon_counters') IS NOT NULL DROP TABLE #perfmon_counters;
IF OBJECT_ID('tempdb..#PerfCntr_Data') IS NOT NULL DROP TABLE #PerfCntr_Data;
IF OBJECT_ID('tempdb..#Backup_Report') IS NOT NULL DROP TABLE #Backup_Report;
IF OBJECT_ID('tempdb..#DBSize') IS NOT NULL DROP TABLE #DBSize;
IF OBJECT_ID('tempdb..#JOBSTATUS') IS NOT NULL DROP TABLE #JOBSTATUS;
IF OBJECT_ID('tempdb..#fixeddrives') IS NOT NULL DROP TABLE #fixeddrives;
IF OBJECT_ID('tempdb..#LogSpace') IS NOT NULL DROP TABLE #LogSpace;
IF OBJECT_ID('tempdb..#AGStatus') IS NOT NULL DROP TABLE #AGStatus;
IF OBJECT_ID('tempdb..#tempdbfileusage') IS NOT NULL DROP TABLE #tempdbfileusage;

SET NOCOUNT OFF;  
SET ARITHABORT OFF;  
END  
END TRY
BEGIN CATCH
    DECLARE @msg NVARCHAR(255);
    SET @msg = 'An error occurred: ' + ERROR_MESSAGE();
    RAISERROR (50002, 10, 127);
END CATCH

