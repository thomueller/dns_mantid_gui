from __future__ import (absolute_import, division, print_function, unicode_literals)

#-------------------------
# helper functions
#-------------------------


def get_filepath_string(data):
    run_numbers = [j for i in data['data_numbers'].values() for j in i] ## flatted numbers of all banks in one list
    filepaths = []
    for rn in run_numbers:
        infile = '{}/{}_{}.d_dat'.format(data['data_path'], data['proposal_number'], rn)
        filepaths.append(infile)
    filepath_mantid = ",".join(filepaths)
    return filepath_mantid




def hkl_string_to_mantid_string(hkl):
    """hkl can contain brackets and spaces or commas as seperators """
    hkl = hkl.strip("[]()")
    hkl = hkl.replace(' ', ',')
    return hkl