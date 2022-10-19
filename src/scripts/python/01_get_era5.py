# IMPORTS
from functools import reduce
import json
import os
import sys
from uritemplate import variables
import yaml
from inspect import getsourcefile


# PREAMBLE
PATHS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(getsourcefile(lambda:0))),
    "../../../PATHS.yml")   # this is a method flexible to exectuion location
PCAT = yaml.load(open(PATHS_FILE, "r"), Loader=yaml.FullLoader)


# UTIL
def get_path(*key_args):
    path = reduce(lambda x, y: x.get(y), key_args, PCAT)
    return os.path.abspath(os.path.join(os.path.dirname(PATHS_FILE), path))


# FUNCTIONS OF MAIN
def access_src_code():
    DIR_METHODS = get_path("CODE", "METHODOLOGIES", "ROOT")
    sys.path.insert(1, DIR_METHODS)

def get_cdsapi_fetcher():
    from cdsapifetcher import CDSAPIFetcher
    # return CDSAPIFetcher()
    return CDSAPIFetcher(collection="reanalysis-era5-single-levels")

def download_era5(cdsapi_fetcher):
    # define the csv file for subareas, the output directory, as well as the
    # csv file that tracks the progress.
    FILE_SUBAREAS_V1 = get_path("DATA", "FEATURES", "SUBAREASELECTION", "V01")
    # DIR_ERA5_V1 = get_path("DATA", "FEATURES", "ERA5HOURLY", "V01", "ROOT")
    DIR_ERA5_V1_EXTRA = get_path("DATA", "FEATURES", "ERA5HOURLY", "V01", "EXTRA")
    FILE_LOG = get_path("DATA", "FEATURES", "ERA5HOURLY", "V01", "LOG")
    FILE_LOG = get_path("DATA", "FEATURES", "ERA5HOURLY", "V01", "LOG_EXTRA")

    # for the extra task we only need 2 variables
    vars = ["mean_surface_downward_short_wave_radiation_flux",
            "mean_surface_direct_short_wave_radiation_flux"]
    
    # download the data
    cdsapi_fetcher.get_data(
        FILE_SUBAREAS_V1, directory=DIR_ERA5_V1_EXTRA, name_logcsvfile=FILE_LOG,
        #)
        offset=True, variables=vars, format="grib")
    return


# MAIN
def main():
    # establish access to src code
    access_src_code()

    # load fetcher class and create instance
    caf = get_cdsapi_fetcher()
    
    # download the data
    download_era5(caf)
    print("Done!")
    return


# RUN
if __name__ == "__main__":
    main()