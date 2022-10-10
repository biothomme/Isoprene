# here we implement classes to regrid the GriddingMachine.jl datasets
from datetime import datetime
import numpy as np
import os
import xarray as xr
import xesmf as xe

class RegridderSimple:
    def __init__(self, name_ncfile, fill_na=True,
                 value_fill_na=0) -> None:
        assert os.path.exists(name_ncfile)
        self.file = name_ncfile
        
        # load the xarray
        self.ds = xr.open_dataset(self.file)
        
        if len(self.ds.dims) > 2:
            self.ds = xr.open_dataset(self.file, chunks={"ind": 1})
        
        if fill_na : self.ds = self.ds.fillna(value_fill_na)
        return
    
    def regrid(self, name_latitude="lat", name_longitude="lon",
               range_latitude=np.arange(-89.95, 89.95+.1, .1),
               range_longitude=np.arange(-179.95, 179.95+.1, .1),
               method="bilinear", extrap_method="nearest_s2d",
               copy_attributes=True, force_new_regridder=False):
        """regrid

        Regrid NetCDF dataset using method.

        Args:
            name_latitude (str, optional): Name of the latitude dimension. Defaults to "lat".
            name_longitude (str, optional): Name of the longitude dimension. Defaults to "lon".
            range_latitude (list, optional): Array of latitude coordinates. Defaults to np.arange(-89.95, 89.95+.1, .1).
            range_longitude (list, optional):  Array of longitude coordinates. Defaults to np.arange(-179.95, 179.95+.1, .1).
            method (str, optional): Method for regridding. Defaults to "bilinear".
            extrap_method (str, optional): Method for extrapolation of data. Defaults to "nearest_s2d".
            copy_attributes (bool, optional): Copy attributes of the NetCDF file to the new one. Defaults to True.
            force_new_regridder (bool, optional): Force to set up new Regridder instance if already present. Defaults to False.

        Returns:
            xarray.array: Regridded Dataset
        """
        # we need to avoid combination "conservative" with extrapolation
        if method == "conservative" : extrap_method = None
        
        # initialize regridder if not given
        if not hasattr(self, "regridder") or force_new_regridder:
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
            # make regridder - this step takes ages
            self.regridder = xe.Regridder(
                self.ds, ds_tmplt, method, extrap_method=extrap_method)
            
        # finally regrid the array and copy the data attributes.
        ds_regridded = self.regridder(self.ds)
        if copy_attributes : ds_regridded = self._copy_attrs(ds_regridded)
        
        self.ds_regridded = ds_regridded
        return ds_regridded
    
    def regrid_and_save(self, name_outfile, force=False, engine="h5netcdf",
                        **kwargs):
        """regrid_and_save

        Regrid NetCDF dataset and save it as new file.

        Args:
            name_outfile (str): Name of the regridded new file.
            force (bool, optional): Force overwrite of file. Defaults to False.
            engine (str, optional): Engine to write new NetCDF file. Defaults to "h5netcdf".
        """
        if os.path.exists(name_outfile) and not force:
            raise FileExistsError(
                f"The desired output file {name_outfile} already exists."
            )
        # regrid the data
        self.regrid(**kwargs)
        
        # save the new netcdf file
        self.ds_regridded.to_netcdf(name_outfile, engine=engine)
        return
    
    def _copy_attrs(self, ds_regridded):
        """_copy_attrs

        Copy attributes from old dataset to given regridded dataset

        Args:
            ds_regridded (xarray.array): Regridded dataset.

        Returns:
            xarray.array: Regridded dataset with updated attributes.
        """
        STR_NEWLINE = "\n"
        # copy the overall attributes and add annotation
        ds_regridded.attrs = self.ds.attrs
        ds_regridded.attrs["notes"] += (f"{STR_NEWLINE}File was regridded for "
            "master project on Land Surface Modelling "
            f"(https://github.com/biothomme/Isoprene) on {datetime.now()}.")
        
        # copy attributes of each dimension/variable
        keys_ds = [*ds_regridded.dims, *ds_regridded.keys()]
        for key in keys_ds:
            ds_regridded[key].attrs = self.ds[key].attrs
        
        return ds_regridded
# end RegridderSimple
