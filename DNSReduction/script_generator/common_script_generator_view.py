# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Path Configuration Widget = View - Tab of DNS Reduction GUI
"""
from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QProgressDialog
from qtpy.QtCore import Signal, Qt

from DNSReduction.data_structures.dns_view import DNSView

try:
    from mantidqt.utils.qt import load_ui
except ImportError:
    from mantidplot import load_ui
#from DNSReduction.helpers.mapping_creator import mapping_creator


class DNSScriptGenerator_view(DNSView):
    """
        Widget that lets user select DNS data directories
    """
    def __init__(self, parent):
        super(DNSScriptGenerator_view, self).__init__(parent)
        self.name = "Script generator"
        self._content = load_ui(__file__, 'script_generator.ui', baseinstance=self)
        self._mapping = {'script_filename' : self._content.lE_filename,
                         'generate_script' :  self._content.pB_generate_script,
                         'copy_script' : self._content.pB_copy_to_clipboard,
                         'script_output' : self._content.tE_script_output,
                        }
        self._mapping['generate_script'].clicked.connect(self.generate_script)
        self._mapping['copy_script'].clicked.connect(self.copy_to_clip)
        self.progress = None

    def set_filename(self, filename='script.py'):
        self._mapping['script_filename'].setText(filename)

    sig_generate_script = Signal()
    sig_progress_canceled = Signal()

    def generate_script(self):
        self.sig_generate_script.emit()

    def set_script_output(self, scripttext):
        self._mapping['script_output'].setPlainText(scripttext)

    def copy_to_clip(self):
        self._mapping['script_output'].selectAll()
        self._mapping['script_output'].copy()
        text_cursor = self._mapping['script_output'].textCursor()
        text_cursor.clearSelection()
        self._mapping['script_output'].setTextCursor(text_cursor)


    def open_progress_dialog(self, numberofsteps):
        self.progress = QProgressDialog("Script running please wait", "Abort Loading", 0, numberofsteps)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setMinimumDuration(200)
        self.progress.open(self.progress_canceled)

    def set_progress(self, step):
        self.progress.setValue(step)

    def progress_canceled(self):
        self.sig_progress_canceled.emit()
