# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +

import unittest
from unittest import mock
from unittest.mock import patch

from mantidqtinterfaces.DNSReduction.data_structures.dns_dataset import DNSDataset
from mantidqtinterfaces.DNSReduction.data_structures.dns_obs_model import DNSObsModel
from mantidqtinterfaces.DNSReduction.script_generator.common_script_generator_model import \
    DNSScriptGeneratorModel
from mantidqtinterfaces.DNSReduction.script_generator.elastic_powder_script_generator_model\
    import DNSElasticPowderScriptGeneratorModel  # yapf: disable
from mantidqtinterfaces.DNSReduction.tests.helpers_for_testing import (get_fake_elastic_datadic,
                                                    get_elastic_standard_datadic)


class DNSElasticPowderScriptGeneratorModelTest(unittest.TestCase):
    # pylint: disable=protected-access, too-many-public-methods

    model = None
    parent = None
    sample_data = None
    standard_data = None

    @classmethod
    def setUpClass(cls):
        cls.parent = mock.Mock()
        cls.model = DNSElasticPowderScriptGeneratorModel(cls.parent)
        cls.model.raise_error = mock.Mock()
        cls.error_raised = cls.model.raise_error
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
        cls.sample_data.banks = [1, 2, 3]
        cls.sample_data.scriptname = '123.txt'
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
        cls.standard_data.scriptname = '123.txt'

    def setUp(self):
        self.error_raised.reset_mock()
        self.model._spac = "    "
        self.model._loop = "123"

    def test___init__(self):
        self.assertIsInstance(self.model,
                              DNSElasticPowderScriptGeneratorModel)
        self.assertIsInstance(self.model, DNSScriptGeneratorModel)
        self.assertIsInstance(self.model, DNSObsModel)

    def test_check_all_fields_there(self):
        testv = self.model._check_all_fields_there(
            ['x_sf', 'y_sf', 'z_sf', 'z_nsf', 'g_nsf'])
        self.assertTrue(testv)
        testv = self.model._check_all_fields_there(['x_sf', 'y_sf', 'z_sf'])
        self.assertFalse(testv)
        self.error_raised.assert_called_once()

    def test_get_xyz_field_string(self):
        testv = self.model._get_xyz_field_string('a1')
        self.assertEqual(testv, [
            "# do xyz polarization analysis for magnetic powders \na1_nuclear"
            "_coh, a1_magnetic, a1_spin_incoh= xyz_seperation(\n    x_sf='a1_"
            "x_sf', y_sf='a1_y_sf', z_sf='a1_z_sf', z_nsf='a1_z_nsf')"
        ])

    def test_get_to_matrix_string(self):
        testv = self.model._get_to_matrix_string('a1', 'vana')
        self.assertEqual(
            testv,
            "ConvertMDHistoToMatrixWorkspace('a1_vana', Outputworkspace='mat_"
            "a1_vana', Normalization='NoNormalization')")

    def test_get_sep_save_string(self):
        self.model._ascii = True
        self.model._nexus = True
        self.model._export_path = '1234/'
        testv = self.model._get_sep_save_string('a1', 'vana')
        self.assertEqual(
            testv,
            "SaveAscii('mat_a1_vana', '1234//a1_vana.csv', WriteSpectrumID"
            "=False)\nSaveNexus('mat_a1_vana', '1234//a1_vana.nxs')")
        self.model._ascii = False
        self.model._nexus = False
        testv = self.model._get_sep_save_string('a1', 'vana')
        self.assertEqual(testv, "")

    def test_get_xyz_lines(self):
        self.model._ascii = True
        self.model._nexus = True
        self.model._xyz = False
        testv = self.model._get_xyz_lines()
        self.assertEqual(testv, [])
        self.model._xyz = True
        testv = self.model._get_xyz_lines()
        self.assertIsInstance(testv, list)
        self.assertEqual(len(testv), 7)
        self.assertEqual(
            testv[0],
            "# do xyz polarization analysis for magnetic powders \nknso_nuc"
            "lear_coh, knso_magnetic, knso_spin_incoh= xyz_seperation(\n   "
            " x_sf='knso_x_sf', y_sf='knso_y_sf', z_sf='knso_z_sf', z_nsf='"
            "knso_z_nsf')")
        self.assertEqual(
            testv[1],
            "ConvertMDHistoToMatrixWorkspace('knso_nuclear_coh', Outputworks"
            "pace='mat_knso_nuclear_coh', Normalization='NoNormalization')")
        self.assertEqual(
            testv[2],
            "SaveAscii('mat_knso_nuclear_coh', '1234//knso_nuclear_coh.csv',"
            " WriteSpectrumID=False)\nSaveNexus('mat_knso_nuclear_coh', '123"
            "4//knso_nuclear_coh.nxs')")
        self.assertEqual(
            testv[3],
            "ConvertMDHistoToMatrixWorkspace('knso_magnetic', Outputworkspac"
            "e='mat_knso_magnetic', Normalization='NoNormalization')")
        self.assertEqual(
            testv[4], "SaveAscii('mat_knso_magnetic', '1234//kns"
                      "o_magnetic.csv', Wr"
                      "iteSpectrumID=False)\nSaveNexus('mat_knso_magnetic'"
                      ", '1234//knso_magnetic.nxs')")
        self.assertEqual(
            testv[5],
            "ConvertMDHistoToMatrixWorkspace('knso_spin_incoh', Outputworks"
            "pace='mat_knso_spin_incoh', Normalization='NoNormalization')")
        self.assertEqual(
            testv[6],
            "SaveAscii('mat_knso_spin_incoh', '1234//knso_spin_incoh.csv', "
            "WriteSpectrumID=False)\nSaveNexus('mat_knso_spin_incoh', '1234//"
            "knso_spin_incoh.nxs')")

    def test_get_nsf_sf_pairs(self):
        self.model._ascii = True
        self.model._nexus = True
        testv = self.model._get_nsf_sf_pairs()
        self.assertEqual(testv, ['knso_x', 'knso_y', 'knso_z'])

    def test_get_nonmag_lines(self):
        self.model._ascii = False
        self.model._nexus = False
        self.model._nonmag = False
        testv = self.model._get_nonmag_lines()
        self.assertEqual(testv, [])
        self.model._nonmag = True
        testv = self.model._get_nonmag_lines()
        self.assertIsInstance(testv, list)
        self.assertEqual(len(testv), 16)
        self.assertEqual(
            testv[0],
            "# sepearation of coherent and incoherent scattering of non"
            " magnetic sample")
        self.assertEqual(
            testv[1],
            "knso_x_nuclear_coh, knso_x_spin_incoh = non_mag_sep('knso_x_sf',"
            " 'knso_x_nsf')")
        self.assertEqual(
            testv[2],
            "ConvertMDHistoToMatrixWorkspace('knso_x_nuclear_coh', Outputwork"
            "space='mat_knso_x_nuclear_coh', Normalization='NoNormalization')")
        self.assertEqual(testv[3], '')
        self.assertEqual(
            testv[4],
            "ConvertMDHistoToMatrixWorkspace('knso_x_spin_incoh', Outputwork"
            "space='mat_knso_x_spin_incoh', Normalization='NoNormalization')")
        self.assertEqual(testv[5], '')
        self.assertEqual(
            testv[6],
            "knso_y_nuclear_coh, knso_y_spin_incoh = non_mag_sep('knso_y_sf'"
            ", 'knso_y_nsf')")
        self.assertEqual(
            testv[7],
            "ConvertMDHistoToMatrixWorkspace('knso_y_nuclear_coh', Outputw"
            "orkspace='mat_knso_y_nuclear_coh', Normalization='NoNormaliza"
            "tion')")
        self.assertEqual(testv[8], '')
        self.assertEqual(
            testv[9],
            "ConvertMDHistoToMatrixWorkspace('knso_y_spin_incoh', Outputwo"
            "rkspace='mat_knso_y_spin_incoh', Normalization='NoNormalizatio"
            "n')")
        self.assertEqual(testv[10], '')
        self.assertEqual(
            testv[11],
            "knso_z_nuclear_coh, knso_z_spin_incoh = non_mag_sep('knso_z_sf',"
            " 'knso_z_nsf')")
        self.assertEqual(
            testv[12],
            "ConvertMDHistoToMatrixWorkspace('knso_z_nuclear_coh', Outputwor"
            "kspace='mat_knso_z_nuclear_coh', Normalization='NoNormalizati"
            "on')")
        self.assertEqual(testv[13], '')
        self.assertEqual(
            testv[14],
            "ConvertMDHistoToMatrixWorkspace('knso_z_spin_incoh', Outputwor"
            "kspace='mat_knso_z_spin_incoh', Normalization='NoNormalizatio"
            "n')")
        self.assertEqual(testv[15], '')

    @patch('DNSReduction.script_generator.elastic_powder_script_generator_mod'
           'el.DNSDataset')
    def test_setup_sample_data(self, mock_dns_dataset):
        self.model._sample_data = None
        mock_dns_dataset.return_value = self.sample_data
        self.model._setup_sample_data({'data_dir': '123'}, {'full_data': []})
        self.assertEqual(self.model._sample_data, self.sample_data)
        self.assertEqual(self.model._plotlist, ['mat_knso_x_sf'])

    @patch('DNSReduction.script_generator.elastic_powder_script_generator_mod'
           'el.DNSDataset')
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

    def test_get_header_lines(self):
        testv = self.model._get_header_lines()
        self.assertIsInstance(testv, list)
        self.assertEqual(len(testv), 6)
        self.assertEqual(
            testv[0], "from mantidqtinterfaces.DNSReduction.scripts.md_powder_elastic import "
                      "load_all, background_substraction")
        self.assertEqual(
            testv[1], "from mantidqtinterfaces.DNSReduction.scripts.md_powder_elastic import "
                      "vanadium_correction, fliping_ratio_correction")
        self.assertEqual(
            testv[2], "from mantidqtinterfaces.DNSReduction.scripts.md_powder_elastic import "
                      "non_mag_sep, xyz_seperation")
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

    def test_get_binning_lines(self):
        testv = self.model._get_binning_lines()
        self.assertEqual(testv, ['', 'binning = [1, 6, 5]'])

    def test_get_load_data_lines(self):
        self.model._corrections = True
        self.model._norm = 'time'
        testv = self.model._get_load_data_lines()
        self.assertEqual(testv, [
            "wss_sample = load_all(sample_data, binning, normalizeto='time')",
            "wss_standard = load_all(standard_data, binning, normalizeto='"
            "time')"
        ])
        self.model._corrections = False
        testv = self.model._get_load_data_lines()
        self.assertEqual(testv, [
            "wss_sample = load_all(sample_data, binning, normalizeto='time')"
        ])

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

    def test_get_substract_bg_from_standa_lines(self):
        self.model._vanac = True
        testv = self.model._get_substract_bg_from_standa_lines()
        self.assertEqual(testv, [
            '', '# substract background from vanadium and nicr',
            'for sample, workspacelist in wss_standard.items(): \n    '
            'for workspace in workspacelist:\n        background_substr'
            'action(workspace)'
        ])
        self.model._vanac = False
        self.model._nicrc = False
        testv = self.model._get_substract_bg_from_standa_lines()
        self.assertEqual(testv, [])

    def test_get_backgroundstring(self):
        self.model._backfac = '1'
        self.model._sampb = False
        testv = self.model._get_backgroundstring()
        self.assertEqual(testv, "")
        self.model._sampb = True
        testv = self.model._get_backgroundstring()
        self.assertEqual(testv,
                         '    background_substraction(workspace, factor=1)')

    def test_get_vanacstring(self):
        self.model._ign_vana = 'True'
        self.model._sum_sfnsf = 'True'
        self.model._vanac = False
        testv = self.model._get_vanacstring()
        self.assertEqual(testv, "")
        self.model._vanac = True
        testv = self.model._get_vanacstring()
        self.assertEqual(
            testv,
            "    vanadium_correction(workspace, vanaset=sta"
            "ndard_data['vana'], ignore_vana_fields=True, sum_vana_sf_nsf=Tr"
            "ue)")

    def test_get_samp_corrections_lines(self):
        self.model._ign_vana = 'True'
        self.model._sum_sfnsf = 'True'
        self.model._backfac = '1'
        self.model._vanac = False
        self.model._sampb = False
        testv = self.model._get_samp_corrections_lines()
        self.assertEqual(testv, [])
        self.model._sampb = True
        testv = self.model._get_samp_corrections_lines()
        self.assertEqual(testv, [
            '', '# correct sample data', '123    background_substraction'
                                         '(workspace, factor=1)'
        ])

    def test_get_nicr_cor_lines(self):
        self.model._nicrc = False
        testv = self.model._get_nicr_cor_lines()
        self.assertEqual(testv, [])
        self.model._nicrc = True
        testv = self.model._get_nicr_cor_lines()
        self.assertEqual(testv, ["123    fliping_ratio_correction(workspace)"])

    def test_get_ascii_save_string(self):
        self.model._ascii = False
        self.model._export_path = "123"
        testv = self.model._get_ascii_save_string()
        self.assertEqual(testv, '')
        self.model._ascii = True
        testv = self.model._get_ascii_save_string()
        self.assertEqual(
            testv,
            "    SaveAscii('mat_{}'.format(workspace), '123/{}.csv'.format(wo"
            "rkspace), WriteSpectrumID=False)")

    def test_get_nexus_save_string(self):
        self.model._nexus = False
        self.model._export_path = "123"
        testv = self.model._get_nexus_save_string()
        self.assertEqual(testv, '')
        self.model._nexus = True
        testv = self.model._get_nexus_save_string()
        self.assertEqual(
            testv,
            "    SaveNexus('mat_{}'.format(workspace), '123/{}.nxs'.format(wo"
            "rkspace))")

    def test_get_convert_to_matrix_lines(self):
        testv = self.model._get_convert_to_matrix_lines('abc')
        self.assertEqual(testv, [
            "123    ConvertMDHistoToMatrixWorkspace(wor"
            "kspace, Outputworkspace='mat_{}'.format(workspace), Normalizati"
            "on='NoNormalization')abc", ''
        ])

    def test__get_save_string(self):
        self.model._ascii = True
        self.model._nexus = True
        self.model._export_path = "123"
        testv = self.model._get_save_string()
        self.assertEqual(
            testv,
            "    SaveAscii('mat_{}'.format(workspace), '123/{}.csv'.format"
            "(workspace), WriteSpectrumID=False)    SaveNexus('mat_{}'.for"
            "mat(workspace), '123/{}.nxs'.format(workspace))")

    @patch('DNSReduction.script_generator.elastic_powder_script_generator_mod'
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
        self.assertEqual(len(testv), 57)
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
        paths = {
            'data_dir': '',
            'standards_dir': '',
            'export_dir': '',
            'ascii': False,
            'nexus': False,
            'export': False
        }
        testv = self.model.script_maker(options, paths, fselector)
        self.assertIsInstance(testv, list)
        self.assertEqual(len(testv), 13)
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
        self.model.script_maker(options, paths, fselector)
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
        self.assertEqual(len(testv), 13)
        self.assertFalse(self.model._vanac)
        self.assertFalse(self.model._nicrc)
        self.assertFalse(self.model._sampb)
        self.assertFalse(self.model._nonmag)
        self.assertFalse(self.model._xyz)
        self.assertFalse(self.model._corrections)
        self.assertFalse(self.model._ascii)
        self.assertFalse(self.model._nexus)
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
        fselector = {'full_data': [], 'standard_data': []}
        paths = {
            'data_dir': '12',
            'standards_dir': '13',
            'export_dir': '14',
            'ascii': True,
            'nexus': True,
            'export': False
        }
        self.model.script_maker(options, paths, fselector)
        self.assertFalse(self.model._vanac)
        self.assertFalse(self.model._nicrc)
        self.assertFalse(self.model._sampb)
        self.assertFalse(self.model._nonmag)
        self.assertFalse(self.model._xyz)
        self.assertFalse(self.model._corrections)
        self.assertFalse(self.model._ascii)
        self.assertFalse(self.model._nexus)
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
        self.assertEqual(len(testv), 13)

    def test_get_plotlist(self):
        self.model._plotlist = ['123']
        testv = self.model.get_plotlist()
        self.assertEqual(testv, ['123'])


if __name__ == '__main__':
    unittest.main()
