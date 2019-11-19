# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Options Widget = View - Tab of DNS Reduction GUI
"""
from __future__ import (absolute_import, division, print_function)
from qtpy.QtCore import Signal
from DNSReduction.data_structures.dns_view import DNSView

#from DNSReduction.helpers.mapping_creator import mapping_creator
#mapper = mapping_creator(self._content)

try:
    from mantidqt.utils.qt import load_ui
except ImportError:
    from mantidplot import load_ui


class DNSTofOptions_view(DNSView):
    """
        Widget that lets user select redcution options
    """
    name = "Options"

    def __init__(self, parent):
        super(DNSTofOptions_view, self).__init__(parent)
        self._content = load_ui(__file__, 'tof_options.ui', baseinstance=self)
        #mapper = mapping_creator(self._content)
        self._mapping = {'vanadium_temperature': self._content.dSB_vanadium_temperature,
                         'substract_background_from_vanadium': self._content.cB_substract_background_from_vanadium,
                         'dEmin': self._content.dSB_dEmin,
                         'correct_elastic_peak_position': self._content.cB_correct_elastic_peak_position,
                         'qmax': self._content.dSB_qmax,
                         'epp_channel': self._content.SB_epp_channel,
                         'qmin': self._content.dSB_qmin,
                         'dEmax': self._content.dSB_dEmax,
                         'dEstep': self._content.dSB_dEstep,
                         'corrections': self._content.gB_corrections,
                         'wavelength': self._content.dSB_wavelength,
                         'det_efficency': self._content.cB_det_efficency,
                         'delete_raw': self._content.cB_delete_raw,
                         'monitor_normalization': self._content.cB_monitor_normalization,
                         'qstep': self._content.dSB_qstep,
                         'background_factor': self._content.dSB_background_factor,
                         'substract_background': self._content.cB_substract_background,
                         'mask_bad_detectors' : self._content.cB_mask_bad_detectors,
                        }
        self._content.pB_get_wavelength.clicked.connect(self.get_wavelength)
        self._content.pB_estimate.clicked.connect(self.estimate_q_and_binning)

    sig_get_wavelength = Signal()
    sig_estimate_q_and_binning = Signal()

    def get_wavelength(self):
        self.sig_get_wavelength.emit()

    def estimate_q_and_binning(self):
        self.sig_estimate_q_and_binning.emit()
