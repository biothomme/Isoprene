# here some supports for dataloading.
import numpy as np
import datetime

# cropping xarray datasets along longitude and latitude
def crop_dataset(ds_sourcegrid, ds_destgrid,
                 # era5 and griddingmachine.jl use different names for lat/lon
                 name_lat_source="lat", name_lat_dest="latitude",
                 name_lon_source="lon", name_lon_dest="longitude",
                 val_offset=.05, val_overoffset=0.01,
                 val_lonoffset=0, val_latoffset=0,
                 overwrite=True):
    """crop_dataset

    Crop source dataset to the shape of a destination dataset along longitudinal
    and latitudinal axes.

    Args:
        ds_sourcegrid (xr.dataset): Source dataset that should be cropped.
        ds_destgrid (xr.dataset): Destination dataset that provides the shape 
            for cropping.
        name_lat_source (str, optional): Defaults to "lat".
        name_lat_dest (str, optional): Defaults to "latitude".
        name_lon_source (str, optional): Defaults to "lon".
        name_lon_dest (str, optional): Defaults to "longitude".
        val_offset (float, optional): Value to shift the vales along each axis
            dimension. Defaults to .05.
        val_overoffset (float, optional): Additional buffer around the data on
            both sides. Defaults to 0.01.
        val_lonoffset (int, optional): Specific offset for longitudinal 
            dimenssion. Defaults to -180.
        val_latoffset (int, optional): Specific offset for latitudinal 
            dimenssion. Defaults to 0.
        overwrite (bool, optional): Overwrite the dimension values of the source
            dataset by ones of the destination. Defaults to True.

    Returns:
        xr.dataset: Cropped dataset.
    """
    # lambda to make slices that cover the area of cropping
    get_sign = lambda x : -1 if x[0] > x[-1] else 1
    get_stend = lambda x, i : 0-i if get_sign(x)==1 else -1+i
    add_offset = lambda x, y, i : np.around(np.add(x, y).values[get_stend(x, i)], decimals=len(str(y).split(".")[1]))

    # make slices to cut out piece of source grid using destgrid as template
    slat = slice(add_offset(ds_destgrid[name_lat_dest], 
                            val_latoffset+val_offset-val_overoffset, 0),
                 add_offset(ds_destgrid[name_lat_dest], 
                            val_latoffset+val_offset+val_overoffset, 1))
    slon = slice(add_offset(ds_destgrid[name_lon_dest], 
                            val_lonoffset+val_offset-val_overoffset, 0),
                 add_offset(ds_destgrid[name_lon_dest], 
                            val_lonoffset+val_offset+val_overoffset, 1))
    
    # crop the sourcegrid
    ds_source_cropped = ds_sourcegrid.rename(
        {name_lat_source: name_lat_dest, name_lon_source: name_lon_dest}).sel(
        {name_lat_dest: slat, name_lon_dest: slon})
    print(ds_source_cropped["data"])
    # rewrite the dimensions of the cropped dataset
    if overwrite:
        for dim in ds_destgrid.dims:
            if dim in ["time", "ind"] : continue
            if False: #(ds_source_cropped[dim].values[0] - ds_source_cropped[dim].values[-1] *
                ds_source_cropped[dim] = ds_destgrid[dim].values[::-1]
                # ds_destgrid[dim].values[-1] - ds_destgrid[dim].values[0]) < 0:
            else:
                ds_source_cropped[dim] = ds_destgrid[dim].values
            #print(ds_source_cropped[dim])
    print(ds_source_cropped["data"])

    return ds_source_cropped

# converting dates to different types
def datetime_conversion(datetime_numpy):
    """datetime_conversion

    Convert numpy.datetime64 date to datetime.datetime object.

    Args:
        datetime_numpy (np.datetime64): Date provided.

    Returns:
        datetime.datetime: Date in converted format.
    """
    return datetime.datetime.utcfromtimestamp(int(datetime_numpy)/1e9)