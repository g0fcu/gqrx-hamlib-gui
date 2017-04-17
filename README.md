# gqrx-hamlib-gui

gqrxHamlib - a gqrx to Hamlib interface to keep frequency
between gqrx and a radio in sync when using gqrx as a panadaptor
using Hamlib to control the radio

The Hamlib daemon (rigctld) must be running, gqrx started with
the 'Remote Control via TCP' button clicked and
comms to the radio working otherwise an error will occur when
starting this program. Ports used are the defaults for gqrx and Hamlib.

Return codes from gqrx and Hamlib are printed to the GUI window

This program is written in Python 3.5/PyQt4. From version 2.6.2 it requires Python 3.x to run.

Installation
------------
Install PyQt4 via your package manager if not already installed: sudo apt-get install python-qt4

Install gqrxHamlib: sudo pip install gqrxHamlib

Run gqrxHamlib: type 'gqrxHamlib' at command prompt

Copyright 2017 Simon Kennedy, G0FCU, g0fcu at g0fcu.com
