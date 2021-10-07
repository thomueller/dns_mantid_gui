# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Powder Plot widget
"""
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import DNSWidget
from mantidqtinterfaces.DNSReduction.plot.elastic_powder_plot_model import \
    DNSElasticPowderPlotModel
from mantidqtinterfaces.DNSReduction.plot.elastic_powder_plot_presenter import \
    DNSElasticPowderPlotPresenter
from mantidqtinterfaces.DNSReduction.plot.elastic_powder_plot_view import \
    DNSElasticPowderPlotView


class DNSElasticPowderPlotWidget(DNSWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.view = DNSElasticPowderPlotView(parent=parent.view)
        self.model = DNSElasticPowderPlotModel(parent=self)
        self.presenter = DNSElasticPowderPlotPresenter(parent=self,
                                                       view=self.view,
                                                       model=self.model,
                                                       name=name)
