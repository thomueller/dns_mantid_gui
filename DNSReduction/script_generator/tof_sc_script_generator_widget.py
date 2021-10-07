# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Path widget
"""
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import DNSWidget
from mantidqtinterfaces.DNSReduction.script_generator.common_script_generator_view import \
    DNSScriptGeneratorView
from mantidqtinterfaces.DNSReduction.script_generator.tof_sc_script_generator_presenter import \
    DNSTofScScriptGeneratorPresenter


class DNSTofScScriptGeneratorWidget(DNSWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.view = DNSScriptGeneratorView(parent=parent.view)
        self.model = None
        self.presenter = DNSTofScScriptGeneratorPresenter(parent=self,
                                                          view=self.view,
                                                          model=self.model,
                                                          name=name)
