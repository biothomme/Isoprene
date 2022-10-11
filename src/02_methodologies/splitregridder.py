# here we implement a class that allows to regrid very large netcdf files successively
import numpy as np
import os
import xarray as xr
import xesmf as xe

from regridder import RegridderSimple

class RegridderSplitted:
    """ RegridderSplitted

    Class to regrid large netCDF file using a split into subsets, stored as
    temporary files and concatenating their regridded output later.
    """
    def __init__(self):
        return