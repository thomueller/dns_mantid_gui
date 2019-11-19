from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
# import mantid algorithms
from mantid.simpleapi import LoadDNSLegacy, MergeRuns, DeleteWorkspaces, GroupWorkspaces, ConvertUnits
from mantid.simpleapi import ConvertToDistribution, CorrectKiKf, ConvertToMD, ConvertToMDMinMaxGlobal, MergeMD, BinMD, mtd
__author__ = "m.ganeva.fz-juelich.de"
#-------------------------
# helper functions
#-------------------------

def pre_load_data(run_numbers, prefix, p, data):
    """
    helper function to load data
    """
    wslist = []
    for rn in run_numbers:
        infile = '{}/{}_{}.d_dat'.format(data['data_path'], data['proposal_number'], rn)
        wsname = os.path.splitext(infile)[0]
        if p['wavelength'] > 0:
            LoadDNSLegacy(infile, Normalization='no', ElasticChannel=p['e_channel'], Wavelength=p['wavelength'], OutputWorkspace=wsname)
        else:
            LoadDNSLegacy(infile, Normalization='no', ElasticChannel=p['e_channel'], OutputWorkspace=wsname)
        wslist.append(wsname)

    ws = MergeRuns(wslist, SampleLogsSum='mon_sum,duration', SampleLogsTimeSeries='deterota,T1,T2,Tsp', OutputWorkspace=prefix)
    if p['delete_raw']:
        DeleteWorkspaces(wslist)
    return ws

def load_data(data, prefix, p):
    wslist = []
    for i, runs in enumerate(data['data_numbers'].values()):
        wsname = "{}_{}".format(prefix, i+1)
        pre_load_data(runs, wsname, p, data)
        wslist.append(wsname)
    GroupWorkspaces(wslist, OutputWorkspace=prefix)

def convert_to_dE(gws, Ei):
    dEws = '{}_dE'.format(gws)
    ConvertUnits(gws, Target='DeltaE', EMode='Direct', EFixed=Ei, OutputWorkspace=dEws)
    ConvertToDistribution(dEws)
    sws = '{}_dE_S'.format(gws)
    CorrectKiKf(dEws, OutputWorkspace=sws)

def get_sqw(gws_name, outws_name, b):
    gws = mtd[gws_name]
    minvals, maxvals = ConvertToMDMinMaxGlobal(gws[0], '|Q|', 'Direct')
    outws = 'g{}_mde'.format(outws_name)
    ConvertToMD(gws, QDimensions='|Q|', dEAnalysisMode='Direct',
                PreprocDetectorsWS="-", MinValues=minvals, MaxValues=maxvals, OutputWorkspace=outws)
    outws1 = '{}_mde'.format(outws_name)
    if gws.getNumberOfEntries() > 1:
        MergeMD(outws, OutputWorkspace=outws1)
    else:
        outws1 = outws

    xbins = int((b['qmax'] - b['qmin'])/b['qstep'])
    xmax = b['qmin'] + xbins*b['qstep']
    ad0 = '|Q|,{qmin},{qmax},{qbins}'.format(qmin=b['qmin'], qmax=xmax, qbins=xbins)

    ybins = int((b['dEmax'] - b['dEmin'])/b['dEstep'])
    ymax = b['dEmin'] + ybins*b['dEstep']
    ad1 = 'DeltaE,{ymin},{ymax},{ybins}'.format(ymin=b['dEmin'], ymax=ymax, ybins=ybins)
    BinMD(InputWorkspace=outws1, AlignedDim0=ad0, AlignedDim1=ad1, OutputWorkspace='{}_sqw'.format(outws_name))
