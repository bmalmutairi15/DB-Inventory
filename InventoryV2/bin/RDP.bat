@echo off
setlocal
if “%1%” == “” (
pause
goto :eof
)
set sServer=%~1%
set sUser=%2%
set sSeconds=10
CMDKEY /generic:TERMSRV/%sServer% /user:%sUser%
start mstsc /v:%sServer%
ping -n %sSeconds% 127.0.0.1 >nul:
cmdkey /delete:TERMSRV/%sServer%