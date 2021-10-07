# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Options Presenter - Tab of DNS Reduction GUI
"""

from mantidqtinterfaces.DNSReduction.options.common_options_presenter import \
    DNSCommonOptionsPresenter


class DNSTofScOptionsPresenter(DNSCommonOptionsPresenter):
    def __init__(self, name=None, parent=None, view=None, model=None):
        super().__init__(parent=parent, name=name, view=view, model=model)
        self.view.sig_get_wavelength.connect(self._determine_wavelength)

    def process_request(self):
        self.get_option_dict()
