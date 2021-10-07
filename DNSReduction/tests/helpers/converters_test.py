# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +

import unittest

from mantidqtinterfaces.DNSReduction.helpers.converters import (
    convert_hkl_string, convert_hkl_string_to_float, d_spacing_from_lattice,
    el_twotheta_to_d, el_twotheta_to_q, lambda_to_energy, twotheta_to_q,
    speed_to_energy)


class DNSconvertersTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_lambda_to_E(self):
        energy = lambda_to_energy(4.74)
        self.assertAlmostEqual(energy, 3.64098566)
        with self.assertRaises(ZeroDivisionError):
            lambda_to_energy(0)

    def test_el_twotheta_to_d(self):
        self.assertAlmostEqual(el_twotheta_to_d(1, 2), 114.59301348013031)

    def test_el_twotheta_to_q(self):
        self.assertAlmostEqual(el_twotheta_to_q(1, 2), 0.05483043962596419)

    def test_twotheta_to_q(self):
        qabs = twotheta_to_q(120, 4.74, 0)
        self.assertAlmostEqual(qabs, 2.29594856)
        qabs = twotheta_to_q(120, 4.74, 3)
        self.assertAlmostEqual(qabs, 1.67443094)
        with self.assertRaises(ZeroDivisionError):
            twotheta_to_q(120, 0, 0)

    def test_speed_to_E(self):
        self.assertAlmostEqual(speed_to_energy(834), 3.635697328)
        self.assertEqual(speed_to_energy(0), 0)

    def test_d_spacing_from_lattice(self):
        testv = d_spacing_from_lattice(2, 3, 4, 78, 86, 85, [1, 2, 3])
        self.assertAlmostEqual(testv, 0.9979628311312633)

    def test_convert_hkl_string(self):
        testv = convert_hkl_string('[1 2 3]')
        self.assertEqual(testv, '1,2,3')
        testv = convert_hkl_string('(1,2,3)')
        self.assertEqual(testv, '1,2,3')

    def test_convert_hkl_string_to_float(self):
        testv = convert_hkl_string_to_float('[1 2 3]')
        self.assertIsInstance(testv[0], float)
        self.assertEqual(testv, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
