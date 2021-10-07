# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Options Presenter - Tab of DNS Reduction GUI
"""

from mantidqtinterfaces.DNSReduction.helpers.converters import (convert_hkl_string_to_float,
                                             d_spacing_from_lattice)
from mantidqtinterfaces.DNSReduction.options.common_options_model import DNSCommonOptionsModel


class DNSElasticSCOptionsModel(DNSCommonOptionsModel):

    @staticmethod
    def get_dx_dy(options):
        hkl1 = convert_hkl_string_to_float(options['hkl1'])
        hkl2 = convert_hkl_string_to_float(options['hkl2'])
        dx = d_spacing_from_lattice(a=options['a'],
                                    b=options['b'],
                                    c=options['c'],
                                    alpha=options['alpha'],
                                    beta=options['beta'],
                                    gamma=options['gamma'],
                                    hkl=hkl1)
        dy = d_spacing_from_lattice(a=options['a'],
                                    b=options['b'],
                                    c=options['c'],
                                    alpha=options['alpha'],
                                    beta=options['beta'],
                                    gamma=options['gamma'],
                                    hkl=hkl2)
        return [dx, dy]

    @staticmethod
    def convert_hkl_string(hkl):
        # catches if user uses brackets or spaces in hkl specification
        hkl = hkl.strip("[]()")
        hkl = hkl.replace(' ', ',')
        return hkl
