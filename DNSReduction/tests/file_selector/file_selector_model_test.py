# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
presenter for dns path panel
"""

import os
import unittest
from unittest import mock
from unittest.mock import patch

from mantidqtinterfaces.DNSReduction.data_structures.dns_obs_model import DNSObsModel
from mantidqtinterfaces.DNSReduction.data_structures.dns_treemodel import DNSTreeModel
from mantidqtinterfaces.DNSReduction.data_structures.object_dict import ObjectDict
from mantidqtinterfaces.DNSReduction.file_selector.file_selector_model import \
    DNSFileSelectorModel
from mantidqtinterfaces.DNSReduction.tests.helpers_for_testing import get_filepath, dns_file


class DNSFileSelectorModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent = mock.Mock()
        cls.parent.update_progress = mock.Mock()
        cls.model = DNSFileSelectorModel(cls.parent)
        cls.filepath = get_filepath()

    def setUp(self):
        self.parent.update_progress.reset_mock()

    def get3files(self):
        # functions, so we do get an new object for every test
        return [
            'service_774714.d_dat', 'service_787463.d_dat',
            'service_788058.d_dat'
        ]

    def get2files(self):
        return ['service_787463.d_dat', 'service_788058.d_dat']

    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSFileSelectorModel._save_filelist')
    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSFile', new=dns_file)
    def read3files(self, mock_save):
        # this avoids reading files by patching dnsfile with a corresponding
        # dictionary, there are three different files supported
        self.model.datafiles = self.get3files()
        self.model.alldatafiles = self.get3files()
        self.model.datapath = self.filepath
        self.model.read_all(self.model.datafiles, self.model.datapath, {})
        mock_save.assert_called_once()

    def test___init__(self):
        self.assertIsInstance(self.model, DNSObsModel)
        self.assertIsInstance(self.model.treemodel, DNSTreeModel)
        self.assertIsInstance(self.model.standard_data, DNSTreeModel)
        self.assertTrue(hasattr(self.model, 'alldatafiles'))
        self.assertTrue(hasattr(self.model, 'old_data_set'))
        self.assertTrue(hasattr(self.model, 'active_model'))
        self.assertTrue(hasattr(self.model, 'loading_canceled'))

    def test_filter_out_already_loaded(self):
        self.model.old_data_set = [1]
        testv = self.model._filter_out_already_loaded([1, 2, 3], True)
        self.assertEqual(testv, [2, 3])
        self.model.old_data_set = [1]
        testv = self.model._filter_out_already_loaded([1, 2, 3], False)
        self.assertEqual(testv, [1, 2, 3])

    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSFileSelectorModel._get_list_of_loaded_files')
    @patch('DNSReduction.file_selector.file_selector_model.'
           'return_filelist')
    def test_set_datafiles_to_load(self, mock_return_filelist, mock_load):
        mock_load.return_value = [1, 2]
        mock_return_filelist.return_value = self.get3files()
        self.model.old_data_set = self.get3files()[0]
        testv = self.model.set_datafiles_to_load(datapath='a',
                                                 fn_range=[0, 1000000],
                                                 filtered=False,
                                                 watcher=True)
        self.assertEqual(testv, (2, [1, 2],
                                 ['service_787463.d_dat',
                                  'service_788058.d_dat'], [0, 1000000]))

    def test_get_start_end_filenumbers(self):
        self.model.alldatafiles = self.get2files()
        testv = self.model._get_start_end_filenumbers()
        self.assertEqual(testv, [787463, 788058])

    def test_filter_range(self):
        self.model.alldatafiles = self.get3files()
        testv = self.model._filter_range(self.get2files(),
                                         [0, 1],
                                         filtered=False)
        self.assertEqual(testv, (self.get2files(), [0, 1]))

        testv = self.model._filter_range(self.get2files(),
                                         [None, 1],
                                         filtered=True)
        self.assertEqual(testv, ([], [774714, 788058]))
        testv = self.model._filter_range(self.get3files(),
                                         filtered=True,
                                         fn_range=[787463, 787463])
        self.assertEqual(testv, ([self.get2files()[0]], [787463, 787463]))

    def test_read_all(self):
        self.read3files()
        self.assertFalse(self.model.loading_canceled)
        self.assertEqual(self.parent.update_progress.call_count, 3)
        self.assertEqual(len(self.model.old_data_set), 3)
        self.assertEqual(self.model.treemodel.rowCount(), 3)  # three scans

    @patch('DNSReduction.file_selector.file_selector_model.'
           'return_filelist')
    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSFile', new=dns_file)
    def test_read_standard(self, mock_return_filelist):
        mock_return_filelist.return_value = ['service_774714.d_dat']
        standardpath = self.filepath
        testv = self.model.read_standard(standardpath)
        self.parent.update_progress.assert_not_called()
        self.assertEqual(testv, 1)

    @patch('DNSReduction.file_selector.file_selector_model.'
           'unzip_latest_standard')
    def test_try_unzip(self, mock_unzip):
        testv = self.model.try_unzip('a', 'b')
        mock_unzip.assert_called_once_with('a', 'b')
        testv = self.model.try_unzip('a', '')
        self.assertFalse(testv)

    # def test_add_number_of_files_per_scan(self):
    #     pass # tested in treemodel

    def test_clear_scans_if_not_sequential(self):
        self.read3files()
        self.model._clear_scans_if_not_sequential(True)
        self.assertEqual(self.model.treemodel.rowCount(), 3)
        self.model._clear_scans_if_not_sequential(False)
        self.assertEqual(self.model.treemodel.rowCount(), 0)

    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSFileSelectorModel._load_saved_filelist')
    def test_get_list_of_loaded_files(self, mock_load):
        mock_load.return_value = 'x'
        testv = self.model._get_list_of_loaded_files('a', True)
        self.assertEqual(testv, {})
        testv = self.model._get_list_of_loaded_files('a', False)
        mock_load.assert_called_once_with('a')
        self.assertEqual(testv, 'x')

    @patch('DNSReduction.file_selector.file_selector_model.'
           'load_txt')
    def test_load_saved_filelist(self, mock_load):
        mock_load.return_value = [" ; 0"*14]
        testv = self.model._load_saved_filelist('123')
        mock_load.assert_called_once_with('last_filelist.txt', '123')
        self.assertIsInstance(testv['0'], ObjectDict)
        for name in ['filenumber', 'det_rot', 'sample_rot', 'field',
                     'temp_samp', 'sample', 'endtime', 'tofchannels',
                     'channelwidth', 'filename', 'wavelength',
                     'selector_speed', 'scannumber', 'scancommand',
                     'scanpoints', 'new_format']:
            self.assertTrue(hasattr(testv['0'], name))
        self.assertEqual(len(testv), 1)
        mock_load.side_effect = IOError
        testv = self.model._load_saved_filelist('123')
        self.assertEqual(testv, {})

    # def test_get_number_of_scans(self):
    # tested in the treemodel

    # def test_get_scan_range(self):
    # tested in the treemodel

    def test_check_last_scans(self):
        self.read3files()
        self.model.check_last_scans(1, False, [0, 1, 2])
        self.assertEqual(self.model.treemodel.get_checked(False), [788058])
        self.model.check_last_scans(1, True, [0, 1, 2])

    # def test_check_scans_by_indexes(self, indexes):
    # tested in treemodel

    # def test_check_scans_by_rows(self, rows):
    # tested in treemodel

    # def test_uncheck_all_scans(self):
    #  tested in treemodel

    def test_check_by_filenumbers(self):
        self.read3files()
        testv = self.model.check_by_filenumbers([4])
        self.assertEqual(testv, 1)
        testv = self.model.check_by_filenumbers([788058])
        self.assertEqual(testv, 0)

    # def test_check_fn_range(self, ffnmb, lfnmb):
    # tested in treemodel

    def test_set_loading_canceled(self):
        self.model.set_loading_canceled()
        self.assertTrue(self.model.loading_canceled)
        self.model.set_loading_canceled(False)
        self.assertFalse(self.model.loading_canceled)

    def test_get_model(self):
        treemodel = self.model.get_model()
        self.assertIsInstance(treemodel, DNSTreeModel)
        self.assertEqual(self.model.treemodel, treemodel)
        treemodel = self.model.get_model(standard=True)
        self.assertIsInstance(treemodel, DNSTreeModel)
        self.assertEqual(self.model.standard_data, treemodel)

    def test_model_is_standard(self):
        self.assertFalse(self.model.model_is_standard())
        self.model.active_model = self.model.standard_data
        self.assertTrue(self.model.model_is_standard())

    # def test_get_data(self):
    # tested in treemodel

    def test_set_model(self):
        self.model.active_model = ''
        self.assertFalse(self.model.model_is_standard())
        self.model.set_model(standard=True)
        self.assertTrue(self.model.model_is_standard())
        self.assertFalse(self.model.active_model == self.model.treemodel)
        self.model.set_model()
        self.assertTrue(self.model.active_model == self.model.treemodel)

    def test_filter_scans_for_boxes(self):
        self.read3files()
        filters = [('dummy', True)]
        testv = self.model.filter_scans_for_boxes(filters, is_tof=True)
        self.assertEqual(testv, {0, 1, 2})  # hidden scan rows
        filters = [('scan', True)]
        testv = self.model.filter_scans_for_boxes(filters, is_tof=True)
        self.assertEqual(testv, {0, 1})

    def test__filter_tof_scans(self):
        self.read3files()
        testv = self.model._filter_tof_scans(is_tof=True)
        self.assertEqual(testv, {0, 1})
        testv = self.model._filter_tof_scans(is_tof=False)
        self.assertEqual(testv, {2})

    def test_filter_standard_types(self):
        self.read3files()
        filters = {'vanadium': True, 'nicr': False, 'empty': False}
        testv = self.model.filter_standard_types(filters, True, False)
        self.assertEqual(testv, {1, 2})  # hidden scan rows
        filters = {'vanadium': False, 'nicr': True, 'empty': False}
        testv = self.model.filter_standard_types(filters, True, False)
        self.assertEqual(testv, {0, 1, 2})  # hidden scan rows

    @patch('DNSReduction.file_selector.file_selector_model.'
           'open_editor')
    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSTreeModel.get_filename_from_index')
    def test_open_datafile(self, mock_index, mock_open):
        self.model.active_model = self.model.standard_data
        mock_index.return_value = 'a'
        self.model.open_datafile(1, 'b', 'c')
        mock_open.assert_called_once_with('a', 'c')
        mock_open.reset_mock()
        self.model.active_model = self.model.treemodel
        self.model.open_datafile(1, 'b', 'c')
        mock_open.assert_called_once_with('a', 'b')

    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSFile')
    def test_load_file_from_chache_or_new(self, mock_dnsfile):
        filename = self.get2files()[0]
        datapath = self.filepath
        mydict = {filename : dns_file('a', filename)}
        testv = self.model._load_file_from_chache_or_new(mydict, filename, 'a')
        mock_dnsfile.assert_not_called()
        self.assertIsInstance(testv, ObjectDict)
        testv = self.model._load_file_from_chache_or_new({}, filename, 'a')
        mock_dnsfile.assert_called_once_with('a', filename)

    @patch('DNSReduction.file_selector.file_selector_model.'
           'DNSTreeModel.get_txt')
    @patch('DNSReduction.file_selector.file_selector_model.'
           'save_txt')
    def test_save_filelist(self, mock_save, mock_get_txt):
        mock_get_txt.return_value = 'c'
        mock_save.side_effect = PermissionError  # handled exception
        self.model._save_filelist('a')
        mock_get_txt.assert_called_once()
        mock_save.assert_called_once_with('c', 'last_filelist.txt', 'a')


if __name__ == '__main__':
    unittest.main()
