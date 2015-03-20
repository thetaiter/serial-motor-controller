#!/bin/bash
# INSTALL PYTHON 3.4 and Tkinter
sudo apt-get install python3.4 python3-tk

# DOWNLOAD AND INSTALL PYSERIAL
cd ~/Downloads
wget https://pypi.python.org/packages/source/p/pyserial/pyserial-2.7.tar.gz
tar -xvzf pyserial-2.7.tar.gz
cd pyserial-2.7
sudo python3 setup.py install

# CLEAN UP
sudo rm -r ~/Downloads/pyserial-2.7 ~/Downloads/pyserial-2.7.tar.gz
