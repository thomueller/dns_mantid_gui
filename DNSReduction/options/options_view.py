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

from DNSReduction.data_structures.dns_view import DNSView

#from DNSReduction.DNSHelpers.mapping_creator import mapping_creator
#mapper = mapping_creator(self._content)

try:
    from mantidqt.utils.qt import load_ui
except ImportError:
    from mantidplot import load_ui


class DNSOptions_view(DNSView):
    """
        Widget that lets user select redcution options
    """
    name = "Options"

    def __init__(self, parent):
        super(DNSOptions_view, self).__init__(parent)
        self._content = load_ui(__file__, 'options.ui', baseinstance=self)
        #mapper = mapping_creator(self._content)
        self._mapping = {'multiple_scattering': self._content.dSB_multiple_scattering,
                         'norm_time': self._content.rB_norm_time,
                         'separation_coh_inc': self._content.rB_separation_coh_inc,
                         'sum_vana_det_pos': self._content.cB_sum_vana_det_pos,
                         'sum_vana_sf_nsf': self._content.cB_sum_vana_sf_nsf,
                         'ignore_vana_fields': self._content.cB_ignore_vana_fields,
                         'separation': self._content.gB_separation,
                         'det_efficency': self._content.cB_det_efficency,
                         'flipping_ratio': self._content.cB_flipping_ratio,
                         'separation_xyz': self._content.rB_separation_xyz,
                         'substract_background_from_sample': self._content.cB_substract_background_from_sample,
                         'corrections': self._content.gB_corrections,
                         'background_factor': self._content.dSB_background_factor,
                         'norm_monitor': self._content.rB_norm_monitor,
                        }
