# here we implement a class that allows to regrid very large netcdf files successively
import numpy as np
import os
import xarray as xr
import xesmf as xe

from regridder import RegridderSimple
from xarraysplitter import XArraySplitter

class RegridderSplitted(RegridderSimple):
    """ RegridderSplitted

    Class to regrid large netCDF file using a split into subsets, stored as
    temporary files and concatenating their regridded output later.
    """
    def __init__(self, name_ncfile, fill_na=True,
                 value_fill_na=0) -> None:
        assert os.path.exists(name_ncfile)
        self.file = name_ncfile
        
        # load the xarray
        self.ds = xr.open_dataset(self.file)
        
        # save if nas should be filled
        self.fillna = fill_na
        self.value_fill = value_fill_na
        return
        
    def regrid(self, dir_tempfiles=".", prefix_tempfiles="temp_split", 
               suffix_tempfiles="nc", name_latitude="lat", name_longitude="lon", 
               range_latitude=np.arange(-89.95, 89.95+.1, .1),
               range_longitude=np.arange(-179.95, 179.95+.1, .1),
               method="bilinear", force=False,
               extrap_method="nearest_s2d", copy_attributes=True,
               threshold=.000001, factor=1, engine="h5netcdf"):
        from functools import reduce
        from tempfile import TemporaryDirectory
        
        # make temporary directory
        if not os.path.exists(dir_tempfiles) : os.makedirs(dir_tempfiles)
        dir_temp = TemporaryDirectory(dir=dir_tempfiles)
        if hasattr(self, "td") : self.td.cleanup()
        self.td = dir_temp  # for easy closing
        
        # we need to avoid combination "conservative" with extrapolation
        if method == "conservative" : extrap_method = None
        
        # making a template dataset with desired shape
        dict_additional_dims = {
            k: ([k], list(self.ds[k].values))
            for k in self.ds.dims
            if k not in [name_latitude, name_longitude]
        }
        ds_tmplt = xr.Dataset({
            "lat": ([name_latitude], range_latitude),
            "lon": ([name_longitude], range_longitude),
            **dict_additional_dims
            })
        
        # split the dataset
        self.array_split = XArraySplitter(
            self.ds, ds_tmplt, name_lat=name_latitude, name_lon=name_longitude,
            threshold=threshold, factor=factor)
        count_splits = len(self.array_split)
        
        # we produce all small regridded splits and store them in a temp dir
        for i, (ds_in, ds_out) in enumerate(self.array_split):
            if self.fillna : ds_in = ds_in.fillna(self.value_fill)
            
            # make regridder
            regridder = xe.Regridder(
                ds_in, ds_out, method, extrap_method=extrap_method)
            # finally regrid the array and copy the data attributes.
            ds_regridded = regridder(ds_in)
            if copy_attributes : ds_regridded = self._copy_attrs(ds_regridded)
            index = str(i).zfill(len(str(count_splits)))
            name_tempfile = self.assemble_name_file(
                dir_temp.name, prefix_tempfiles, suffix_tempfiles, index)
            ds_regridded.to_netcdf(name_tempfile, engine=engine)
            
        # cool, then we open all of the temp files and merge them to a large
        # dataset
        # get all names
        names_regridded_files = (
            os.path.join(dir_temp.name, f) for f in os.listdir(dir_temp.name))
        # load all xarrays - lazily
        list_datarray_rgrd = (xr.load_dataset(f) for f in names_regridded_files)
        # merge them
        ds_regridded = reduce(lambda x, y: x.merge(y), list_datarray_rgrd)
        
        # remove the temporary dir
        self.td.cleanup()
        
        self.ds_regridded = ds_regridded
        
        return ds_regridded
    
    def assemble_name_file(self, dir_base, prefix, suffix, index):
        base_file = os.path.splitext(os.path.split(self.file)[-1])[0]
        return os.path.join(
            dir_base, f"{prefix}_{base_file}_{index}.{suffix}"
        )