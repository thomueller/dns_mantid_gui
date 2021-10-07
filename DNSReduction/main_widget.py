# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS GUI Main widget
"""
from mantidqtinterfaces.DNSReduction.command_line.command_check import CommandLineReader
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import DNSWidget
from mantidqtinterfaces.DNSReduction.dns_modus import DNSModus
from mantidqtinterfaces.DNSReduction.main_presenter import DNSReductionGUIPresenter
from mantidqtinterfaces.DNSReduction.main_view import DNSReductionGUIView
from mantidqtinterfaces.DNSReduction.parameter_abo import ParameterAbo


class DNSReductionGuiWidget(DNSWidget):
    """Main DNS Gui widget, host, view, presenter, model"""
    def __init__(self, name=None, parent=None):
        super().__init__(name, parent)
        self.name = name
        self.view = DNSReductionGUIView()  # has no parent
        self.command_line_reader = CommandLineReader()
        self.parameter_abo = ParameterAbo()
        self.model = self.parameter_abo
        self.modus = DNSModus(name='powder_elastic', parent=self)
        self.presenter = DNSReductionGUIPresenter(
            parent=self,
            view=self.view,
            modus=self.modus,
            name=name,
            parameter_abo=self.parameter_abo,
            command_line_reader=self.command_line_reader)
