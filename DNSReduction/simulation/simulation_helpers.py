# -*- coding: utf-8 -*-
"""
Created on Fri May  3 22:06:18 2019

@author: thomasm
"""
from __future__ import (absolute_import, division, print_function)
import numpy as np
from numpy import cos, sin, arcsin, arccos, radians, pi, rad2deg

from mantid.kernel import V3D


def hkl_string_to_float_list(hkl):
    """hkl can contain brackets and spaces or commas as seperators """
    hkl = hkl.strip("[]()")
    hkl = hkl.replace(' ', ',')
    hkl = [float(x) for x in hkl.split(',')]
    return hkl

def angToHKL(twotheta, omega, UBinv, wavelength):
    """calculates hkl for diffractometer angles and given inverse UB """
    theta = radians(twotheta / 2.0)
    omega = radians(omega) - theta
    uphi = np.array([-cos(omega), 0, -sin(omega)])
    hphi = 2 * sin(theta) / wavelength * uphi
    hkl = np.dot(UBinv, hphi)
    return hkl

def max_q(wavelength):
    """ returns maximum q at DNS for PA detector """
    maxq = 2 * sin(radians(135.5 / 2.0)) / wavelength
    return maxq

def det_rot_nmb_to_tth(det_rot, det_number):
    return  -det_rot + det_number * 5

def q_to_tth(q, wavelength):
    return rad2deg(2*arcsin(q * wavelength/ (4*pi)))

def tth_to_rot_nmb(tth):
    det_rot = -5 - tth % 5
    channel = tth // 5 - 1
    return [det_rot, channel]

def lorentz_correction(intensity, tth):
    return intensity / sin(radians(tth))

def check_inplane(q1, q2, hkl):
    q1q2 = np.column_stack((q1, q2))
    return np.linalg.det(np.column_stack((q1q2, hkl))) == 0

def hkl_to_omega(hkl, UB, wavelength, tth):
    hphi = np.transpose(np.dot(hkl, np.transpose(UB)))
    uphi = hphi * wavelength/2.0 /sin(radians(tth/2.0))
    sign = np.sign(arcsin(float(uphi[2])))
    omega = -sign*rad2deg(arccos((round(float(uphi[0]), 10)))) + tth/2.0
    ### rounding necesarry to prevent floats slightly larger 1 which will kill arccos
    return omega

def omega_to_samp_rot(omega, det_rot):
    return omega + det_rot

def rotate_UB(omegaoffset, UB):
    w1 = radians(omegaoffset)
    R = np.matrix([[cos(w1), 0, -sin(w1)],
                   [0, 1, 0],
                   [sin(w1), 0, cos(w1)]])
    UB = np.dot(R, UB)
    return UB

def shift_channels_below_23(channel, det_rot):
    # shifting detector_rot to higher angles
    # if reflection is not on last detector
    while channel > 23:
        channel += -1
        det_rot += -5
    return [channel, det_rot]

def ki_from_wavelength(wavelength):
    """sets ki for given wavelength"""
    return 2 * pi / wavelength

def return_qx_qx_inplane_refl(orilat, q1, q2, refls):
    """ returns a qx,qx,Intensity,h,k,l list for reflections in plane """
    reflections = []
    for refl in  refls:
        if refl.inplane:
            qx, qy = return_qxqy(orilat, q1, q2, refl.hkl)
            intensity = refl.fs_lc
            reflections.append([qx, qy, intensity, refl.h, refl.k, refl.l])
    reflections = np.asarray(reflections)
    return reflections

def return_qxqy(orilat, q1, q2, hkl):
    angle_q1_hkl = radians(orilat.recAngle(hkl[0], hkl[1], hkl[2], q1[0], q1[1], q1[2]))
    angle_q2_hkl = radians(orilat.recAngle(hkl[0], hkl[1], hkl[2], q2[0], q2[1], q2[2]))
    n_q1 = np.linalg.norm(orilat.qFromHKL(q1))
    n_q2 = np.linalg.norm(orilat.qFromHKL(q2))
    n_hkl = np.linalg.norm(orilat.qFromHKL(hkl))
    qx = cos(angle_q1_hkl) * n_hkl / n_q1
    qy = cos(angle_q2_hkl) * n_hkl / n_q2
    return [qx, qy]


def return_dns_surface_shape(orilat, tth_rang, omega_rang, q1, q2, wavelength):
    'returns TTH,OMEGA list of the surface boundary of dns sc measurement'
    UBinv = np.linalg.inv(orilat.getUB())
    line = []
    # create shape of dns measured surface in tth and omega
    tthr = np.concatenate((
        tth_rang[0] * np.ones(len(omega_rang)),
        tth_rang,
        tth_rang[-1] * np.ones(len(omega_rang)),
        np.flip(tth_rang)
        ))
    omegar = np.concatenate((
        np.flip(omega_rang),
        omega_rang[0] * np.ones(len(tth_rang)),
        omega_rang,
        omega_rang[-1] * np.ones(len(tth_rang))
        ))
    for i, omega in enumerate(omegar):
        hkl = angToHKL(tthr[i], omega, UBinv, wavelength)
        qx, qy = return_qxqy(orilat, q1, q2, hkl)
        line.append([qx, qy])
    line = np.asarray(line)
    return line

def listtoV3D(liste): # mantid has shity vector classes
    v3dv = V3D(liste[0], liste[1], liste[2])
    return v3dv