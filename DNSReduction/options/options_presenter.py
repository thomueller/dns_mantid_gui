# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2019 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Options Presenter - Tab of DNS Reduction GUI
"""
from __future__ import (absolute_import, division, print_function)

from DNSReduction.data_structures.dns_observer import DNSObserver
from DNSReduction.options.options_view import DNSOptions_view



class DNSOptions_presenter(DNSObserver):

    def __init__(self, parent):
        super(DNSOptions_presenter, self).__init__(parent, 'options')
        self.name = 'options'
        self.view = DNSOptions_view(self.parent.view)
