# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,

#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
creates mapping of Qt elements in ui file
"""

from qtpy.QtWidgets import (QCheckBox, QDoubleSpinBox, QGroupBox, QLineEdit,
                            QRadioButton, QSpinBox)


class MappingCreator:
    def __init__(self, ui):
        mapping = '        self._map = ' + str(
            self.get_mapping(search=ui, mapping={}))
        mapping = mapping.replace("', u'", ",\n                       '")
        mapping = mapping.replace(": u'", ": self._content.")
        mapping = mapping.replace("{u'", "{'")
        mapping = mapping.replace("'}", "\n                       }")
        print(mapping)

    def get_mapping(self, search, mapping):
        for child in search.children():
            if child.children() and not isinstance(
                    child, QDoubleSpinBox) and not isinstance(child, QSpinBox):
                self.get_mapping(child, mapping=mapping)
            name = child.objectName()
            try:
                shortname = name.split('_', 1)[1]
            except IndexError:
                shortname = name
            state = self.get_single_state(child)
            if name and state is not None:
                mapping[shortname] = name
        return mapping

    @staticmethod
    def get_single_state(target_object):
        # pylint: disable=too-many-return-statements
        """
        defines for which Widgets status should be returned and how
        """
        if isinstance(target_object, QDoubleSpinBox):
            return target_object.value()
        if isinstance(target_object, QSpinBox):
            return target_object.value()
        if isinstance(target_object, QLineEdit):
            return target_object.text()
        if isinstance(target_object, QCheckBox):
            return target_object.isChecked()
        if isinstance(target_object, QRadioButton):
            return target_object.isChecked
        if isinstance(target_object, QGroupBox):
            if target_object.isCheckable():
                return target_object.isChecked
        return None

    @staticmethod
    def set_single_state(target_object, value):
        """
        defines for which Widgets status should be set and how
        """
        if isinstance(target_object, QDoubleSpinBox):
            target_object.setValue(float(value))
        elif isinstance(target_object, QSpinBox):
            target_object.setValue(int(value))
        elif isinstance(target_object, QLineEdit):
            target_object.setText(str(value))
        elif isinstance(target_object, QCheckBox):
            target_object.setChecked(value)
        elif isinstance(target_object, QRadioButton):
            target_object.setChecked(value)
        elif isinstance(target_object, QGroupBox):
            if target_object.isCheckable():
                target_object.setChecked(value)
