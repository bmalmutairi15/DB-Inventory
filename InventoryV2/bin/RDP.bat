@echo off
setlocal
if “%1%” == “” (
pause
goto :eof
)
set DBserver=%~1%
set DomainUser=%2%
set sSeconds=10
cmdkey /generic:TERMSRV/%DBserver% /user:%DomainUser%
start mstsc /v:%DBserver%
ping -n %WaitTime% 127.0.0.1 >nul:
cmdkey /delete:TERMSRV/%DBserver%