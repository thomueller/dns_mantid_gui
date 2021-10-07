# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Elastic Powder Script Generator widget
"""
# yapf: disable
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import DNSWidget
from mantidqtinterfaces.DNSReduction.script_generator.common_script_generator_view import \
    DNSScriptGeneratorView
from mantidqtinterfaces.DNSReduction.script_generator.elastic_powder_script_generator_model \
    import DNSElasticPowderScriptGeneratorModel
from mantidqtinterfaces.DNSReduction.script_generator.elastic_powder_script_generator_presenter \
    import DNSElasticPowderScriptGeneratorPresenter
# yapf: enable


class DNSElasticPowderScriptGeneratorWidget(DNSWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.view = DNSScriptGeneratorView(parent=parent.view)
        self.model = DNSElasticPowderScriptGeneratorModel(parent=self)
        self.presenter = DNSElasticPowderScriptGeneratorPresenter(
            parent=self, view=self.view, model=self.model, name=name)
