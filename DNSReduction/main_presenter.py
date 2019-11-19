# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
Reduction GUI for DNS Instrument at MLZ
"""
from __future__ import (absolute_import, division, print_function)
from DNSReduction.main_model import DNSReductionGUI_model
from DNSReduction.dns_modus import DNSModus

class ParameterAbo(object):
    ### observers are the presenters of the tabs of the gui or xml_dumper
    ### they are instances of DNSObserver and have a
    ### argument name which is a unique string
    ### and a method update which can get information from the gui parameters
    ### they are passive in relation to this presenter, just react on .get_option_dict() calls
    ### they can have their own view to which only they interact

    def __init__(self):
        self.observers = []
        self.gui_parameter = DNSReductionGUI_model() ## Ordered Dictionary

    def register(self, observer):
        if observer not in self.observers: ## do not allow multiple registrations, should not happen anyhow
            self.observers.append(observer)
            observer.sig_request_from_abo.connect(self.process_request)
        self.update_from_observer(observer)

    def unregister(self, observer):
        observer.sig_request_from_abo.disconnect()
        self.observers.remove(observer)

    def clear(self):
        for observer in self.observers:
            observer.sig_request_from_abo.disconnect()
        self.observers = []

    def notify_observers(self):
        gui_param = self.gui_parameter.get()
        for observer in self.observers:
            observer.update(gui_param)

    def notify_focused_tab(self, observer):
        observer.tab_got_focus()

    def xml_load(self, gui_param):
        self.gui_parameter.set_whole_dict(gui_param)
        self.notify_observers()
        for observer in self.observers:
            observer.set_view_from_param()

    def update_from_observer(self, observer):
        self.gui_parameter.update(observer.name, observer.get_option_dict())
        self.notify_observers()

    def update_from_all_observers(self):
        """
        this functions gets data from all observers
        """
        for observer in self.observers:
            self.gui_parameter.update(observer.name, observer.get_option_dict())
        self.notify_observers()

    def process_request(self):
        for observer in self.observers:
            observer.process_request()
        self.update_from_all_observers()

class DNSReductionGUI_presenter(object):
    """
    main gui presenter for dns presenter is onwed by View which is the MainWindow
    """
    def __init__(self, view):
        self.view = view
        self.view.sig_tab_changed.connect(self.tab_changed)
        self.view.sig_save_as_triggered.connect(self.save_as)
        self.view.sig_open_triggered.connect(self.load_xml)
        self.view.sig_modus_change.connect(self.switch_mode)
        self.view.clear_subviews()
        self.modus = DNSModus('powder_elastic', parent=self)
        self.parameter_abo = ParameterAbo()
        for presenter in self.modus.presenters.values():
            self.view.add_subview(presenter.view)
            self.parameter_abo.register(presenter)
        self.switch_mode('powder_elastic')

        return

    def tab_changed(self, oldtabindex, tabindex):
        oldview = self.view.get_view_for_tabindex(oldtabindex)
        actualview = self.view.get_view_for_tabindex(tabindex)
        for observer in self.parameter_abo.observers:
            if observer.view == oldview:
                self.parameter_abo.update_from_observer(observer)
        for observer in self.parameter_abo.observers:
            if observer.view == actualview:
                self.parameter_abo.notify_focused_tab(observer)

    def save_as(self):
        self.parameter_abo.update_from_all_observers()
        self.modus.presenters['xml_dump'].save_xml()

    def load_xml(self):
        gui_param = self.modus.presenters['xml_dump'].load_xml()
        if gui_param is not None:
            self.parameter_abo.xml_load(gui_param)

    def switch_mode(self, modus):
        self.view.clear_subviews()
        self.parameter_abo.clear()
        self.modus.change(modus)
        for name, presenter in self.modus.presenters.items():
            self.parameter_abo.register(presenter)
            if presenter.view.has_tab:
                self.view.add_subview(presenter.view)
