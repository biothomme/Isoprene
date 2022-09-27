import ee
from functools import reduce

class EEERA5Fetcher:
    def __init__(self, collection="ECMWF/ERA5_LAND/HOURLY"):
        # we authenticate at EE
        self.authenticate()
        
        # and set the image collection
        self.name_coll = collection
        self.imgcoll = ee.ImageCollection(collection)
        return
        
    def authenticate(self):
        """authenticate

        Authenticate, authoritize and initialize at EarthEngine to allow
        downloads (see https://developers.google.com/earth-engine/guides/python_install#install-options).
        """
        # we only authenticate if no credentials are existing
        try:
            ee.oauth.get_credentials_arguments()
        except FileNotFoundError:
            print("Authentication needs to be performed:")
            ee.Authenticate()
        
        # we always initialize
        ee.Initialize()
        return
    
    def get_data(self, **kwargs_filter):
        """get_data
        
        Filter and load ImageCollection.

        Returns:
            imgcoll: filtered ImageCollection
        """        
    
        imgcoll = self.imgcoll
        
        # avoid mistakes in cases
        kwargs_filter = {k.lower(): v for k, v in kwargs_filter.items()}
        
        if "date" in kwargs_filter.keys():
            imgcoll = imgcoll.filterDate(kwargs_filter.pop("date"))
        if "bounds" in kwargs_filter.keys():
            imgcoll = imgcoll.filterBounds(kwargs_filter.pop("bounds"))
        
        imgcoll = reduce(lambda x, y: x.filter(y), kwargs_filter.values(), imgcoll)
        return imgcoll
    
# This class was depreceated as not useful - ERA5 collection at EE has lower
# resolution than the CDS.