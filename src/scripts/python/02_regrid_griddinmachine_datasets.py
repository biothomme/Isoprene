# IMPORTS
from functools import reduce
import os
import sys
import yaml
from inspect import getsourcefile


# PREAMBLE
PATHS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(getsourcefile(lambda:0))),
    "../../../PATHS.yml")   # this is a method flexible to exectuion location
PCAT = yaml.load(open(PATHS_FILE, "r"), Loader=yaml.FullLoader)


# UTIL
def get_path(*key_args):
    """get_path

    Convert path from catalogue file to absolute path for executing file.

    Returns:
        _type_: _description_
    """
    path = reduce(lambda x, y: x.get(y), key_args, PCAT)
    return os.path.abspath(os.path.join(os.path.dirname(PATHS_FILE), path))


# FUNCTIONS OF MAIN
def access_src_code():
    """access_src_code 

    Acces the directory with the Regridder classes.
    """
    DIR_METHODS = get_path("CODE", "METHODOLOGIES", "ROOT")
    sys.path.insert(1, DIR_METHODS)
    return

def split_datasets():
    """split_datasets 

    Group the GriddingMachine.jl datasets respective different ways of regridding.

    Returns:
        dict: Dictionary grouping the different datasets.
    """
    import xarray as xr
    
    dict_gmfeatures_grouped = {
        "temporal": {},
        "categorical": {},
        "multilayered": {},
        "simple": {}
    }
    dict_gmfeatures = {
        k: v for k, v
        in PCAT["DATA"]["FEATURES"].items()
        if "GRIDDING_MACHINE" in v}
    
    # for different kind of datasets we apply other regriddings
    # thus, we split them into 4 groups
    for k, v in dict_gmfeatures.items():
        # most complex are data with a time component
        # ATTENTION: xesmf does not support temporal regridding
        if not "_1Y_" in v["GRIDDING_MACHINE"]:
            group = "temporal"
        # most simple those with only lat and lon
        elif len(xr.open_dataset(
            get_path("DATA", "FEATURES", k, "GRIDDING_MACHINE")).sizes) == 2:
            group = "simple"
        # also we have PFT as mulilayered catergorical data
        elif k == "PLANT_FUNC_TYPE":
            group = "categorical"
        # and finally multilayered soil data
        else:
            group = "multilayered"
        dict_gmfeatures_grouped[group].update({k: v})
    return dict_gmfeatures_grouped

def get_regridder(name_ncfile):
    """get_regridder

    Make regridder instance for given file name.

    Args:
        name_ncfile (str): Path of netCDF file.

    Returns:
        regridder.RegridderSimple: Wrapper for regridding
    """
    from regridder import RegridderSimple
    return RegridderSimple(name_ncfile)



# MAIN
def main():
    # establish access to src code
    access_src_code()

    # group all datasets
    dict_datasets = split_datasets()
    
    # first we make the simple bilinear non temporal scalar regridding
    for key in dict_datasets["simple"].keys():
        if os.path.exists(get_path("DATA", "FEATURES", key, "V01")) : continue
        print(key)
        try:
            file_ds = get_path("DATA", "FEATURES", key, "GRIDDING_MACHINE")
            file_ds_regridded = get_path("DATA", "FEATURES", key, "V01")
        
            rgs = get_regridder(file_ds)
            rgs.regrid_and_save(file_ds_regridded)
        except TypeError:
            print("failed")
    # next, we do the same for the multilayered soil datsets
    for key in dict_datasets["multilayered"].keys():
        if os.path.exists(get_path("DATA", "FEATURES", key, "V01")) : continue
        file_ds = get_path("DATA", "FEATURES", key, "GRIDDING_MACHINE")
        file_ds_regridded = get_path("DATA", "FEATURES", key, "V01")
        
        rgs = get_regridder(file_ds)
        rgs.regrid_and_save(file_ds_regridded)
    
    # for the pft dataset we apply conservative mapping
    for key in dict_datasets["categorical"].keys():
        if os.path.exists(get_path("DATA", "FEATURES", key, "V01")) : continue
        file_ds = get_path("DATA", "FEATURES", key, "GRIDDING_MACHINE")
        file_ds_regridded = get_path("DATA", "FEATURES", key, "V01")
        
        rgs = get_regridder(file_ds)
        rgs.regrid_and_save(file_ds_regridded, method="conservative")

    # for the LAI dataset (temporal) we do not do regridding - already in shape
    pass

    print("Done!")
    return


# RUN
if __name__ == "__main__":
    main()
