# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
Common Presenter for DNS Script generators
"""

import numpy as np
from mantid.simpleapi import mtd

from mantidqtinterfaces.DNSReduction.data_structures.dns_dataset import DNSDataset
from mantidqtinterfaces.DNSReduction.helpers.list_range_converters import get_normation
from mantidqtinterfaces.DNSReduction.script_generator.common_script_generator_model import \
    DNSScriptGeneratorModel


class DNSElasticSCScriptGeneratorModel(DNSScriptGeneratorModel):
    """
    Common Model for DNS Script generators
    """
    def __init__(self, parent):
        # pylint: disable=too-many-instance-attributes
        # having the options as instance attribues, is much better readable
        # none of them are public
        super().__init__(parent)
        self._data_arrays = {}
        self._script = []
        self._plotlist = []
        self._sample_data = None
        self._standard_data = None
        self._loop = None
        self._spac = None
        self._vanac = None
        self._nicrc = None
        self._sampb = None
        self._backfac = None
        self._ign_vana = None
        self._sum_sfnsf = None
        self._nonmag = None
        self._xyz = None
        self._corrections = None
        self._export_path = None
        self._ascii = None
        self._nexus = None
        self._norm = None

    def script_maker(self, options, paths, fselector=None):
        self._script = []
        # shortcuts for options
        self._vanac = options['corrections'] and options['det_efficency']
        self._nicrc = options['corrections'] and options['flipping_ratio']
        self._sampb = (options['corrections']
                       and options['substract_background_from_sample'])
        self._backfac = options['background_factor']
        self._ign_vana = str(options['ignore_vana_fields'])
        self._sum_sfnsf = str(options['sum_vana_sf_nsf'])
        self._xyz = options["separation"] and options['separation_xyz']
        self._nonmag = options["separation"] and options['separation_coh_inc']

        self._corrections = (self._sampb or self._vanac or self._nicrc)
        self._export_path = paths["export_dir"]
        self._ascii = (paths["ascii"] and paths["export"]
                       and bool(self._export_path))
        self._nexus = (paths["nexus"] and paths["export"]
                       and bool(self._export_path))
        self._norm = get_normation(options)


        self._setup_sample_data(paths, fselector)
        self._setup_standard_data(paths, fselector)
        self._interpolate_standard()
        self._set_loop()

        # startin wrting script
        self._add_lines_to_script(self._get_header_lines())
        self._add_lines_to_script(self._get_sample_data_lines())
        self._add_lines_to_script(self._get_standard_data_lines())
        self._add_lines_to_script(self._get_param_lines(options))
        self._add_lines_to_script(self._get_binning_lines())
        self._add_lines_to_script(self._get_load_data_lines())
        self._add_lines_to_script(self._get_bg_corr_lines())
        self._add_lines_to_script(self._get_vanac_lines())
        self._add_lines_to_script(self._get_nicrc_lines())
        return self._script

    def _setup_sample_data(self, paths, fselector):
        self._sample_data = DNSDataset(data=fselector['full_data'],
                                       path=paths['data_dir'],
                                       issample=True)
        self._plotlist = self._sample_data.create_plotlist()

    def _setup_standard_data(self, paths, fselector):
        if self._corrections:
            self._standard_data = DNSDataset(data=fselector['standard_data'],
                                             path=paths['standards_dir'],
                                             issample=False,
                                             fields=self._sample_data.fields)

    def _interpolate_standard(self):
        self._standard_data.interpolate_standard(
            banks=self._sample_data.banks,
            scriptname=self._sample_data.scriptname,
            parent=self)

    def _set_loop(self):
        if len(self._sample_data.keys()) == 1:
            self._loop = "for workspace in wss_sample['{}']:" \
                         "".format(list(self._sample_data.keys())[0])
            self._spac = "\n" + " " * 4
        else:
            self._loop = "for sample, workspacelist in wss_sample.items(): " \
                         "\n    for workspace in workspacelist:"
            self._spac = "\n" + " " * 8

    @staticmethod
    def _get_header_lines():
        lines = [
            'from mantidqtinterfaces.DNSReduction.scripts.md_sc_elastic import load_all',
            'from mantidqtinterfaces.DNSReduction.scripts.md_sc_elastic import '
            'vanadium_correction, fliping_ratio_correction',
            'from mantidqtinterfaces.DNSReduction.scripts.md_sc_elastic import'
            ' background_substraction',
            'from mantid.simpleapi import ConvertMDHistoToMatrixWorkspace,'
            ' mtd',
            'from mantid.simpleapi import SaveAscii, SaveNexus', ''
        ]
        return lines

    def _get_sample_data_lines(self):
        return ['sample_data = {}'.format(self._sample_data.format_dataset())]

    def _get_standard_data_lines(self):
        if self._corrections:
            return [
                'standard_data = {}'
                ''.format(self._standard_data.format_dataset())
            ]
        return ['']

    def _get_param_lines(self, options):

        return ["", "params = {{'a' : {0}, "
                "\n          'b' : {1},"
                "\n          'c' : {2},"
                "\n          'alpha' : {3},"
                "\n          'beta'  : {4},"
                "\n          'gamma' : {5},"
                "\n          'hkl1'  : '{6}',"
                "\n          'hkl2'  : '{7}',"
                "\n          'omega_offset' : {8},"
                "\n          'norm_to' : '{9}',"
                "\n          'dx' : '{10:7.4f}',"
                "\n          'dy' : '{11:7.4f}',"
                "}}".format(options['a'],
                            options['b'],
                            options['c'],
                            options['alpha'],
                            options['beta'],
                            options['gamma'],
                            options['hkl1'],
                            options['hkl2'],
                            options['omega_offset'],
                            self._norm,
                            options['dx'],
                            options['dy'],
                            ), ""]

    def _get_binning_lines(self):
        lines = [
            "binning = {{'twoTheta' : [{:.3f}, {:.3f}, {:d}],\n" \
            "           'Omega':  [{:.3f}, {:.3f}, {:d}]}} # min, max," \
            " number_of_bins".format(
                self._sample_data.ttheta.bin_edge_min,
                self._sample_data.ttheta.bin_edge_max,
                self._sample_data.ttheta.nbins,
                self._sample_data.omega.bin_edge_min,
                self._sample_data.omega.bin_edge_max,
                self._sample_data.omega.nbins)]
        return lines

    def _get_load_data_lines(self):
        lines = [
            "wss_sample = load_all(sample_data, binning, params)"
            .format(self._norm)
        ]
        if self._corrections:
            lines += [("wss_standard = load_all(standard_data, "
                       "binning, params, standard=True,"
                       ")".format(self._norm))]
        lines += ['']
        return lines

    def _get_bg_corr_lines(self):
        lines = []
        if self._vanac or self._nicrc:
            lines = [
                "# substract background from vanadium and nicr",
                "for sample, workspacelist in wss_standard.items(): "
                "\n    for workspace in workspacelist:"
                "\n        background_substraction(workspace)", ""
                ]
        return lines

    def _return_sample_bg_string(self):
        return "{}background_substraction(workspace, " \
               "factor={})".format(self._spac, self._backfac)

    def _return_sample_vanac_strinf(self):
        return "{}vanadium_correction(workspace, " \
               " vanaset=standard_data['vana'], " \
               "ignore_vana_fields={}, " \
               "sum_vana_sf_nsf={})".format(
                    self._spac, self._ign_vana, self._sum_sfnsf)

    def _get_vanac_lines(self):
        backgroundstring = self._return_sample_bg_string()
        vanacstring = self._return_sample_vanac_strinf()
        lines = []
        if self._sampb or self._vanac:
            lines = ["# correct sample data",
                     "{}{}{}".format(
                        self._loop, backgroundstring, vanacstring)]
        return lines

    def _get_nicrc_lines(self):
        lines = []
        if self._nicrc:
            lines = ["{}{}fliping_ratio_correction(workspace)"
                     .format(self._loop, self._spac)]
        return lines

    def get_plotlist(self):
        for plot in self._plotlist:
            self._data_arrays[plot] = {
                'ttheta': self._sample_data.ttheta.range,
                'omega': self._sample_data.omega.range,
                'intensity': mtd[plot].getSignalArray(),
                'error': np.sqrt(mtd[plot].getErrorSquaredArray())
            }
        return self._plotlist, self._data_arrays
