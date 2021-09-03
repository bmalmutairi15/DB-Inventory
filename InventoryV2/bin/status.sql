BEGIN
	SET NOCOUNT ON;
IF SERVERPROPERTY ('IsHadrEnabled') = 1 and SERVERPROPERTY ('IsClustered') = 0
BEGIN
SELECT
--'AG Primary Replica' as [Role]
ARS.role_desc as [Role]
 ,RCS.replica_server_name as [hostname]

FROM sys.dm_hadr_availability_replica_cluster_states AS RCS
INNER JOIN sys.dm_hadr_availability_replica_states AS ARS
ON ARS.replica_id = RCS.replica_id
--WHERE ARS.role_desc = 'PRIMARY'
WHERE ARS.is_local = 1
END
IF SERVERPROPERTY ('IsClustered') = 1 and SERVERPROPERTY ('IsHadrEnabled') =0
BEGIN
SELECT 'FCI Active Node' as [Role],NodeName as [hostname] FROM sys.dm_os_cluster_nodes where is_current_owner=1
END
IF SERVERPROPERTY ('IsClustered') = 0 and SERVERPROPERTY ('IsHadrEnabled') = 0
BEGIN
SELECT 'Standalone' as [Role], CAST(SERVERPROPERTY('MachineName') as nvarchar(50)) as [hostname]
END
END