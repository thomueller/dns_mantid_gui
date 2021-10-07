# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
import matplotlib
from matplotlib import colors
import matplotlib.cm as cm

def get_log_norm(log, zlim):
    if log:
        return colors.SymLogNorm(linthresh=0.001, vmin=zlim[0], vmax=zlim[1])
    return colors.Normalize(vmin=zlim[0], vmax=zlim[1])

def get_cmap(colormapname):
    return cm.get_cmap(name=colormapname, lut=None)

def get_shading(axis_type):
    shading = axis_type['shading']
