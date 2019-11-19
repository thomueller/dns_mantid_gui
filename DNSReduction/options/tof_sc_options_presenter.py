# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2019 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Options Presenter - Tab of DNS Reduction GUI
"""
from __future__ import (absolute_import, division, print_function)
from numpy import cos, radians, pi
from DNSReduction.data_structures.dns_observer import DNSObserver
from DNSReduction.options.tof_sc_options_view import DNSTofScOptions_view

def twotheta_to_q(twotheta, wavelength, deltaE):
    #deltaE in meV
    #wavelength in Angstroem
    #twotheta is not 2*theta here!
    deltaE = deltaE*1.6021766208*10**-22 # converts meV to Joule
    hquer = 6.626070040*10**-34/pi/2 ### in J*s
    mneutron = 1.674927471*10**-27 ## in kg
    twotheta = radians(twotheta)
    ki = pi*2/wavelength # incoming wavevector
    #outgoing wavevector # = ki for elastic  ## factor 10**-20 is for converting 1/m^2 to 1/Angstroem^2
    kf = (ki**2-deltaE*2*mneutron/hquer**2*10**-20)**0.5
    qabs = 2*pi*(ki**2+kf**2-2*ki*kf*cos(twotheta))**0.5 / 2.0 / pi # length of Q in inelastic case
    return qabs

def v_to_E(velocity):
    mneutron = 1.674927471*10**-27 ## in kg
    E = mneutron/2.0 * velocity**2 / 1.6021766208 / 10**-22  ## in meV
    return E

def lambda_to_E(wavelength):
    mneutron = 1.674927471*10**-27 ## in kg
    hquer = 6.626070040*10**-34 ### in J*s
    E = hquer**2 / 2 / mneutron / wavelength**2 * 10**20 /1.6021766208 / 10**-22
    return E


class DNSTofScOptions_presenter(DNSObserver):

    def __init__(self, parent):
        super(DNSTofScOptions_presenter, self).__init__(parent, 'options')
        self.name = 'tof_sc_options'
        self.view = DNSTofScOptions_view(self.parent.view)
        self.view.sig_get_wavelength.connect(self.get_wavelength)
        #self.view.sig_estimate_q_and_binning.connect(self.estimate_q_and_binning)

    def get_wavelength(self):
        fulldata = self.param_dict['file_selector']['full_data']
        if not fulldata:
            self.raise_error('no data selected', critical=True)
            return None
        wavelengths = [x['wavelength'] for x in fulldata]
        if len(set(wavelengths)) > 1:
            self.raise_error('Warning, different wavelengths in datafiles')
        else:
            own_options = self.get_option_dict()
            own_options['wavelength'] = wavelengths[0]
            self.set_view_from_param()
        return wavelengths[0]


    def process_request(self):
        self.get_option_dict()
