# here one can find a class that wraps around xarray.datasets
# with temporal dimensions to retrieve data of the closest
# date expected

from dateutil import parser
from dateutil.relativedelta import relativedelta
import os
import xarray as xr

from utils_dataloader import datetime_conversion

class XArrayTemporal:
    """ XArrayTemporal

    Wrapper around xarray.dataset with temporal dimension.
    """
    def __init__(self, array_temporal):
        # we assure that there is a dimension called time
        if not "time" in array_temporal.dims and not "ind" in array_temporal.dims:
            raise ValueError("The provided data array has no dimension `time` or `ind`.")
        if not "time" in array_temporal.dims:
            array_temporal = array_temporal.rename({"ind": "time"})

        # we convert string times to datetimes
        if isinstance(array_temporal["time"].values[0], str):
            array_temporal["time"] = [parser.parse(t) for t in array_temporal["time"].values]
        self.ds = array_temporal
        
        # load all years of the dataset
        self.dates = [datetime_conversion(t) for t in self.ds["time"].values]
        self.years = set([t.year for t in self.dates])
        return
    
    def get_closest_date(self, datetime_given):
        """get_closest_date _summary_

        Retrieve the closest date of the closest year to a given datetime
        provided, where an entry in the dataset exists.

        Args:
            datetime_given (datetime.datetime): Date to which the closest date
                within the closest year should be retrieved.

        Returns:
            numpy.datetime: _description_
        """
        # first get the closest year
        if not datetime_given.year in self.years:
            list_yeardeltas = [y-datetime_given.year for y in self.years]
            delta_best = sorted(list_yeardeltas, key=abs)[0]
            datetime_given = datetime_given+relativedelta(year=datetime_given.year+delta_best)
        # then we get the closest date using the closest year as new year
        list_timedeltas = [abs(t-datetime_given) for t in self.dates]
        datetime_closest = [
            t for t in self.dates if abs(t-datetime_given)==min(list_timedeltas)][0]
        return datetime_closest
    
    def select_date(self, datetime_given, overwrite=True):
        """select_date

        Find the data for the closest date of the closest year of a desired
        datetime.

        Args:
            datetime_given (datetime.datetime): Date that data should be close 
                to.
            overwrite (bool, optional): Overwrite the closest date with the date
                provided. Defaults to True.

        Returns:
            xr.dataset: Dataset of closest date.
        """
        datetime_closest = self.get_closest_date(datetime_given)
        # select the data given the date
        ds_for_date = self.ds.sel({"time": datetime_closest})
        
        # overwrite date instance with the date given
        if overwrite:
            ds_for_date["time"] = datetime_given
        return ds_for_date
# end XArrayTemporal