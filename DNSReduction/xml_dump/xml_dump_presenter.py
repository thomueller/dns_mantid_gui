# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:52:08 2019

@author: thomasm
"""

from __future__ import (absolute_import, division, print_function)
from DNSReduction.xml_dump import xml_helper
from DNSReduction.data_structures.dns_observer import DNSObserver
from DNSReduction.xml_dump.xml_dump_view import DNSXMLDump_view

class DNSXMLDump_presenter(DNSObserver):
    name = 'xml'
    def __init__(self, parent):
        super(DNSXMLDump_presenter, self).__init__(parent, 'xml_dump')
        self.name = 'xml_dump'
        self.view = DNSXMLDump_view(None)

    def save_xml(self):
        xml_file_path = self.view.get_save_filename()
        if xml_file_path:
            options = self.param_dict
            xml_helper.dic_to_xml_file(options, xml_file_path)
        return xml_file_path

    def load_xml(self):
        xml_file_path = self.view.get_load_filename()
        options = xml_helper.xml_file_to_dict(xml_file_path)
        if options is None:
            print('No DNS xml file')
        return options


    def set_view_from_param(self):
        pass
