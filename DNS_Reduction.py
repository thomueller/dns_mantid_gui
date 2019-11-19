# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,

#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
Reduction module for DNS instrument at MLZ
"""
from __future__ import (absolute_import, division, print_function)
import sys
from qtpy import QtGui
from mantidqt.gui_helper import get_qapplication
from DNSReduction.main_view import DNSReductionGUI_view
app, within_mantid = get_qapplication()

reducer = DNSReductionGUI_view()
reducer.setWindowTitle('DNS Reduction GUI')
app.setWindowIcon(QtGui.QIcon('DNSReduction/dns_icon.png'))
reducer.show()
if not within_mantid:
    sys.exit(app.exec_())
