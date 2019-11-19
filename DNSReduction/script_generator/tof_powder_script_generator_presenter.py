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
from DNSReduction.script_generator.common_script_generator_presenter import DNSScriptGenerator_presenter


class DNSTofPowderScriptGenerator_presenter(DNSScriptGenerator_presenter):

     # pass the view and model into the presenter
    def __init__(self, parent):
        super(DNSTofPowderScriptGenerator_presenter, self).__init__(parent, 'tof_powder_script_generator')

    def script_maker(self):
        self.script = [""]
        def l(line=""):
            self.script += [line]
        sampledata = self.param_dict['file_selector']['full_data']
        tof_opt = self.param_dict['tof_powder_options']
        if (tof_opt['dEstep'] == 0 or tof_opt['qstep'] == 0 or
                tof_opt['qmax'] <= tof_opt['qmin'] or
                tof_opt['dEmax'] <= tof_opt['dEmin']):
            self.raise_error('Bin sizes make no sense.', critical=True)
            return False
        standarddata = self.param_dict['file_selector']['standard_data']
        vanadata = [data for data in standarddata if data['sampletype'] == 'vana']
        emptydata = [data for data in standarddata if data['sampletype'] == 'empty']
        ppsample = self.preprocess_filelist(sampledata)
        self.number_of_banks = len(ppsample)
        ppvana = self.preprocess_filelist(vanadata)
        self.number_of_vana_banks = (len(ppvana))
        ppempty = self.preprocess_filelist(emptydata)
        self.number_of_empty_banks = (len(ppempty))
        sppsample = str(ppsample).replace("]), (", "]),\n                                            (")
        sppvana = str(ppvana).replace("]), (", "]),\n                                            (")
        sppempty = str(ppempty).replace("]), (", "]),\n                                            (")
        vanadium_correction = False
        background_correction = False

        if self.number_of_vana_banks > 0 and tof_opt['corrections'] and tof_opt['det_efficency']:
            vanadium_correction = True
        if self.number_of_empty_banks > 0 and tof_opt['corrections']:
            background_correction = True
        if self.number_of_banks == 0:
            self.raise_error('No data selected.', critical=True)
            return False
        if self.number_of_vana_banks == 0 and  tof_opt['corrections'] and tof_opt['det_efficency']:
            self.raise_error('No vanadium files selected, but Vanadium correction option choosen.')
            return False
        if (self.number_of_empty_banks == 0 and
                tof_opt['corrections'] and
                (tof_opt['substract_background_from_vanadium'] or tof_opt['substract_background'])):
            self.raise_error('No Background files selected, but background substraction option choosen.')
            return False
        l("import numpy as np")
        l("from mantid.simpleapi import *")
        l("from DNSReduction.scripts.dnstof import *")
        l("from collections import OrderedDict")
        l()
        l("data   = {{'data_path'        : '{}',".format(self.param_dict['paths']['data_dir']) +
          "\n         'proposal_number'  : '{}',".format(self.param_dict['paths']['prop_nb']) +
          "\n          'data_numbers'     : {} }}".format(sppsample))
        if vanadium_correction:
            l("vana   = {{'data_path'        : '{}',".format(self.param_dict['paths']['standards_dir']) +
              "\n         'proposal_number'  : '{}',".format(self.param_dict['paths']['prop_nb']) +
              "\n          'data_numbers'     : {} }}".format(sppvana))
        if background_correction:
            l("empty  = {{'data_path'        : '{}',".format(self.param_dict['paths']['standards_dir']) +
              "\n          'proposal_number'  : '{}',".format(self.param_dict['paths']['prop_nb']) +
              "\n          'data_numbers'     : {} }}".format(sppempty))



        paramstring = ("params = {{'e_channel'        : {}, ".format(tof_opt['epp_channel']) +
                       "\n          'wavelength'       : {},".format(tof_opt['wavelength']) +
                       "\n          'delete_raw'       : {},".format(tof_opt['delete_raw']))
        if vanadium_correction:
            paramstring += "\n          'vana_temperature' : {},".format(tof_opt['vanadium_temperature'])
        if background_correction and tof_opt['background_factor'] != 1:
            paramstring += "\n          'ecFactor'         : {},".format(tof_opt['background_factor'])
        paramstring += '}'
        l(paramstring)
        l()
        l("bins = {{'qmin' : {}, 'qmax' : {}, 'qstep' : {},".format(tof_opt['qmin'], tof_opt['qmax'], tof_opt['qstep']) +
          "\n        'dEmin': {}, 'dEmax': {}, 'dEstep': {}}}".format(tof_opt['dEmin'], tof_opt['dEmax'], tof_opt['dEstep']))
        l()
        l('load_data(data, "raw_data1", params)')
        if background_correction:
            l('load_data(empty, "raw_ec", params)')
        if vanadium_correction:
            l('load_data(vana, "raw_vanadium", params)')
        l("")
        if tof_opt['monitor_normalization']:
            l('# normalize')
            l('data1 = MonitorEfficiencyCorUser("raw_data1")')
        else:
            l('data1 = mtd["raw_data1"]')
        if background_correction:
            l('ec =  MonitorEfficiencyCorUser("raw_ec")')
        if vanadium_correction:
            l('vanadium =  MonitorEfficiencyCorUser("raw_vanadium")')
        if background_correction and tof_opt['background_factor'] != 1:
            l('# scale empty can')
            if self.number_of_empty_banks != self.number_of_banks:
                l("ec = params['ecFactor']*ec[0]")
            else:
                l("ec = params['ecFactor']*ec")
            if tof_opt['substract_background']:
                l()
                l('# subtract empty can')
                l('data1 = data1- ec')

        if vanadium_correction:
            if tof_opt['substract_background_from_vanadium'] and background_correction:
                l('vanadium = vanadium - ec')
            if self.number_of_vana_banks != self.number_of_banks: ### number of banks differs
                l('# only one vandium bank position')
                l('vanadium = vanadium[0]')
                l()
            l('# detector efficciency correction: compute coefficients')
            l('epptable = FindEPP(vanadium)')
            l("coefs = ComputeCalibrationCoefVan(vanadium, epptable, Temperature=params['vana_temperature'])")
            l()
            if tof_opt['mask_bad_detectors']:
                l('# get list of bad detectors')
                if self.number_of_vana_banks > 0:
                    l('badDetectors = np.where(np.array(coefs[0].extractY()).flatten() <= 0)[0]')
                else:
                    l('badDetectors = np.where(np.array(coefs.extractY()).flatten() <= 0)[0]')
                l('print("Following detectors will be masked: ", badDetectors)')
                l('MaskDetectors(data1, DetectorList=badDetectors)')
                l()
            l('# apply detector efficiency correction')
            l('data1 = Divide(data1, coefs)')
            if tof_opt['correct_elastic_peak_position']:
                l()
                l('# correct TOF to get EPP at 0 meV')
                l('data1 = CorrectTOF(data1, epptable)')
                l()
        l('# get Ei')
        l("Ei = data1[0].getRun().getLogData('Ei').value")
        l('print ("Incident Energy is {} meV".format(Ei))')
        l()
        l('# get S(q,w)')
        l("convert_to_dE('data1', Ei)")
        l()
        l('# merge al detector positions together')
        l("get_sqw('data1_dE_S', 'data1', bins)")
        return self.script
