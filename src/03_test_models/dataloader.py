# here a dataloader for all features
import os
import pandas as pd
import xarray as xr

class LSMFeatureLoader:
    def __init__(self, dir_subareas, suffix_file=".nc", file_subareacsv=None):
        # directory with era5 files need to exist
        if not os.path.exists(dir_subareas):
            raise FileExistsError(f"Directory {dir_subareas} does not exist.")
        
        # list all files
        self.files_era5 = sorted(
            [os.path.join(dir_subareas, f) for f in os.listdir(dir_subareas) 
             if f.endswith(suffix_file)])

        # load the subarea csv file
        if file_subareacsv is not None:
            if not os.path.exists(file_subareacsv):
                raise FileExistsError(
                    f"CSV file {file_subareacsv} does not exist.")
            self.csv = pd.read_csv(file_subareacsv)
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
        self.iterator = (LSMFeature(f) for f in self.files_era5)
        return self
    
    def __next__(self):
        return next(self.iterator)
        
# end LSNFeatureLoader

class LSMFeature:
    def __init__(self, file_netcdf, **kwargs):
        self.da = xr.load_dataset(file_netcdf)
        self.attach_features(**kwargs)
        return
    
    def attach_features(self, **kwargs):
        return