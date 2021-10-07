# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
import unittest
from unittest import mock

from mantidqt.gui_helper import get_qapplication

from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import DNSWidget
from mantidqtinterfaces.DNSReduction.script_generator.common_script_generator_view import \
    DNSScriptGeneratorView
from mantidqtinterfaces.DNSReduction.script_generator.tof_sc_script_generator_presenter import \
    DNSTofScScriptGeneratorPresenter
from mantidqtinterfaces.DNSReduction.script_generator.tof_sc_script_generator_widget import \
    DNSTofScScriptGeneratorWidget

app, within_mantid = get_qapplication()


class DNSTofScScriptGenerator_widgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = mock.Mock()
        parent.view = None
        cls.widget = DNSTofScScriptGeneratorWidget('elastic_powder_options',
                                                   parent)

    def test___init__(self):
        self.assertIsInstance(self.widget, DNSTofScScriptGeneratorWidget)
        self.assertIsInstance(self.widget, DNSWidget)
        self.assertIsInstance(self.widget.view, DNSScriptGeneratorView)
        self.assertIsInstance(self.widget.presenter,
                              DNSTofScScriptGeneratorPresenter)


if __name__ == '__main__':
    unittest.main()
