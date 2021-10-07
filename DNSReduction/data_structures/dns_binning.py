import numpy as np

from mantidqtinterfaces.DNSReduction.data_structures.object_dict import ObjectDict


class DNSBinning(ObjectDict):
    """
    stores DNSBinning information, if the number of bins is not given
    it is calculated from the step size, also defines bin_edges
    """

    def __init__(self, xmin, xmax, step, number_of_bins=None):
        super().__init__()
        self['min'] = xmin
        self['max'] = xmax
        self['step'] = step
        if number_of_bins is None:
            if step == 0:
                number_of_bins = 1
            else:
                number_of_bins = int(round((xmax - xmin) / step) + 1)
        self['nbins'] = number_of_bins
        self['range'] = np.linspace(xmin, xmax, self.nbins)
        self['bin_edge_min'] = xmin - step / 2
        self['bin_edge_max'] = xmax + step / 2
        self['bin_edge_range'] = np.linspace(self.bin_edge_min,
                                             self.bin_edge_max,
                                             self.nbins + 1)
