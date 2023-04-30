@echo off
For %%i In ("*.adm") Do (
"tldat.exe" "%%i"
)
del *.adm