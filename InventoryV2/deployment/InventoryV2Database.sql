USE [InventoryV2]
GO
/****** Object:  Table [dbo].[Keys]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Keys](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[key] [nvarchar](250) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[logs]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[logs](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[User] [nvarchar](50) NOT NULL,
	[Action] [nvarchar](50) NULL,
	[details] [nvarchar](2000) NULL,
	[DateTime] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Main]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Main](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Name] [nvarchar](50) NOT NULL,
	[Domain] [nvarchar](50) NULL,
	[col3] [nvarchar](50) NULL,
	[col4] [nvarchar](50) NULL,
	[col5] [nvarchar](50) NULL,
	[col6] [nvarchar](50) NULL,
	[col7] [nvarchar](50) NULL,
	[col8] [nvarchar](50) NULL,
	[col9] [nvarchar](50) NULL,
	[col10] [nvarchar](50) NULL,
	[col11] [nvarchar](50) NULL,
	[col12] [nvarchar](50) NULL,
	[col13] [nvarchar](50) NULL,
	[col14] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[scripts]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[scripts](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TAGs] [nvarchar](50) NULL,
	[Description] [nvarchar](200) NULL,
	[Script] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  StoredProcedure [dbo].[sp_countbycategory]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE     PROCEDURE [dbo].[sp_countbycategory] 

AS
BEGIN
  select col14,count(col14) as [Count] 
  from main
  where col14 !=''
  group by col14
END
GO
/****** Object:  StoredProcedure [dbo].[sp_countbyosversion]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_countbyosversion] 

AS
BEGIN
  select col12,count(col12) as [Count] 
  from main
  where col12 !=''
  group by col12
END
GO
/****** Object:  StoredProcedure [dbo].[sp_countbysqlversion]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_countbysqlversion] 

AS
BEGIN
  select col11,count(col11) as [Count] 
  from main
  where col11 !=''
  group by col11
END


GO
/****** Object:  StoredProcedure [dbo].[SP_delete]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO



CREATE   PROCEDURE [dbo].[SP_delete] 
(
	@col0 int
	 )
AS
BEGIN
   SET NOCOUNT ON;
   INSERT INTO [dbo].[logs]
   SELECT SUSER_Name(),'Delete',D.[Name]+', '+D.col3+', '+col4+', '+D.col5+', '+col6+', '+D.col7+', '+col8  ,GETDATE()
   FROM(
   Delete from [dbo].[Main]
   output DELETED.*
   where [ID]=@col0

)D

END


GO
/****** Object:  StoredProcedure [dbo].[SP_deletescript]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO




CREATE   PROCEDURE [dbo].[SP_deletescript] 
(
	@col0 int
	 )
AS
BEGIN
   SET NOCOUNT ON;
   Delete from [dbo].[SCRIPTS]
   where [ID]=@col0

END



GO
/****** Object:  StoredProcedure [dbo].[SP_insert]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[SP_insert] 
(
	@col1 [nvarchar](50)  ,
	@col2 [nvarchar](50) =NULL ,
	@col3 [nvarchar](50)=NULL ,
	@col4 [nvarchar](50) =NULL,
	@col5 [nvarchar](50)=NULL ,
	@col6 [nvarchar](50)=NULL ,
	@col7 [nvarchar](50)=NULL ,
	@col8 [nvarchar](50)=NULL ,
	@col9 [nvarchar](50) =NULL,
	@col10 [nvarchar](50)=NULL ,
	@col11 [nvarchar](50) =NULL,
	@col12 [nvarchar](50)=NULL ,
	@col13 [nvarchar](50)=NULL ,
	@col14 [nvarchar](50)=NULL )
AS
BEGIN
	SET NOCOUNT ON;
	
INSERT INTO [dbo].[Main]
           ([Name],
			[Domain],
			col3,
			col4 ,
			col5,
			col6,
			col7,
			col8,
			col9,
			col10,
			col11,
			col12,
			col13,
			col14)
     VALUES
           (@col1,
			@col2,
			@col3,
			@col4 ,
			@col5,
			@col6,
			@col7,
			@col8,
			@col9,
			@col10,
			@col11,
			@col12,
			@col13,
			@col14 )

END
GO
/****** Object:  StoredProcedure [dbo].[sp_insertscript]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[sp_insertscript] 
(
	@col1 [nvarchar](50)  ,
	@col2 [nvarchar](200) =NULL ,
	@col3 [nvarchar](max)=NULL )
AS
BEGIN
	SET NOCOUNT ON;
	SET QUOTED_IDENTIFIER OFF;
	
INSERT INTO [dbo].[SCRIPTS]
           ([TAGs]
           ,[Description]
           ,[Script]
           )
     VALUES
           (@col1,
			@col2,
			@col3)

END
GO
/****** Object:  StoredProcedure [dbo].[sp_instancecount]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_instancecount] 

AS
SET NOCOUNT ON
BEGIN
  select count(1) as [Instance Count] 
  from main
END
GO
/****** Object:  StoredProcedure [dbo].[sp_search]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO




CREATE   PROCEDURE [dbo].[sp_search] 
(
	@search [nvarchar](50)  
	 )
AS
BEGIN
  declare @search1 varchar(50)
  declare @search2 varchar(50)
  declare @count1 int
  SET NOCOUNT ON;
  set @search1= LTRIM(RTRIM(PARSENAME( REPLACE(@search,',','.'),2)))
  set @search2= LTRIM(RTRIM(PARSENAME( REPLACE(@search,',','.'),1)))
  set @count1= (select count(*) from STRING_SPLIT(@search,','))-- > 1
  if  @count1=1
    begin
    set @search='%'+@search+'%'

	
    select 
            [ID]
		   ,[Name]
           ,[Domain]
           ,col3
           ,col4
           ,col5
           ,col6
           ,col7
           ,col8
           ,col9
           ,col10
           ,col11
           ,col12
           ,col13
           ,col14
    FROM [dbo].[Main] 
	where ([Name] like @search)
	or ([Domain] like @search)
	or ([col3]  like @search)
	or (col4  like @search)
	or (col5  like @search)
	or (col6  like @search)
	or (col7  like @search)
	or (col8  like @search)
	or (col9  like @search)
	or (col10  like @search)
	or (col11  like @search)
	or (col12  like @search)
	or (col13  like @search)
	or (col14  like @search)

	end
	if  @count1=2
	begin
	set @search1='%'+@search1+'%'
	set @search2='%'+@search2+'%'

	
    select 
            [ID]
		   ,[Name]
           ,[Domain]
           ,[col3]
           ,col4
           ,col5
           ,col6
           ,col7
           ,col8
           ,col9
           ,col10
           ,col11
           ,col12
           ,col13
           ,col14
    FROM [dbo].[Main] 
	where ([Name] like @search1 OR [Name] like @search2)
	or ([Domain] like @search1 OR [Domain] like @search2)
	or ([col3]  like @search1 OR [col3]  like @search2)
	or (col4  like @search1 OR col4  like @search2)
	or (col5  like @search1 OR col5  like @search2)
	or (col6  like @search1 OR col6  like @search2)
	or (col7  like @search1 OR col7  like @search2)
	or (col8  like @search1 OR col8  like @search2)
	or (col9  like @search1 OR col9  like @search2)
	or (col10  like @search1 OR col10  like @search2)
	or (col11  like @search1 OR col11  like @search2)
	or (col12  like @search1 OR col12  like @search2)
	or (col13  like @search1 OR col13  like @search2)
	or (col14  like @search1 OR col14  like @search2)
	end
END
GO
/****** Object:  StoredProcedure [dbo].[sp_searchscripts]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO
CREATE   PROCEDURE [dbo].[sp_searchscripts] 
(
	@search [nvarchar](50)  
	 )
AS
BEGIN
  SET NOCOUNT ON;
  set @search='%'+LTRIM(RTRIM(@search))+'%'
  select [ID],[TAGs],[Description],[script]
  from SCRIPTS
  where [TAGs] like @search
  or [Description] like @search
END
GO
/****** Object:  StoredProcedure [dbo].[sp_servercount]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_servercount] 

AS
BEGIN
  select (select count(DISTINCT col4) from main where col4 !='')
+  (select count(DISTINCT col6) from main where col6 !='')
+  (select count(DISTINCT col8) from main where col8 !='')
as [Total Servers]
END

GO
/****** Object:  StoredProcedure [dbo].[sp_servicecount]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_servicecount] 

AS
SET NOCOUNT ON
BEGIN
  select count(distinct([Name])) as [service Count] 
  from main
END
GO
/****** Object:  StoredProcedure [dbo].[SP_Update]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[SP_Update] 
(   @col0 [int] ,
@ToBeUpdated [nvarchar](50),
	@NewVal [nvarchar](50) )
AS
BEGIN
	SET NOCOUNT ON;
if   @ToBeUpdated='Name'	
        update [dbo].[Main]
        set [Name]=@NewVal
		where  ID=@col0
if   @ToBeUpdated=N'col3'	
        update [dbo].[Main]
        set col3=@NewVal
		where  ID=@col0
if   @ToBeUpdated='Domain'	
        update [dbo].[Main]
        set [Domain]=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col4'	
        update [dbo].[Main]
        set col4=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col5'	
        update [dbo].[Main]
        set col5=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col6'	
        update [dbo].[Main]
        set col6=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col7'	
        update [dbo].[Main]
        set col7=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col8'	
        update [dbo].[Main]
        set col8=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col9'	
        update [dbo].[Main]
        set col9=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col10'	
        update [dbo].[Main]
        set col10=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col11'	
        update [dbo].[Main]
        set col11=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col12'	
        update [dbo].[Main]
        set col12=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col13'	
        update [dbo].[Main]
        set col13=@NewVal
		where  ID=@col0
if   @ToBeUpdated='col14'	
        update [dbo].[Main]
        set col14=@NewVal
		where  ID=@col0
END
GO
/****** Object:  StoredProcedure [dbo].[SP_updatescript]    Script Date: 9/3/2021 12:51:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO


CREATE PROCEDURE [dbo].[SP_updatescript] 
(   @col0 [int] ,
    @col1 [nvarchar](50),
	@col2 [nvarchar](200),
	@col3[nvarchar](max))
AS
BEGIN
    SET QUOTED_IDENTIFIER OFF
	update SCRIPTS 
	set TAGs=@col1,[Description]=@col2,Script=@col3
	where ID=@col0
END
GO
/*******insert one record for demo**********/
USE [InventoryV2]
GO
INSERT INTO [dbo].[Main]
     VALUES
           ('app name','MyDomain','Node1','IP1','Node2','IP2','DRNode','DRIP','Listener/virtual name','Listener/virtualIP','SQL Version','OS Version','Primary DBA','PORT #')
GO
