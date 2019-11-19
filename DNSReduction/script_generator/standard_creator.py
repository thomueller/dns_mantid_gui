# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
presenter for dns path panel
"""

from __future__ import (absolute_import, division, print_function)
import numpy as np

fulldata = [{'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.0, 'filenumber': 554933, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554933.d_dat', 'field': 'x7_sf', 'sample_rot': 100.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.0, 'filenumber': 554934, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554934.d_dat', 'field': 'x7_nsf', 'sample_rot': 100.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.0, 'filenumber': 554935, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554935.d_dat', 'field': 'y7_sf', 'sample_rot': 100.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.0, 'filenumber': 554936, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554936.d_dat', 'field': 'y7_nsf', 'sample_rot': 100.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.0, 'filenumber': 554937, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554937.d_dat', 'field': 'z7_sf', 'sample_rot': 100.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.0, 'filenumber': 554938, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554938.d_dat', 'field': 'z7_nsf', 'sample_rot': 100.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.5, 'filenumber': 554939, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554939.d_dat', 'field': 'x7_sf', 'sample_rot': 99.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.5, 'filenumber': 554940, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554940.d_dat', 'field': 'x7_nsf', 'sample_rot': 99.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.5, 'filenumber': 554941, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554941.d_dat', 'field': 'y7_sf', 'sample_rot': 99.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.5, 'filenumber': 554942, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554942.d_dat', 'field': 'y7_nsf', 'sample_rot': 99.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.5, 'filenumber': 554943, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554943.d_dat', 'field': 'z7_sf', 'sample_rot': 99.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -5.5, 'filenumber': 554944, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554944.d_dat', 'field': 'z7_nsf', 'sample_rot': 99.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.0, 'filenumber': 554945, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554945.d_dat', 'field': 'x7_sf', 'sample_rot': 99.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.0, 'filenumber': 554946, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554946.d_dat', 'field': 'x7_nsf', 'sample_rot': 99.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.0, 'filenumber': 554947, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554947.d_dat', 'field': 'y7_sf', 'sample_rot': 99.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.0, 'filenumber': 554948, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554948.d_dat', 'field': 'y7_nsf', 'sample_rot': 99.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.0, 'filenumber': 554949, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554949.d_dat', 'field': 'z7_sf', 'sample_rot': 99.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.0, 'filenumber': 554950, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554950.d_dat', 'field': 'z7_nsf', 'sample_rot': 99.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.5, 'filenumber': 554951, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554951.d_dat', 'field': 'x7_sf', 'sample_rot': 98.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.5, 'filenumber': 554952, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554952.d_dat', 'field': 'x7_nsf', 'sample_rot': 98.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.5, 'filenumber': 554953, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554953.d_dat', 'field': 'y7_sf', 'sample_rot': 98.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.5, 'filenumber': 554954, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554954.d_dat', 'field': 'y7_nsf', 'sample_rot': 98.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.5, 'filenumber': 554955, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554955.d_dat', 'field': 'z7_sf', 'sample_rot': 98.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -6.5, 'filenumber': 554956, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554956.d_dat', 'field': 'z7_nsf', 'sample_rot': 98.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.0, 'filenumber': 554957, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554957.d_dat', 'field': 'x7_sf', 'sample_rot': 98.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.0, 'filenumber': 554958, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554958.d_dat', 'field': 'x7_nsf', 'sample_rot': 98.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.0, 'filenumber': 554959, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554959.d_dat', 'field': 'y7_sf', 'sample_rot': 98.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.0, 'filenumber': 554960, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554960.d_dat', 'field': 'y7_nsf', 'sample_rot': 98.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.0, 'filenumber': 554961, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554961.d_dat', 'field': 'z7_sf', 'sample_rot': 98.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.0, 'filenumber': 554962, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554962.d_dat', 'field': 'z7_nsf', 'sample_rot': 98.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.5, 'filenumber': 554963, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554963.d_dat', 'field': 'x7_sf', 'sample_rot': 97.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.5, 'filenumber': 554964, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554964.d_dat', 'field': 'x7_nsf', 'sample_rot': 97.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.5, 'filenumber': 554965, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554965.d_dat', 'field': 'y7_sf', 'sample_rot': 97.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.5, 'filenumber': 554966, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554966.d_dat', 'field': 'y7_nsf', 'sample_rot': 97.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.5, 'filenumber': 554967, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554967.d_dat', 'field': 'z7_sf', 'sample_rot': 97.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.5, 'filenumber': 554968, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554968.d_dat', 'field': 'z7_nsf', 'sample_rot': 97.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.99, 'filenumber': 554969, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554969.d_dat', 'field': 'x7_sf', 'sample_rot': 97.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.99, 'filenumber': 554970, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554970.d_dat', 'field': 'x7_nsf', 'sample_rot': 97.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.99, 'filenumber': 554971, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554971.d_dat', 'field': 'y7_sf', 'sample_rot': 97.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.99, 'filenumber': 554972, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554972.d_dat', 'field': 'y7_nsf', 'sample_rot': 97.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.99, 'filenumber': 554973, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554973.d_dat', 'field': 'z7_sf', 'sample_rot': 97.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -7.99, 'filenumber': 554974, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554974.d_dat', 'field': 'z7_nsf', 'sample_rot': 97.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -8.5, 'filenumber': 554975, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554975.d_dat', 'field': 'x7_sf', 'sample_rot': 96.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -8.5, 'filenumber': 554976, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554976.d_dat', 'field': 'x7_nsf', 'sample_rot': 96.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -8.5, 'filenumber': 554977, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554977.d_dat', 'field': 'y7_sf', 'sample_rot': 96.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -8.5, 'filenumber': 554978, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554978.d_dat', 'field': 'y7_nsf', 'sample_rot': 96.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -8.5, 'filenumber': 554979, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554979.d_dat', 'field': 'z7_sf', 'sample_rot': 96.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -8.5, 'filenumber': 554980, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554980.d_dat', 'field': 'z7_nsf', 'sample_rot': 96.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.0, 'filenumber': 554981, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554981.d_dat', 'field': 'x7_sf', 'sample_rot': 96.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.0, 'filenumber': 554982, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554982.d_dat', 'field': 'x7_nsf', 'sample_rot': 96.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.0, 'filenumber': 554983, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554983.d_dat', 'field': 'y7_sf', 'sample_rot': 96.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.0, 'filenumber': 554984, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554984.d_dat', 'field': 'y7_nsf', 'sample_rot': 96.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.0, 'filenumber': 554985, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554985.d_dat', 'field': 'z7_sf', 'sample_rot': 96.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.0, 'filenumber': 554986, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554986.d_dat', 'field': 'z7_nsf', 'sample_rot': 96.0}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.49, 'filenumber': 554987, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554987.d_dat', 'field': 'x7_sf', 'sample_rot': 95.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.49, 'filenumber': 554988, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554988.d_dat', 'field': 'x7_nsf', 'sample_rot': 95.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.49, 'filenumber': 554989, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554989.d_dat', 'field': 'y7_sf', 'sample_rot': 95.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.49, 'filenumber': 554990, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554990.d_dat', 'field': 'y7_nsf', 'sample_rot': 95.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.49, 'filenumber': 554991, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554991.d_dat', 'field': 'z7_sf', 'sample_rot': 95.5}, {'channelwidth': 1.3, 'sampletype': '_knso', 'wavelength': 4.2, 'det_rot': -9.49, 'filenumber': 554992, 'tofchannels': 1, 'temperature': 3.5, 'samplename': '_knso', 'filename': u'C:/data/p13656\\p13656_554992.d_dat', 'field': 'z7_nsf', 'sample_rot': 95.5}]
#vanadata = fulldata



field_dict = {
    'x7_sf'    : 'x_sf',
    'x20_sf'   : 'x_sf',
    '-x7_sf'   : 'minus_x_sf',
    '-x20_sf'  : 'minus_x_sf',
    'x7_nsf'   : 'x_nsf',
    'x20_nsf'  : 'x_nsf',
    '-x7_nsf'  : 'minus_x_nsf',
    '-x20_nsf' : 'minus_x_nsf',
    'y7_sf'    : 'y_sf',
    'y20_sf'   : 'y_sf',
    '-y7_sf'   : 'minus_y_sf',
    '-y20_sf'  : 'minus_y_sf',
    'y7_nsf'   : 'y_nsf',
    'y20_nsf'  : 'y_nsf',
    '-y7_nsf'  : 'minus_y_nsf',
    '-y20_nsf' : 'minus_y_nsf',
    'z7_sf'    : 'z_sf',
    'z20_sf'   : 'z_sf',
    '-z7_sf'   : 'minus_z_sf',
    '-z20_sf'  : 'minus_z_sf',
    'z7_nsf'   : 'z_nsf',
    'z20_nsf'  : 'z_nsf',
    '-z7_nsf'  : 'minus_z_nsf',
    '-z20_nsf' : 'minus_z_nsf',
    }


number_dict = {entry['filenumber']: entry for entry in fulldata}

def create_standard():
    dataset = {}
    for entry in  fulldata:
        if entry['samplename'] not in ['vana', 'nicr', 'leer', 'empty']:
            datatype = 'sample'
        elif entry['samplename'] == 'leer': ## compatibility with old dnsplot names for empty
            datatype = 'empty'
        else:
            datatype = entry['samplename']
        field = field_dict.get(entry['field'], entry['field'])
        datapath = entry['filename'].replace('_'+str(entry['filenumber'])+'.d_dat', '')
        if datatype in dataset.keys():
            if field in dataset[datatype].keys():
                if datapath in  dataset[datatype][field].keys():
                    dataset[datatype][field][datapath].append(entry['filenumber'])
                else:
                    dataset[datatype][field][datapath] = [entry['filenumber']]#
            else:
                dataset[datatype][field] = {}
                dataset[datatype][field][datapath] = [entry['filenumber']]
        else:
            dataset[datatype] = {}
            dataset[datatype][field] = {}
            dataset[datatype][field][datapath] = [entry['filenumber']]
    #print(dataset)
    return dataset
data = create_standard()



#### reading vanadium data
vanadata = {'sample': {'x_sf': {u'C:/data/p13656\\p13656': [554933, 554939, 554945, 554951, 554957, 554963, 554969, 554975, 554981, 554987]}, 'z_sf': {u'C:/data/p13656\\p13656': [554937, 554943, 554949, 554955, 554961, 554967, 554973, 554979, 554985, 554991]}, 'y_nsf': {u'C:/data/p13656\\p13656': [554936, 554942, 554948, 554954, 554960, 554966, 554972, 554978, 554984, 554990]}, 'z_nsf': {u'C:/data/p13656\\p13656': [554938, 554944, 554950, 554956, 554962, 554968, 554974, 554980, 554986, 554992]}, 'x_nsf': {u'C:/data/p13656\\p13656': [554934, 554940, 554946, 554952, 554958, 554964, 554970, 554976, 554982, 554988]}, 'y_sf': {u'C:/data/p13656\\p13656': [554935, 554941, 554947, 554953, 554959, 554965, 554971, 554977, 554983, 554989]}}}
arr = []
for mykey, values in vanadata['sample']['x_sf'].items():
    for number in values:
        filename = '{}_{}.d_dat'.format(mykey, number)
        with open(filename, 'r') as f:
            txt = f.readlines()
        del f
        det_rot = float(txt[13][-15:-5].strip())
        time = float(txt[56][-15:-5].strip())
        monitor = int(txt[57][-15:-1].strip())
        int_list = [det_rot, time, monitor]
        for i in range(24):
            int_list.append(int(txt[74+i][3:-1].strip()))
        arr.append(int_list)
        del txt
arr = np.reshape(np.asarray(arr), (-1, 27))
arr = np.sort(arr, axis=0)


#### averaging standard files which are closer together than 0.05
### simply starts rom lowest value, if you choose rounding limit to large
### all will be put in 1 bin
rounding_limit = 0.05
new_arr = []
dividers = []
inside = False
for line in arr:
    for number, compare in enumerate(new_arr):
        if abs(compare[0]-line[0]) < rounding_limit:
            inside = True
            break
        else:
            inside = False
    if inside:
        new_arr[number] = new_arr[number] + line
        dividers[number] += 1
    else:
        new_arr.append(line)
        dividers.append(1)
for number, divisor in enumerate(dividers):
    new_arr[number][0] = new_arr[number][0]/divisor
new_arr = np.stack(new_arr)
print(new_arr)

## interpolating new intensities
x = [-10.1, -9, -8, -7.4, -6.9, -6, -5.25, -4.5]
alle = []
for det_number in range(27):
    alle.append(np.round(np.interp(x=x, xp=arr[:, 0], fp=arr[:, det_number]), 2))
new = np.vstack(alle)
new[0] = x
new = np.transpose(new) #np.reshape(alle,(len(x),-1))
print(new)
