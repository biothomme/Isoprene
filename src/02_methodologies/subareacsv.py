# here one can find a class that reads subarea definitions from a csv file
# as well as subclasses with more extended functionalities

import dateutil
import os
import pandas as pd

from utils_cdsapi import make_name_outfile

class SubareaCSV:
    """ SubareaCSV

    Wrapper for csv file defining subareas for CDSAPI download.
    """
    def __init__(self, name_file):
        assert os.path.exists(name_file)
        self.file = name_file

        return
    
    def __iter__(self):
        self.data = pd.read_csv(self.file, chunksize=1)
        return self
    
    def __next__(self):
        return self.process_row(next(self.data))

    def process_row(self, row):
        """process_row 
        
        Assemble CDSAPI request given a csv row.

        Args:
            row (pd.DataFrame): Row of csv file.

        Returns:
            dict: Request arguments.
        """
        date_read = dateutil.parser.parse(row["time"].iat[0])
        dict_request = {
            "day": date_read.day,
            "month": date_read.month,
            "year": date_read.year,
            "time": [date_read.strftime("%H:%M")],
            "area": [
                row["latitude_max"].iat[0],
                row["longitude_min"].iat[0],
                row["latitude_min"].iat[0],
                row["longitude_max"].iat[0]
                ]
            }
        return dict_request
# end SubareaCSV


class NetCDFSubareaCSV(SubareaCSV):
    def __init__(self, name_file_csv, name_dir_netcdf,
                 base_netcdfs=None, suffix_netcdfs=None):
        # init the subarea file
        super().__init__(name_file_csv)
        
        # approve the directory with netcdfs exists
        assert os.path.exists(name_dir_netcdf)
        self.dir = name_dir_netcdf
        self.base_ncdf = base_netcdfs
        self.sfx_ncdf = suffix_netcdfs
        return
    
    def __next__(self):
        dict_row = super().__next__()
        name_ncdf = make_name_outfile("", dict_row)
        name_ncdf_prcd = self.process_name(name_ncdf)
        return dict_row, name_ncdf_prcd
    
    def process_name(self, name_file):
        # add base of name
        if self.base_ncdf is not None:
            name_file = f"{self.base_ncdf}{name_file}"
        
        # add suffix of name
        if self.sfx_ncdf is not None:
            name_file = f"{name_file}{self.sfx_ncdf}"
        
        # we append the full path
        name_file = os.path.join(self.dir, name_file)
        
        # and warn if it does not exist.
        if not os.path.exists(name_file):
            raise Warning(f"Attention, the file {name_file} does not exist.")
        return name_file
# end NetCDFSubareaCSV