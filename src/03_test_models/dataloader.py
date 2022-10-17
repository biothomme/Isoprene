# here a dataloader for all features
import numpy as np
import os
import pandas as pd
import xarray as xr

from temporalxarray import XArrayTemporal
from utils_dataloader import crop_dataset
from utils_dataloader import datetime_conversion

class LSMFeatureLoader:
    def __init__(self, dir_subareas, suffix_file=".nc", file_subareacsv=None,
                 random=False, **kwargs_datasets):
        # directory with era5 files need to exist
        if not os.path.exists(dir_subareas):
            raise FileExistsError(f"Directory {dir_subareas} does not exist.")

        # load the subarea csv file
        if file_subareacsv is not None:
            if not os.path.exists(file_subareacsv):
                raise FileExistsError(
                    f"CSV file {file_subareacsv} does not exist.")
            self.csv = pd.read_csv(file_subareacsv)
            self.csv.sort_values(by="time")
        
        # list all files - random or not
        self.random = random
        self.files_era5 = sorted(
            [os.path.join(dir_subareas, f) for f in os.listdir(dir_subareas) 
             if f.endswith(suffix_file)])
        
        # store the datasets that should be added and if order is random
        self.kwargs_add = kwargs_datasets
        return
    
    def get_file_date(self, name_file):
        """get_file_date 

        Obtain the date and time of a given file.

        Args:
            name_file (str): NetCDF file with ERA5 data.

        Returns:
            datetime.datetime: Date of data from input file.
        """
        with xr.load_dataset(name_file) as ar:
            return ar["time"].values[0]
    
    def __iter__(self):
        """__iter__

        Initialize (random) iterator for LSMFeatures.
        """
        from random import sample
        if self.random:
            self.iterator = (
                LSMFeature(f, **self.kwargs_add) for f in 
                sample(self.files_era5, len(self.files_era5)))
        else:
            self.iterator = (
                LSMFeature(f, **self.kwargs_add) for f in self.files_era5)
        return self
    
    def __next__(self):
        return next(self.iterator)
        
# end LSNFeatureLoader

class LSMFeature:
    def __init__(self, file_netcdf, name_add_dim = "ind", max_lonoffset=180,
                 max_latoffset=0, **kwargs):
        # dataset is loaded and name of additional dim stored
        self.dataset = xr.load_dataset(file_netcdf)
        for offs, dim in zip([max_lonoffset, max_latoffset],
                             ["longitude", "latitude"]):
            self.dataset[dim] = list(map(
                lambda x : -(2*offs)+x if x > offs else x,
                self.dataset[dim].values))
            self.dataset = self.dataset.sortby(dim)
        self.adddim = name_add_dim
        
        # additional files are attached and cropped to the ds size.
        self.attach_features(**kwargs)
        return
    
    def attach_features(self, temporal_datasets=["LAI", "CHLOROPHYLL"],
                        **feature_kwargs):
        ds_dest = self.dataset
        # we iterate over all features to attach them
        for k, file_feature in feature_kwargs.items():
            name_feature = k.lower()
            ds = crop_dataset(xr.open_dataset(file_feature), ds_dest)
            
            # temporal features need selection of the respective date
            if k in temporal_datasets : temporal = True
            else : temporal = False

            # for additional dimensions, we flatten the add datasets
            if self.adddim in ds.dims:
                if not temporal:
                    for i in ds[self.adddim].values:
                        name_layer = f"{name_feature}{i}"
                        layer_ds_new = ds.sel({self.adddim: i}).rename(
                            data=name_layer).drop(self.adddim)
                        ds_dest = ds_dest.merge(layer_ds_new[name_layer])
                    continue
                else:
                    # for temporal datasets we select the best date
                    wrapper_ds = XArrayTemporal(ds)
                    ds = wrapper_ds.select_date(
                        datetime_conversion(
                            ds_dest["time"].values[0])).drop("time")
            # otherwise, we simply combine the cropped dataset
            ds_new = ds.rename(data=name_feature)
            ds_dest = ds_dest.merge(ds_new[name_feature])
        
        # some datasets lost the time:
        for var in ds_dest.var():
            if "time" not in ds_dest[var].dims:
                ds_dest[var] = ds_dest[var].expand_dims(time=ds_dest["time"])
        self.dataset = ds_dest
        return ds_dest