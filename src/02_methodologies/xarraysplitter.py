# here one can find a class that splits (large) xarrays into smaller netCDFs
import numpy as np
import xarray as xr

class XArraySplitter:
    """XArraySplitter
    
    Class to split source data array into small units given an array template for destination.
    Cuts between the units are performed on congruent tile margins of source and destination.
    """
    def __init__(self, xarray_source, xarray_dest, threshold=.000001,
                 name_lat="lat", name_lon="lon", factor=1):
        self.source = xarray_source
        self.dest = xarray_dest
        
        # store names for longitude and latitude
        self.lat, self.lon = name_lat, name_lon
        
        self.make_splits(threshold=threshold, factor=factor)
        return
    
    def make_splits(self, threshold=None, factor=None):
        """Compute how the source array can be split according to its congruency with the desitination array.
        """
        # lambda to compute the middle points between neighbouring values of a list
        midpoints = lambda x : [np.mean([v1, v2]) for v1, v2 in zip(x[0:-1], x[1:])]
        # lambda to compute the end points of a list
        endpoints = lambda x : (x[0] - (x[1]-x[0])/2, x[-1] + (x[-1]-x[-2])/2)
        
        # compute endpoints for all dimensions of source and dest
        dict_endpoints = {}
        dict_endpoints["source"], dict_endpoints["dest"] = {}, {}
        for dim in [self.lat, self.lon]:
            dict_endpoints["source"][dim], dict_endpoints["dest"][dim] = map(
                endpoints, [self.source[dim].values, self.dest[dim].values])
        dict_endpoints["min"] = {dim: (
            max(dict_endpoints["source"][dim][0], dict_endpoints["dest"][dim][0]),
            min(dict_endpoints["source"][dim][1], dict_endpoints["dest"][dim][1]))
                                for dim in [self.lat, self.lon]}
        
        # slice the dataframes, such that they are within an area that is covered by both dataframes
        dict_slicing = {k: slice(*v) for k, v in dict_endpoints["min"].items()}
        self.source = self.source.sel(dict_slicing)
        self.dest = self.dest.sel(dict_slicing)
        
        # now it is time to compute the splits, that will be conducted
        # therefore, we first need congruent points; i.e. midpoints of both datasets
        # that are almost covering each other
        dict_points_congruent = {"source": {}, "dest":{}}
        self.slices = {"source": {}, "dest":{}}
        for dim in [self.lat, self.lon]:
            # we collect all the indices of congruent tile margins in source
            # and dest array
            dict_midpoints = {
                "source": midpoints(self.source[dim].values),
                "dest": midpoints(self.dest[dim].values)}
            types = ["source", "dest"]
            for typ, xar in zip(types, [self.source, self.dest]):
                typ_other = [t for t in types if t != typ][0]
                dict_points_congruent[typ][dim] = [
                    i for i, p in enumerate(dict_midpoints[typ])
                    if np.any(np.abs(p-dict_midpoints[typ_other]) < threshold)
                ]
                slices = [slice(st+1, en+1) for st, en in zip(
                    [-1, *dict_points_congruent[typ][dim]],
                    [*dict_points_congruent[typ][dim], len(xar[dim].values)-1])]
                # we only take the slices that have an index that is multiple of
                # the given `factor`
                if len(slices) % factor != 0:
                    raise ValueError(
                        f"`factor` {factor} is no divisor of the number of "
                        f"congruent margins ({len(slices)}).")
                self.slices[typ][dim] = [
                    slice(slices[i].start, slices[i+factor-1].stop)
                    for i in range(0, len(slices)-factor, factor)]
        return 
    
    def __iter__(self):
        """Set up iterator for dataset splits.
        """
        from itertools import product
        self.iterator = (
            {"source": {self.lon: lo[0], self.lat: la[0]},
             "dest": {self.lon: lo[1], self.lat: la[1]}} for lo, la in product(
                zip(self.slices["source"][self.lon], self.slices["dest"][self.lon]),
                zip(self.slices["source"][self.lat], self.slices["dest"][self.lat])
            )
        )
        return self
    
    def __next__(self):
        """Return next split from dataset.
        """
        slice_current = next(self.iterator)
        return (self.source.isel(slice_current["source"]),
                self.dest.isel(slice_current["dest"]))
        
    def __len__(self):
        """Return amount of splits of the dataset.
        """
        return np.multiply(*map(
            lambda x : len(self.slices["source"][x])+1, [self.lat, self.lon]))