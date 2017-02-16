# gqrx-hamlib-gui

gqrxHamlib - a gqrx to Hamlib interface to keep frequency
between gqrx and a radio in sync when using gqrx as a panadaptor
using Hamlib to control the radio

The Hamlib daemon (rigctld) must be running, gqrx started with
the 'Remote Control via TCP' button clicked and
comms to the radio working otherwise an error will occur when
starting this program. Ports used are the defaults for gqrx and Hamlib.

Return codes from gqrx and Hamlib are printed to the GUI window

This program is written in Python 3.5/PyQt4


Installation
------------
SIP is a pre-requisite to PyQt4
Install SIP: 	https://www.riverbankcomputing.com/software/sip/download
		Extract downloaded file
		cd to extracted files		
		python3 configure.py
		make
		sudo make install

Install PyQt4*:  https://www.riverbankcomputing.com/software/pyqt/download
		Extract downloaded file
		cd to extracted files	
		python3 configure-ng.py
		make
		sudo make install

Install gqrxHamlib: sudo pip3 install gqrxHamlib

Run gqrxHamlib: type 'gqrxHamlib' at command prompt

*Unfortunately it is not possible to include PyQt4 in the gqrxHamlib pip install. 
