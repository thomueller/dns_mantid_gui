# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Path Configuration Widget = View - Tab of DNS Reduction GUI
"""
from __future__ import (absolute_import, division, print_function)

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib import backend_bases

from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator, NullLocator
from mantid.simpleapi import mtd
try:
    from mantidqt.utils.qt import load_ui
except ImportError:
    from mantidplot import load_ui
from mantidqt import icons
from DNSReduction.data_structures.dns_view import DNSView
from DNSReduction.data_structures.dns_plot_list import DNSPlotListModel


## remove subplot from toolbar
backend_bases.NavigationToolbar2.toolitems = (
    ('Home', 'Reset original view', 'home', 'home'),
    ('Back', 'Back to  previous view', 'back', 'back'),
    ('Forward', 'Forward to next view', 'forward', 'forward'),
    (None, None, None, None),
    ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
    ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
    (None, None, None, None),
    ('Save', 'Save the figure', 'filesave', 'save_figure'),
   )



class DNSElasticPowderPlot_view(DNSView):
    """
        Widget that lets user save or load data reduction xml files
    """
    ## Widget name
    name = "Paths"

    def __init__(self, parent):
        super(DNSElasticPowderPlot_view, self).__init__(parent)
        self._content = load_ui(__file__, 'elastic_powder_plot.ui', baseinstance=self)
        self.name = 'Plotting'
        self.xml_filepath = None
        self.main_view = parent
        self.has_tab = True
        self.layout = self._content.plot_layout
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3), dpi=200))
        self.static_canvas.setSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.static_canvas, self)
        self.plot_head_layout.addWidget(self.toolbar)
        self.plot_head_layout.addStretch()

        self.layout.addWidget(self.static_canvas)
        self._mapping = {'datalist' :  self._content.lV_datalist,
                         'down' : self._content.tB_down,
                         'up' : self._content.tB_up,
                         'raw' : self._content.tB_raw,
                         'separated' : self._content.tB_separated,
                         'deselect' : self._content.tB_deselect,
                         'grid' : self._content.tB_grid,
                         'log_scale' : self._content.cB_log_scale,
                         'linestyle' : self._content.tB_linestyle,
                         'errorbar' : self._content.tB_errorbar,
                        }
        self._mapping['down'].setIcon(icons.get_icon("mdi.arrow-down"))
        self._mapping['up'].setIcon(icons.get_icon("mdi.arrow-up"))
        self._mapping['deselect'].setIcon(icons.get_icon("mdi.close"))
        self._mapping['grid'].setIcon(icons.get_icon("mdi.grid"))
        self._mapping['linestyle'].setIcon(icons.get_icon("mdi.ray-vertex"))
        self._mapping['errorbar'].setIcon(icons.get_icon("mdi.format-size"))

        self.datalist = self._mapping['datalist']
        self.hasplot = False
        self.ax = None
        self.cb = None
        self.plotmin = None
        self.cl = None
        self.workspace = None
        self.plotmax = None
        self.minimum = None
        self.maximum = None
        self.hasplot = False
        self.static_canvas.figure.tight_layout()
        self.model = DNSPlotListModel(self.datalist)
        self.model.itemChanged.connect(self.set_plot)
        self._mapping['down'].clicked.connect(self.model.down)
        self._mapping['up'].clicked.connect(self.model.up)
        self._mapping['deselect'].clicked.connect(self.model.uncheck_items)
        self._mapping['separated'].clicked.connect(self.model.check_seperated)
        self._mapping['grid'].clicked.connect(self.set_grid)
        self._mapping['log_scale'].stateChanged.connect(self.set_log)
        self._mapping['raw'].clicked.connect(self.model.check_raw)
        self._mapping['linestyle'].clicked.connect(self.change_linestyle)
        self._mapping['errorbar'].clicked.connect(self.change_errorbar)
        self.gridstate = 0
        self.linestyles = {0 : '-',
                           1 : '.',
                           2 : '.-',}
        self.linestyle = 0
        self.errorbar = 0
    sig_plot = Signal()

    def change_errorbar(self):
        self.errorbar = (self.errorbar + 1) % 3
        self.set_plot()

    def change_linestyle(self):
        self.linestyle = (self.linestyle + 1) %3
        self.set_plot()


    def set_datalist(self, datalist):
        self.model.set_items(datalist)
        self.datalist.setModel(self.model)


    def clear_plot(self):
        if self.ax:
            self.ax.figure.clear()
        self.hasplot = False


    def plot(self):
        self.sig_plot.emit()

    def set_log(self, state, draw=True):
        if state:
            self.ax.set_yscale('symlog')
        else:
            self.ax.set_yscale('linear')
        self.ax.figure.canvas.draw()

    def set_grid(self, dummy, draw=True):
        if draw:
            self.gridstate = (self.gridstate + 1) % 3
        if self.gridstate == 1:
            self.ax.xaxis.set_minor_locator(NullLocator())
            self.ax.grid(self.gridstate, which='both', zorder=-1000, linestyle='--')
        elif self.gridstate == 2:
            self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
            self.ax.grid(self.gridstate, which='both', zorder=-1000, linestyle='--')
        else:
            self.ax.xaxis.set_minor_locator(NullLocator())
            self.ax.grid(0)
        if draw:
            self.ax.figure.canvas.draw()



    def set_plot(self):
        if self.ax:
            self.ax.figure.clear()
        self.ax = self.static_canvas.figure.subplots(subplot_kw={'projection':'mantid'})

        self.ax.set_title('Elastic Powder')
        for item in self.model.get_checked_item_names():
            if self.errorbar:
                self.ax.errorbar(mtd[item], self.linestyles[self.linestyle], specNum=1, label=item, capsize=(self.errorbar-1)*3)
            else:
                self.ax.plot(mtd[item], self.linestyles[self.linestyle], specNum=1, label=item)
        self.ax.legend()
        self.set_grid(0, draw=False)
        self.set_log(self._mapping['log_scale'].checkState())

        #norm = colors.Normalize(vmin=self.minimum, vmax=self.maximum)
        #self.cl = self.ax.pcolor(workspace, norm=norm)
       # self.cb = self.static_canvas.figure.colorbar(self.cl)
       # self.cb.set_label('Intensity normed to monitor')
        #self.plotmin, self.plotmax = self.cl.get_clim()
        #self.minimum = self.plotmin
        #self.maximum = self.plotmax
        self.hasplot = True
        #self.cl.set_clim(vmin=self.minimum, vmax=self.maximum)
        self.static_canvas.figure.tight_layout()
