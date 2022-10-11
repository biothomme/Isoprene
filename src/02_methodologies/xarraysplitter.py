# here one can find a class that splits (large) xarrays into smaller netCDFs

class XArraySplitter:
    """XArraySplitter
    
    Class to split source data array into small units given an array template for destination.
    Cuts between the units are performed on congruent tile margins of source and destination.
    """
    def __init__(self, xarray_source, xarray_dest, threshold=.000001, name_lat="lat", name_lon="lon"):
        self.source = xarray_source
        self.dest = xarray_dest
        
        # store names for longitude and latitude
        self.lat, self.lon = name_lat, name_lon
        
        self.make_splits(threshold=threshold)
        return
    
    def make_splits(self, threshold=None):
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
        dict_points_congruent = {}
        self.slices = {}
        for dim in [self.lat, self.lon]:
            midpoints_source = midpoints(self.source[dim].values)
            midpoints_dest = midpoints(self.dest[dim].values)
            dict_points_congruent[dim] = [
                i for i, p in enumerate(midpoints_source)
                if np.any(np.abs(p-midpoints_dest) < threshold)
            ]
            self.slices[dim] = [slice(st, en+1) for st, en in zip(
                [0, *dict_points_congruent[dim]], [*dict_points_congruent[dim], len(self.source[dim].values)-1])]
        return 
    
    def __iter__(self):
        """Set up iterator for dataset splits.
        """
        from itertools import product
        self.iterator = (
            {self.lon: lo, self.lat: la} for lo, la in product(
                self.slices[self.lon], self.slices[self.lat]
            )
        )
        return self
    
    def __next__(self):
        """Return next split from dataset.
        """
        return self.source.isel(next(self.iterator))