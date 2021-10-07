# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS script helpers for elastic powder reduction
"""

import numpy as np
from mantid.simpleapi import (BinMD, CreateSingleValuedWorkspace, DivideMD,
                              LoadDNSSCD, MinusMD, MultiplyMD, PlusMD, mtd)

from mantidqtinterfaces.DNSReduction.data_structures.dns_error import DNSError


def load_all(data_dict, binning, params, standard=False):
    """Loading of multiple DNS files given in a dictionary to workspaces
    """
    workspacenames = {}
    for samplename, fields in data_dict.items():
        workspacenames[samplename] = []
        path = data_dict[samplename]['path']
        for fieldname, filenumbers in fields.items():
            if fieldname != 'path':
                workspacename = "_".join((samplename, fieldname))
                workspacenames[samplename].append(workspacename)
                load_binned(workspacename, binning, params, path, filenumbers,
                            standard)
    return workspacenames


def load_binned(workspacename, binning, params, path, filenumbers, standard):
    """Loading of multiple DNS datafiles into a single workspace
    """

    ad0 = 'Theta,{},{},{}'.format(binning['twoTheta'][0] / 2.0,
                                  binning['twoTheta'][1] / 2.0,
                                  binning['twoTheta'][2])
    ad1 = 'Omega,{},{},{}'.format(binning['Omega'][0], binning['Omega'][1],
                                  binning['Omega'][2])
    filepaths = ["{0}_{1:06d}.d_dat".format(path, number)
                 for number in list(filenumbers)]
    filepaths = ', '.join(filepaths)
    normname = "_".join((workspacename, 'norm'))
    if workspacename.endswith('_sf'):
        fieldname = workspacename[-4:]
    else:
        fieldname = workspacename[-5:]
    if not standard:
        LoadDNSSCD(FileNames=filepaths,
                   OutputWorkspace=workspacename,
                   NormalizationWorkspace=normname,
                   Normalization=params['norm_to'],
                   a=params['a'],
                   b=params['b'],
                   c=params['c'],
                   alpha=params['alpha'],
                   beta=params['beta'],
                   gamma=params['gamma'],
                   OmegaOffset=params['omega_offset'],
                   HKL1=params['hkl1'],
                   HKL2=params['hkl2'],
                   LoadAs='raw',
                   SaveHuberTo='huber_{}'.format(fieldname))
    else:
        LoadDNSSCD(FileNames=filepaths,
                   OutputWorkspace=workspacename,
                   NormalizationWorkspace=normname,
                   Normalization=params['norm_to'],
                   a=params['a'],
                   b=params['b'],
                   c=params['c'],
                   alpha=params['alpha'],
                   beta=params['beta'],
                   gamma=params['gamma'],
                   OmegaOffset=params['omega_offset'],
                   HKL1=params['hkl1'],
                   HKL2=params['hkl2'],
                   LoadAs='raw',
                   LoadHuberFrom='huber_{}'.format(fieldname))
    BinMD(InputWorkspace=workspacename,
          OutputWorkspace=workspacename,
          AxisAligned=True,
          AlignedDim0=ad0,
          AlignedDim1=ad1)

    BinMD(InputWorkspace=normname,
          OutputWorkspace=normname,
          AxisAligned=True,
          AlignedDim0=ad0,
          AlignedDim1=ad1)

    return mtd[workspacename]


def mmtd(workspacename):
    try:
        return mtd[workspacename]
    except KeyError:
        return None


def raise_error(error):
    raise DNSError(error)


def background_substraction(workspacename, factor=1):
    """ Subtraction of background files form other workspaces
    """
    if workspacename.startswith('empty'):
        return None
    if workspacename.endswith('_sf'):
        fieldname = workspacename[-4:]
    else:
        fieldname = workspacename[-5:]
    backgroundname = '_'.join(('empty', fieldname))
    workspacenorm = '_'.join((workspacename, 'norm'))
    backgroundnorm = '_'.join((backgroundname, 'norm'))
    try:
        mtd[backgroundname]
    except KeyError:
        raise_error('No background file for {}'.format(fieldname))
        return mtd[workspacename]
    ratio = mtd[workspacenorm] / mtd[backgroundnorm]
    background_scaled = mtd[backgroundname] * ratio * factor
    mtd[workspacename] = mtd[workspacename] - background_scaled
    return mtd[workspacename]


def vanadium_correction(workspacename,
                        vanaset=None,
                        ignore_vana_fields=False,
                        sum_vana_sf_nsf=False):
    """
    Correction of workspace for detector efficiency, angular coverage, lorentz
    factor based on vanadium data

    Key-Arguments
    vanaset = used Vanadium data, if not given fields matching sample are used
    ignore_vana_fields = if True fields of vanadium files will be ignored
    sum_vana_sf_nsf ) if True SF and NSF channels of vanadium are summed
    """
    vana_sum = None
    vana_sum_norm = None
    workspacenorm = '_'.join((workspacename, 'norm'))
    if workspacename.endswith('_sf'):
        fieldname = workspacename[-4:]
    else:
        fieldname = workspacename[-5:]
    if ignore_vana_fields:
        if vanaset:
            vanalist = []
            normlist = []
            for field in vanaset:
                if field != 'path':
                    vananame = '_'.join(('vana', field))
                    vananorm = '_'.join((vananame, 'norm'))
                    try:
                        vana = mtd[vananame]
                        vana_norm = mtd[vananorm]
                    except KeyError:
                        raise_error('No vanadium file for field {}. '.format(
                            fieldname))
                        return mtd[workspacename]
                    vanalist.append(vana)
                    normlist.append(vana_norm)
            vana_sum = sum(vanalist)
            vana_sum_norm = sum(normlist)
        else:
            raise_error(
                'Need to give vanadium dataset explicit if you want all'
                ' vandium files to be added.')
    elif sum_vana_sf_nsf:
        polarization = fieldname.split('_')[0]
        vana_nsf = '_'.join(('vana', polarization, 'nsf'))
        vana_sf = '_'.join(('vana', polarization, 'sf'))
        vana_nsf_norm = '_'.join((vana_nsf, 'norm'))
        vana_sf_norm = '_'.join((vana_sf, 'norm'))
        try:
            vana_sf = mtd[vana_sf]
            vana_sf_norm = mtd[vana_sf_norm]
        except KeyError:
            raise_error(
                'No vanadium file for {}_sf . You can choose to ignore'
                ' vanadium fields in the options.'.format(polarization))
            return mtd[workspacename]
        try:
            vana_nsf = mtd[vana_nsf]
            vana_nsf_norm = mtd[vana_nsf_norm]
        except KeyError:
            raise_error(
                'No vanadium file for {}_nsf. You can choose to ignore'
                ' vanadium fields in the options.'.format(polarization))
            return mtd[workspacename]
        vana_sum = vana_sf + vana_nsf
        vana_sum_norm = vana_sf_norm + vana_nsf_norm
    else:
        vananame = '_'.join(('vana', fieldname))
        vananorm = '_'.join((vananame, 'norm'))
        try:
            vana_sum = mtd[vananame]
            vana_sum_norm = mtd[vananorm]
        except KeyError:
            raise_error('No vanadium file for {}. You can choose to ignore'
                        ' vanadium fields in the options.'.format(fieldname))
            return mtd[workspacename]
    # common code, which will be run regardless of the case

    sum_signal = np.nan_to_num(vana_sum.getSignalArray())
    total_signal = np.sum(sum_signal)
    sum_error = np.nan_to_num(vana_sum.getErrorSquaredArray())
    total_error = np.sum(sum_error)
    sum_signal_norm = np.nan_to_num(vana_sum_norm.getSignalArray())
    total_signal_norm = np.sum(sum_signal_norm)
    sum_error_norm = np.nan_to_num(vana_sum_norm.getErrorSquaredArray())
    total_error_norm = np.sum(sum_error_norm)

    vana_total = CreateSingleValuedWorkspace(DataValue=total_signal,
                                             ErrorValue=np.sqrt(total_error))
    vana_total_norm = CreateSingleValuedWorkspace(
        DataValue=total_signal_norm, ErrorValue=np.sqrt(total_error_norm))

    coef_u = vana_sum / vana_total
    coef_norm = vana_sum_norm / vana_total_norm
    coef = coef_u / coef_norm
    MultiplyMD(coef, workspacenorm, OutputWorkspace=workspacenorm)
    DivideMD(workspacename, workspacenorm, OutputWorkspace=workspacename)
    return mtd[workspacename]


def fliping_ratio_correction(workspace):
    """Given SF channel, SF and NSF are corrected for finite flipping ratio """
    if workspace.endswith('_nsf'):
        return
    nsf_workspace = ''.join((workspace[:-2], 'nsf'))
    try:
        mtd[nsf_workspace]
    except KeyError:
        raise_error('no matching nsf workspace found for {}'.format(workspace))
        return
    sf_workspace = workspace
    sf = sf_workspace[-4:]
    nsf = nsf_workspace[-5:]
    nicr_sf = '_'.join(('nicr', sf))
    nicr_nsf = '_'.join(('nicr', nsf))
    nicr_sf_norm = '_'.join((nicr_sf, 'norm'))
    nicr_nsf_norm = '_'.join((nicr_nsf, 'norm'))
    try:
        _dummy = mtd[nicr_sf]
        _dummy = mtd[nicr_nsf]
    except KeyError:
        raise_error(
            'no matching NiCr workspace found for {}'.format(workspace))
        return
    new_nicr_sf = DivideMD(nicr_sf, nicr_sf_norm)
    new_nicr_nsf = DivideMD(nicr_nsf, nicr_nsf_norm)

    # 1/k, where k = NSF/SF - 1
    inverse_fr_divider = MinusMD(new_nicr_nsf, new_nicr_sf)
    inverse_fr = DivideMD(new_nicr_sf, inverse_fr_divider)

    # apply correction
    nsf_sf_diff = MinusMD(nsf_workspace, sf_workspace)
    diff_ifr = MultiplyMD(nsf_sf_diff, inverse_fr)
    mtd[sf_workspace] = MinusMD(sf_workspace,
                                diff_ifr,
                                OutputWorkspace=sf_workspace)
    mtd[nsf_workspace] = PlusMD(nsf_workspace,
                                diff_ifr,
                                OutputWorkspace=nsf_workspace)
