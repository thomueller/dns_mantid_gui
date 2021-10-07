# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Tof Sc Options widget
"""
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import DNSWidget
from mantidqtinterfaces.DNSReduction.options.common_options_model import DNSCommonOptionsModel
from mantidqtinterfaces.DNSReduction.options.tof_sc_options_presenter import \
    DNSTofScOptionsPresenter
from mantidqtinterfaces.DNSReduction.options.tof_sc_options_view import DNSTofScOptionsView


class DNSTofScOptionsWidget(DNSWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.view = DNSTofScOptionsView(parent=parent.view)
        self.model = DNSCommonOptionsModel(parent=self)
        self.presenter = DNSTofScOptionsPresenter(parent=self,
                                                  view=self.view,
                                                  model=self.model,
                                                  name=name)
