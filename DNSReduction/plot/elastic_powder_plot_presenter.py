# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:52:08 2019

@author: thomasm
"""

from __future__ import (absolute_import, division, print_function)
from DNSReduction.data_structures.dns_observer import DNSObserver
from DNSReduction.plot.elastic_powder_plot_view import DNSElasticPowderPlot_view
from mantid.simpleapi import mtd



class DNSElasticPowderPlot_presenter(DNSObserver):
    name = 'plot_tof_powder'
    def __init__(self, parent):
        super(DNSElasticPowderPlot_presenter, self).__init__(parent, 'standard_data')
        self.name = 'plot_elastic_powder'
        self.view = DNSElasticPowderPlot_view(self.parent.view)
        self.view.sig_plot.connect(self.plot)
        self.plotted_script_number = 0
        self.script_plotted = False
        
    def set_view_from_param(self):
        pass

    def plot(self):
        try:
            workspace = mtd['mat_knso_x_nsf']
            self.view.set_plot(workspace)
            self.script_plotted = True
        except KeyError:
            self.raise_error('No processed data found, generate script first.')

    def tab_got_focus(self):
        if self.param_dict['elastic_powder_script_generator']['script_number'] != self.plotted_script_number:
            workspaces = [workspace for workspace in mtd.getObjectNames() if mtd[workspace].id() == 'Workspace2D']          
            self.view.set_datalist(workspaces)
            if self.param_dict['options']["separation"]:
                self.view.model.check_seperated()
            else:
                self.view.model.check_first()
            self.plotted_script_number = self.param_dict['elastic_powder_script_generator']['script_number']

    def process_auto_reduction_request(self):
        self.view.clear_plot()
        