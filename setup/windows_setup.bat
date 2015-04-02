title Windows Python Setup

bitsadmin /transfer "Python3.4.3 Download" https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi C:%HOMEPATH%\Downloads\python343.msi

call msiexec /i C:%HOMEPATH%\Downloads\python343.msi /qb TARGETDIR=C:\Python34 ALLUSERS=1 ADDLOCAL=ALL

del C:%HOMEPATH%\Downloads\python343.msi

C:\Python34\Scripts\pip install pyserial

echo Python 3.4 has been installed successfully.

pause