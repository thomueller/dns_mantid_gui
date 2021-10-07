# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS unit convertes
"""

from numpy import cos, deg2rad, pi, radians, sin, sqrt


def lambda_to_energy(wavelength):
    mneutron = 1.674927471 * 10 ** -27  # in kg
    hquer = 6.626070040 * 10 ** -34  # in J*s
    energy = (
        hquer ** 2 / 2 / mneutron / wavelength ** 2 * 10 ** 20 /
        1.6021766208 / 10 ** -22)
    return energy


def el_twotheta_to_d(twotheta, wavelength):
    return wavelength / (2 * sin(deg2rad(twotheta / 2.0)))


def el_twotheta_to_q(twotheta, wavelength):
    return pi * 4 * sin(deg2rad(twotheta / 2.0)) / wavelength


def twotheta_to_q(twotheta, wavelength, delta_e):
    # deltaE in meV
    # wavelength in Angstroem
    # twotheta is not 2*theta here!
    delta_e = delta_e * 1.6021766208 * 10 ** -22  # converts meV to Joule
    hquer = 6.626070040 * 10 ** -34 / pi / 2  # in J*s
    mneutron = 1.674927471 * 10 ** -27  # in kg
    twotheta = radians(twotheta)
    ki = pi * 2 / wavelength  # incoming wavevector
    # outgoing wavevector # = ki for elastic
    # factor 10**-20 is for converting 1/m^2 to 1/Angstroem^2
    kf = (ki ** 2 - delta_e * 2 * mneutron / hquer ** 2 * 10 ** -20) ** 0.5
    qabs = 2 * pi * (ki ** 2 +
                     kf ** 2 -
                     2 * ki * kf * cos(twotheta)
                     ) ** 0.5 / 2.0 / pi  # length of Q in inelastic case
    return qabs


def speed_to_energy(velocity):
    mneutron = 1.674927471 * 10 ** -27  # in kg
    energy = mneutron / 2.0 * velocity ** 2 / 1.6021766208 / 10 ** -22
    # in meV
    return energy


def d_spacing_from_lattice(a, b, c, alpha, beta, gamma, hkl):
    # pylint: disable=too-many-arguments
    # alpha beta gamma in deg
    h, k, l = hkl  # noqa: E741
    alpha = radians(alpha)
    beta = radians(beta)
    gamma = radians(gamma)
    calpha = cos(alpha)
    cbeta = cos(beta)
    cgamma = cos(gamma)
    salpha = sin(alpha)
    sbeta = sin(beta)
    sgamma = sin(gamma)
    vol = a * b * c * sqrt(1 - calpha ** 2 -
                           cbeta ** 2 -
                           cgamma ** 2 +
                           2 * calpha * cbeta * cgamma)
    s11 = b ** 2 * c ** 2 * salpha ** 2
    s22 = a ** 2 * c ** 2 * sbeta ** 2
    s33 = a ** 2 * b ** 2 * sgamma ** 2
    s12 = a * b * c ** 2 * (calpha * cbeta - cgamma)
    s23 = a ** 2 * b * c * (cbeta * cgamma - calpha)
    s13 = a * b ** 2 * c * (cgamma * calpha - cbeta)
    invd2 = 1 / vol ** 2 * (s11 * h ** 2 +
                            s22 * k ** 2 +
                            s33 * l ** 2 +
                            2 * s12 * h * k +
                            2 * s23 * k * l +
                            2 * s13 * h * l)
    d = sqrt(1 / invd2)
    return d


def convert_hkl_string(hkl):
    # catches if user uses brackets or spaces in hkl specification
    hkl = hkl.strip("[]()")
    hkl = hkl.replace(' ', ',')
    return hkl


def convert_hkl_string_to_float(hkl):
    return [float(x) for x in convert_hkl_string(hkl).split(',')]
