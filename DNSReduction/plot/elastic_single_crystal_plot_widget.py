# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Elastic SC Plot widget
"""
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import DNSWidget
from mantidqtinterfaces.DNSReduction.plot.elastic_single_crystal_plot_model import \
    DNSElasticSCPlotModel
from mantidqtinterfaces.DNSReduction.plot.elastic_single_crystal_plot_presenter import \
    DNSElasticSCPlotPresenter
from mantidqtinterfaces.DNSReduction.plot.elastic_single_crystal_plot_view import \
    DNSElasticSCPlotView


class DNSElasticSCPlotWidget(DNSWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.view = DNSElasticSCPlotView(parent=parent.view)
        self.model = DNSElasticSCPlotModel(parent=self)
        self.presenter = DNSElasticSCPlotPresenter(parent=self,
                                                   view=self.view,
                                                   model=self.model,
                                                   name=name)
