# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
sub widget for dns single crystal plot view
handling the list of plot files
"""

from qtpy.QtCore import QObject
from qtpy.QtCore import Signal

from mantidqtinterfaces.DNSReduction.data_structures.dns_plot_list import DNSPlotListModel


class DNSDatalist(QObject):
    def __init__(self, parent, view):
        super().__init__(parent)
        self._view = view
        self._parent = parent
        self._model = DNSPlotListModel(view)
        self._old_item = None
        self._model.itemChanged.connect(self._item_clicked)

    sig_datalist_changed = Signal()

    def up(self):
        self._model.itemChanged.disconnect()
        self._model.up()
        self._model.itemChanged.connect(self._item_clicked)
        self.sig_datalist_changed.emit()

    def down(self):
        self._model.itemChanged.disconnect()
        self._model.down()
        self._model.itemChanged.connect(self._item_clicked)
        self.sig_datalist_changed.emit()

    def check_first(self):
        self._model.itemChanged.disconnect()
        self._parent.draw()
        self._parent.app.processEvents()
        self._model.check_first()
        self._model.itemChanged.connect(self._item_clicked)
        self.sig_datalist_changed.emit()

    def get_checked_plots(self):
        return self._model.get_checked_item_names()

    def get_datalist(self):
        return self._model.get_names()

    def _item_clicked(self, item):
        self._model.itemChanged.disconnect()
        self._model.uncheck_items()
        item.setCheckState(2)
        self._model.itemChanged.connect(self._item_clicked)
        if not self._old_item == item:  # prevents double triggering
            self.sig_datalist_changed.emit()
        self._old_item = item

    def set_datalist(self, datalist):
        self._model.itemChanged.disconnect()
        self._model.set_items(datalist)
        self._view.setModel(self._model)
        self._model.itemChanged.connect(self._item_clicked)
