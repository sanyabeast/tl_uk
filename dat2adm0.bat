@echo off
For %%i In ("*.dat") Do (
"tldat.exe" "%%i"
)
del *.dat