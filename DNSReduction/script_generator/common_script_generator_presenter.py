# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
presenter for dns path panel
"""

from __future__ import (absolute_import, division, print_function)
import os
from collections import OrderedDict
from qtpy.QtCore import Signal
from mantidqt.gui_helper import get_qapplication
from DNSReduction.data_structures.dns_observer import DNSObserver
from DNSReduction.script_generator.common_script_generator_view import DNSScriptGenerator_view
from DNSReduction.data_structures.dns_error import DNSError

class DataSet(object):
    def __init__(self):
        super(DataSet, self).__init__()
        self.sample = StandardType()
        self.vana = StandardType()
        self.nicr = StandardType()
        self.leer = StandardType()


class StandardType(object):
    def __init__(self):
        super(StandardType, self).__init__()
        self.x = FieldType()
        self.y = FieldType()
        self.z = FieldType()
        self.other = FieldType()

class FieldType(object):
    def __init__(self):
        super(FieldType, self).__init__()
        self.sf = []
        self.nsf = []
        self.other = []

def list_to_range(value_list):
    if len(value_list) > 3:
        increment = value_list[1] - value_list[0]
        arange = range(value_list[0], value_list[-1] + increment, increment)
        if value_list == arange:
            return 'range({}, {}, {})'.format(value_list[0], value_list[-1] + increment, increment)
    return str(value_list)

def list_to_multirange(value_list):
    """
    some very ugly script, to create range commands from list of numbers
    should find some better method
    """
    range_string = ''
    if len(value_list) > 5:

        start = 0
        increment = value_list[start + 1] - value_list[start]
        for i, value in enumerate(value_list):
            if i == len(value_list)-1 or value + increment != value_list[i+1]:
                end = i+1
                if range_string:
                    range_string = ' + '.join((range_string, list_to_range(value_list[start:end])))
                else:
                    range_string = list_to_range(value_list[start:end])
                start = end
                if start < len(value_list)-1:
                    increment = value_list[start+1] - value_list[start]
        range_string = range_string.replace("] + [", ", ")
    if not range_string:
        range_string = value_list
    return range_string

class DNSScriptGenerator_presenter(DNSObserver):

     # pass the view and model into the presenter
    def __init__(self, parent, name=None, view=None):
        if name is None:
            self.name = 'script_generator'
        else:
            self.name = name
        super(DNSScriptGenerator_presenter, self).__init__(parent, name)
        if view is None:
            self.view = DNSScriptGenerator_view(self.parent.view)
        else:
            self.view = view
        # connect statements
        self.view.sig_generate_script.connect(self.generate_script)
        self.data = DataSet()
        self.app = get_qapplication()[0]
        self.scriptpath = ''
        self.view.sig_progress_canceled.connect(self.progress_canceled)
        self.number_of_empty_banks = None
        self.script = None
        self.number_of_vana_banks = None
        self.number_of_banks = None
        self.progress_is_canceled = False
        self.script_number = 0 ## ID of generated script is used to indetify new scripts for plotting

    def save_script(self, script):
        own_options = self.get_option_dict()
        filename = own_options['script_filename']
        if filename:
            if not filename.endswith('.py'):
                filename = ''.join((filename, ''))
        else:
            filename = 'script.py'
            self.view.set_filename(filename)
        scriptpath = ''.join((self.param_dict['paths']['script_dir'], '/', filename))
        if self.param_dict['paths']['script_dir']:
            self.view.show_statusmessage('script saved to: {}'.format(scriptpath), 30, clear=True)
            if not os.path.exists(self.param_dict['paths']['script_dir']):
                os.makedirs(self.param_dict['paths']['script_dir'])
            with open(scriptpath, 'w') as myfile:
                myfile.write(script)
            return scriptpath
        else:
            self.raise_error('No script filepath set, script will not be saved.')
            return False

    def progress_canceled(self):
        self.progress_is_canceled = True


    def generate_script(self):
        sampledata = self.param_dict['file_selector']['full_data']
        if not sampledata:
            self.raise_error('no data selected', critical=True)
            return
        self.sig_request_from_abo.emit() ### should be catched by main presenter
        #to ask other observer for automatic data reduction
        script = self.script_maker()
        if script:
            scripttext = "\n".join(script)
            self.view.set_script_output(scripttext)
            self.app.processEvents() ## update script texedit before running script
            self.scriptpath = self.save_script(scripttext)
            self.progress_is_canceled = False
            self.view.open_progress_dialog(len(script)-1)
            self.app.processEvents()
            for i, line in enumerate(script):
                print(line)
                try:
                    exec(line)
                except DNSError as errormessage:
                    self.raise_error(str(errormessage))
                self.view.set_progress(i)
                if self.progress_is_canceled:
                    self.view.show_statusmessage('Warning script execution stopped, no valid data.', 30, clear=True)
                    return
        self.script_number += 1
        return

    def preprocess_filelist(self, alldata):
        rounding_limit = 0.05
        files_dict = {}
        for  dnsfile in alldata:
            det_rot = dnsfile['det_rot']
            inside = [x for x in files_dict.keys() if abs(float(x)-det_rot) < rounding_limit]
            if inside:
                files_dict[inside[0]] += [dnsfile['filenumber']]
            else:
                files_dict[str(round(det_rot/rounding_limit)*rounding_limit)] = [dnsfile['filenumber']]
        new_dict = OrderedDict()
        keylist = sorted([float(x) for x in files_dict.keys()], reverse=True)
        for key in keylist:
            new_dict[str(key)] = files_dict[str(key)]
        return new_dict

    def get_option_dict(self):
        if self.view is not None:
            self.own_dict.update(self.view.get_state())
        self.own_dict['script_path'] = self.scriptpath
        self.own_dict['script_number'] = self.script_number
        return self.own_dict

    sig_script_generation_started = Signal()

    def script_maker(self):
        self.script = [""]
        return self.script
