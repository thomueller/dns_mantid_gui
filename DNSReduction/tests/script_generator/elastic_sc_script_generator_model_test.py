# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
Common Presenter for DNS Script generators
"""
import unittest
from unittest import mock
from unittest.mock import patch

from mantidqtinterfaces.DNSReduction.data_structures.dns_dataset import DNSDataset
from mantidqtinterfaces.DNSReduction.script_generator.common_script_generator_model import \
    DNSScriptGeneratorModel
from mantidqtinterfaces.DNSReduction.data_structures.dns_obs_model import DNSObsModel
from mantidqtinterfaces.DNSReduction.script_generator.elastic_sc_script_generator_model import \
    DNSElasticSCScriptGeneratorModel
from mantidqtinterfaces.DNSReduction.tests.helpers_for_testing import (get_fake_elastic_datadic,
                                                    get_elastic_standard_datadic,
                                                    get_fake_elastic_sc_options,
                                                    )


class DNSElasticSCScriptGeneratorModelTest(unittest.TestCase):
    # pylint: disable=protected-access, too-many-public-methods
    parent = None
    model = None
    sample_data = None
    standard_data = None
    fake_workspace = None

    @classmethod
    def setUpClass(cls):
        cls.parent = mock.Mock()
        cls.model = DNSElasticSCScriptGeneratorModel(parent=cls.parent)
        cls.sample_data = mock.create_autospec(DNSDataset)
        cls.model._sample_data = cls.sample_data
        cls.sample_data.datadic = get_fake_elastic_datadic()
        cls.sample_data.create_plotlist.return_value = ['knso_x_sf']
        cls.sample_data.format_dataset.return_value = '12345'
        cls.sample_data.fields = []
        cls.sample_data.ttheta = mock.Mock()
        cls.sample_data.ttheta.bin_edge_min = 1
        cls.sample_data.ttheta.bin_edge_max = 6
        cls.sample_data.ttheta.nbins = 5
        cls.sample_data.ttheta.range = [1, 2, 3]
        cls.sample_data.omega = mock.Mock()
        cls.sample_data.omega.bin_edge_min = 3
        cls.sample_data.omega.bin_edge_max = 5
        cls.sample_data.omega.nbins = 3
        cls.sample_data.omega.range = [4, 5, 6]
        cls.sample_data.scriptname = 'script.py'
        cls.sample_data.banks = [1, 2, 3]
        cls.standard_data = mock.create_autospec(DNSDataset)
        cls.model._standard_data = cls.standard_data
        cls.standard_data.datadic = get_elastic_standard_datadic()
        cls.standard_data.format_dataset.return_value = '123456'
        cls.standard_data.fields = []
        cls.standard_data.ttheta = mock.Mock()
        cls.standard_data.ttheta.bin_edge_min = 1
        cls.standard_data.ttheta.bin_edge_max = 6
        cls.standard_data.ttheta.nbins = 5
        cls.standard_data.banks = [1, 2, 3]
        cls.standard_data.omega = mock.Mock()
        cls.standard_data.omega.bin_edge_min = 3
        cls.standard_data.omega.bin_edge_max = 5
        cls.standard_data.omega.nbins = 3
        cls.standard_data.omega.range = [4, 5, 6]
        cls.standard_data.scriptname = '123.txt'

        cls.fake_workspace = mock.Mock()
        cls.fake_workspace.getErrorSquaredArray.return_value = 1
        cls.fake_workspace.getSignalArray.return_value = 4

    def test___init__(self):
        self.assertIsInstance(self.model, DNSElasticSCScriptGeneratorModel)
        self.assertIsInstance(self.model, DNSScriptGeneratorModel)
        self.assertIsInstance(self.model, DNSObsModel)
        self.assertTrue(hasattr(self.model, '_script'))
        self.assertTrue(hasattr(self.model, '_data_arrays'))
        self.assertTrue(hasattr(self.model, '_plotlist'))
        self.assertTrue(hasattr(self.model, '_sample_data'))
        self.assertTrue(hasattr(self.model, '_standard_data'))
        self.assertTrue(hasattr(self.model, '_loop'))
        self.assertTrue(hasattr(self.model, '_spac'))
        self.assertTrue(hasattr(self.model, '_vanac'))
        self.assertTrue(hasattr(self.model, '_nicrc'))
        self.assertTrue(hasattr(self.model, '_sampb'))
        self.assertTrue(hasattr(self.model, '_backfac'))
        self.assertTrue(hasattr(self.model, '_ign_vana'))
        self.assertTrue(hasattr(self.model, '_sum_sfnsf'))
        self.assertTrue(hasattr(self.model, '_nonmag'))
        self.assertTrue(hasattr(self.model, '_corrections'))
        self.assertTrue(hasattr(self.model, '_export_path'))
        self.assertTrue(hasattr(self.model, '_ascii'))
        self.assertTrue(hasattr(self.model, '_nexus'))
        self.assertTrue(hasattr(self.model, '_norm'))

    @patch('DNSReduction.script_generator.elastic_sc_script_generator_mod'
           'el.DNSDataset')
    def test_script_maker(self, mock_dns_dataset):
        mock_dns_dataset.return_value = self.standard_data
        options = {
            'corrections': 1,
            'det_efficency': 1,
            'flipping_ratio': 1,
            'substract_background_from_sample': 1,
            'background_factor': 1,
            'ignore_vana_fields': 1,
            'sum_vana_sf_nsf': 1,
            'separation': 1,
            'separation_xyz': 1,
            'separation_coh_inc': 1,
            'norm_monitor': 1
        }
        options.update(get_fake_elastic_sc_options())
        fselector = {'full_data': [], 'standard_data': []}
        paths = {
            'data_dir': '12',
            'standards_dir': '13',
            'export_dir': '14',
            'ascii': True,
            'nexus': True,
            'export': True
        }
        testv = self.model.script_maker(options, paths, fselector)
        self.assertTrue(self.model._vanac)
        self.assertTrue(self.model._nicrc)
        self.assertTrue(self.model._sampb)
        self.assertTrue(self.model._backfac)
        self.assertTrue(self.model._nonmag)
        self.assertTrue(self.model._xyz)
        self.assertTrue(self.model._corrections)
        self.assertTrue(self.model._ascii)
        self.assertTrue(self.model._nexus)
        self.assertEqual(self.model._ign_vana, '1')
        self.assertEqual(self.model._sum_sfnsf, '1')
        self.assertEqual(self.model._export_path, '14')
        self.assertEqual(self.model._norm, 'monitor')
        self.assertIsInstance(testv, list)
        lines = [55, 92, 70, 65, 49, 0, 20, 22, 0, 307, 0, 109, 51, 71, 0, 45,
                 130, 0,
                 21, 250, 129]
        for i, tv in enumerate(testv):
            self.assertEqual(len(tv), lines[i])
        options = {
            'corrections': 0,
            'det_efficency': 0,
            'flipping_ratio': 0,
            'substract_background_from_sample': 0,
            'background_factor': 0,
            'ignore_vana_fields': 0,
            'sum_vana_sf_nsf': 0,
            'separation': 0,
            'separation_xyz': 0,
            'separation_coh_inc': 0,
            'norm_monitor': 0
        }
        options.update(get_fake_elastic_sc_options())
        fselector = {'full_data': [], 'standard_data': []}
        paths = {
            'data_dir': '',
            'standards_dir': '',
            'export_dir': '',
            'ascii': False,
            'nexus': False,
            'export': False
        }
        testv = self.model.script_maker(options, paths, fselector)
        lines = [55, 92, 70, 65, 49, 0, 20, 0, 0, 304, 0, 109, 51, 0]
        for i, tv in enumerate(testv):
            self.assertEqual(len(tv), lines[i])
        options = {
            'corrections': 0,
            'det_efficency': 0,
            'flipping_ratio': 0,
            'substract_background_from_sample': 0,
            'background_factor': 0,
            'ignore_vana_fields': 0,
            'sum_vana_sf_nsf': 0,
            'separation': 0,
            'separation_xyz': 0,
            'separation_coh_inc': 0,
            'norm_monitor': 0
        }
        options.update(get_fake_elastic_sc_options())
        testv = self.model.script_maker(options, paths, fselector)
        self.assertFalse(self.model._vanac)
        self.assertFalse(self.model._nicrc)
        self.assertFalse(self.model._sampb)
        self.assertFalse(self.model._backfac)
        self.assertFalse(self.model._nonmag)
        self.assertFalse(self.model._xyz)
        self.assertFalse(self.model._corrections)
        self.assertFalse(self.model._ascii)
        self.assertFalse(self.model._nexus)
        self.assertEqual(self.model._ign_vana, '0')
        self.assertEqual(self.model._sum_sfnsf, '0')
        self.assertEqual(self.model._export_path, '')
        self.assertEqual(self.model._norm, 'time')
        lines = [55, 92, 70, 65, 49, 0, 20, 0, 0, 304, 0, 109, 51, 0]
        for i, tv in enumerate(testv):
            self.assertEqual(len(tv), lines[i])
        options = {
            'corrections': 1,
            'det_efficency': 0,
            'flipping_ratio': 0,
            'substract_background_from_sample': 0,
            'background_factor': 1,
            'ignore_vana_fields': 1,
            'sum_vana_sf_nsf': 1,
            'separation': 1,
            'separation_xyz': 0,
            'separation_coh_inc': 0,
            'norm_monitor': 1
        }
        options.update(get_fake_elastic_sc_options())
        fselector = {'full_data': [], 'standard_data': []}
        paths = {
            'data_dir': '12',
            'standards_dir': '13',
            'export_dir': '14',
            'ascii': False,
            'nexus': False,
            'export': True
        }
        testv = self.model.script_maker(options, paths, fselector)
        self.assertEqual(len(testv[0]), 55)
        self.assertFalse(self.model._vanac)
        self.assertFalse(self.model._nicrc)
        self.assertFalse(self.model._sampb)
        self.assertFalse(self.model._nonmag)
        self.assertFalse(self.model._xyz)
        self.assertFalse(self.model._corrections)
        self.assertFalse(self.model._ascii)
        self.assertFalse(self.model._nexus)
        lines = [55, 92, 70, 65, 49, 0, 20, 0, 0, 307, 0, 109, 51, 0]
        for i, tv in enumerate(testv):
            self.assertEqual(len(tv), lines[i])
        options = {
            'corrections': 0,
            'det_efficency': 1,
            'flipping_ratio': 1,
            'substract_background_from_sample': 1,
            'background_factor': 1,
            'ignore_vana_fields': 1,
            'sum_vana_sf_nsf': 1,
            'separation': 0,
            'separation_xyz': 1,
            'separation_coh_inc': 1,
            'norm_monitor': 1
        }
        options.update(get_fake_elastic_sc_options())
        fselector = {'full_data': [], 'standard_data': []}
        paths = {
            'data_dir': '12',
            'standards_dir': '13',
            'export_dir': '14',
            'ascii': True,
            'nexus': True,
            'export': False
        }
        testv = self.model.script_maker(options, paths, fselector)
        self.assertFalse(self.model._vanac)
        self.assertFalse(self.model._nicrc)
        self.assertFalse(self.model._sampb)
        self.assertFalse(self.model._nonmag)
        self.assertFalse(self.model._xyz)
        self.assertFalse(self.model._corrections)
        self.assertFalse(self.model._ascii)
        self.assertFalse(self.model._nexus)
        lines = [55, 92, 70, 65, 49, 0, 20, 0, 0, 307, 0, 109, 51, 0]
        for i, tv in enumerate(testv):
            self.assertEqual(len(tv), lines[i])
        paths = {
            'data_dir': '12',
            'standards_dir': '13',
            'export_dir': '',
            'ascii': True,
            'nexus': True,
            'export': True
        }
        testv = self.model.script_maker(options, paths, fselector)
        self.assertFalse(self.model._ascii)
        self.assertFalse(self.model._nexus)
        lines = [55, 92, 70, 65, 49, 0, 20, 0, 0, 307, 0, 109, 51, 0]
        for i, tv in enumerate(testv):
            self.assertEqual(len(tv), lines[i])

    @patch('DNSReduction.script_generator.elastic_sc_script_generator_model'
           '.DNSDataset')
    def test_setup_sample_data(self, mock_dns_dataset):
        self.model._sample_data = None
        mock_dns_dataset.return_value = self.sample_data
        self.model._setup_sample_data({'data_dir': '123'}, {'full_data': []})
        self.assertEqual(self.model._sample_data, self.sample_data)
        self.assertEqual(self.model._plotlist, ['knso_x_sf'])

    @patch('DNSReduction.script_generator.elastic_sc_script_generator_model'
           '.DNSDataset')
    def test_setup_standard_data(self, mock_dns_dataset):
        self.model._standard_data = None
        self.model._corrections = True

        mock_dns_dataset.return_value = self.standard_data
        self.model._setup_standard_data({'standards_dir': '123'},
                                        {'standard_data': []})
        self.assertEqual(self.model._standard_data, self.standard_data)

    def test_interpolate_standard(self):
        self.model._interpolate_standard()
        self.standard_data.interpolate_standard.assert_called_once()

    def test_set_loop(self):
        self.model._loop = None
        self.model._spac = None
        self.model._set_loop()
        self.assertEqual(
            self.model._loop,
            "for sample, workspacelist in wss_sample.items(): \n    for work"
            "space in workspacelist:")
        self.assertEqual(self.model._spac, "\n" + " " * 8)
        self.model._sample_data = {'123': 1}
        self.model._set_loop()
        self.assertEqual(self.model._loop,
                         "for workspace in wss_sample['123']:")
        self.assertEqual(self.model._spac, "\n" + " " * 4)
        self.model._sample_data = self.sample_data

    def test_get_header_lines(self):
        testv = self.model._get_header_lines()
        self.assertIsInstance(testv, list)
        self.assertEqual(len(testv), 6)
        self.assertEqual(
            testv[0], 'from mantidqtinterfaces.DNSReduction.scripts.md_sc_elastic import load_all'
        )
        self.assertEqual(
            testv[1], 'from mantidqtinterfaces.DNSReduction.scripts.md_sc_elastic import '
                      'vanadium_correction, fliping_ratio_correction')
        self.assertEqual(
            testv[2], 'from mantidqtinterfaces.DNSReduction.scripts.md_sc_elastic import'
                      ' background_substraction', )
        self.assertEqual(
            testv[3],
            "from mantid.simpleapi import ConvertMDHistoToMatrixWorkspace, mtd"
        )
        self.assertEqual(testv[4],
                         "from mantid.simpleapi import SaveAscii, SaveNexus")
        self.assertEqual(testv[5], "")

    def test_get_sample_data_lines(self):
        testv = self.model._get_sample_data_lines()
        self.assertEqual(testv, ['sample_data = 12345'])

    def test_get_standard_data_lines(self):
        self.model._corrections = True
        testv = self.model._get_standard_data_lines()
        self.assertEqual(testv, ['standard_data = 123456'])
        self.model._corrections = False
        testv = self.model._get_standard_data_lines()
        self.assertEqual(testv, [''])

    def test__get_param_lines(self):
        self.model._norm = 'time'
        testv = self.model._get_param_lines(get_fake_elastic_sc_options())
        self.assertIsInstance(testv, list)
        self.assertEqual(len(testv), 3)
        comparestring = ("params = {'a' : 2, \n          'b' : 3,\n          "
                         "'c' : 4,\n          'alpha' : 78,\n          'beta'"
                         "  : 86,\n          'gamma' : 85,\n          'hkl1' "
                         " : '1,2,3',\n          'hkl2'  : '2,3,4',\n        "
                         "  'omega_offset' : 0,\n          'norm_to' : "
                         "'time',\n          'dx' : ' 1.0000',\n        "
                         "  'dy' : ' 2.0000',}")
        self.assertEqual(testv[1], comparestring)

    def test__get_binning_lines(self):
        testv = self.model._get_binning_lines()
        testl = ["binning = {'twoTheta' : [1.000, 6.000, 5],\n       "
                 "    'Omega':  [3.000, 5.000, 3]} # min, max, number_of_bins"]
        self.assertEqual(testv, testl)

    def test_get_load_data_lines(self):
        self.model._corrections = True
        testv = self.model._get_load_data_lines()
        self.assertEqual(testv, ['wss_sample = load_all(sample_data, binning,'
                                 ' params)', 'wss_standard = load_all(standar'
                                             'd_data, binning, params, standar'
                                             'd=True,)', ''])
        self.model._corrections = False
        testv = self.model._get_load_data_lines()
        self.assertEqual(testv, [
            "wss_sample = load_all(sample_data, binning, params)", ''
        ])

    def test__get_bg_corr_lines(self):
        self.model._vanac = True
        testv = self.model._get_bg_corr_lines()
        self.assertEqual(testv, [
            '# substract background from vanadium and nicr',
            'for sample, workspacelist in wss_standard.items(): \n    '
            'for workspace in workspacelist:\n        background_substr'
            'action(workspace)', ''
        ])
        self.model._vanac = False
        self.model._nicrc = False
        testv = self.model._get_bg_corr_lines()
        self.assertEqual(testv, [])

    def test__return_sample_bg_string(self):
        self.model._spac = '  '
        self.model._backfac = '123'
        testv = self.model._return_sample_bg_string()
        self.assertEqual(testv, '  background_substraction(workspace,'
                                ' factor=123)')

    def test__return_sample_vanac_strinf(self):
        self.model._spac = '  '
        self.model._sum_sfnsf = 1
        self.model._ign_vana = 2
        testv = self.model._return_sample_vanac_strinf()
        self.assertEqual(testv, "  vanadium_correction(workspace,  vanaset=s"
                                "tandard_data['vana'], ignore_vana_fields=2,"
                                " sum_vana_sf_nsf=1)")

    def test__get_vanac_lines(self):
        self.model._backfac = '123'
        self.model._loop = 'fo:'
        self.model._spac = '  '
        self.model._sum_sfnsf = 1
        self.model._ign_vana = 2
        self.model._sampb = False
        self.model._vanac = False
        compare = ['# correct sample data',
                   "fo:  background_substraction(workspace, factor=123)  vanad"
                   "ium_correction(workspace,  vanaset=standard_data['vana'],"
                   " ignore_vana_fields=2, sum_vana_sf_nsf=1)"]

        testv = self.model._get_vanac_lines()
        self.assertEqual(testv, [])
        self.model._sampb = True
        testv = self.model._get_vanac_lines()
        self.assertEqual(testv, compare)
        self.model._sampb = False
        self.model._vanac = True
        testv = self.model._get_vanac_lines()
        self.assertEqual(testv, compare)

    def test__get_nicrc_lines(self):
        self.model._nicrc = False
        self.model._loop = 'fo:'
        self.model._spac = '  '
        testv = self.model._get_nicrc_lines()
        self.assertEqual(testv, [])
        self.model._nicrc = True
        testv = self.model._get_nicrc_lines()
        self.assertEqual(testv, ['fo:  fliping_ratio_correction(workspace)'])

    @patch(
        'DNSReduction.script_generator.elastic_sc_script_generator_model.mtd')
    def test_get_plotlist(self, mtd):
        mtd.__getitem__.return_value = self.fake_workspace
        self.model._plotlist = ['4p1K_map']
        testv = self.model.get_plotlist()
        self.assertEqual(
            testv, (['4p1K_map'],
                    {'4p1K_map': {'ttheta': [1, 2, 3],
                                  'omega': [4, 5, 6],
                                  'intensity': 4,
                                  'error': 1.0}}))


if __name__ == '__main__':
    unittest.main()
