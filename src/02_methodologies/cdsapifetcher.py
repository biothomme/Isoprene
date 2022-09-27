# Here one can find a class to fetch ERA5 data from CDS using CDS-API
import cdsapi

class CDSAPIFetcher:
    def __init__(self, collection="reanalysis-era5-land"):
        # initialize cds api client
        self._initialize()
        
        # and store the collection key
        self.name_coll = collection
        return
    
    def _initialize(self):
        """_initialize

        Set up CDS API client for downloads.
        """        
        self.client = cdsapi.Client()
    
    def get_data(self, name_file, **kwargs_filter):
        self.client.retrieve(
            self.name_coll,
            kwargs_filter,
            name_file
        )
    
    def assemble_request(self, day, month, year, format="netcdf", variables=[],
                         times=[], area=[90, -180, -90, 180], **kwargs):

        """assemble_request

        Assemble a dictionary reflecting a CDS API request for one day.

        Args:
            day (int): day of the data
            month (int): month of the data
            year (int): year of the data
            format (str, optional): Format of the output. Defaults to "netcdf".
            variables (list, optional): List of data variables. Defaults to [].
            times (list, optional): List of times. Defaults to [].
            area (list, optional): Geographical boundaries ordered North, West,
                South, East. Defaults to [90, -180, -90, 180].


        Returns:
            dict: Dictionary for CDS API request.
        """
        TIME_DFLT =  [
            '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
            '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
            '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
            ]
        VAR_DFLT = [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "evaporation_from_vegetation_transpiration",
            "forecast_albedo",
            "leaf_area_index_high_vegetation",
            "leaf_area_index_low_vegetation",
            "skin_reservoir_content",
            "skin_temperature",
            "soil_temperature_level_1",
            "soil_temperature_level_2",
            "soil_temperature_level_3",
            "soil_temperature_level_4",
            "surface_pressure",
            "surface_sensible_heat_flux",
            "total_precipitation",
            "volumetric_soil_water_layer_1",
            "volumetric_soil_water_layer_2",
            "volumetric_soil_water_layer_3",
            "volumetric_soil_water_layer_4"
            ]
        
        # we assemble a dictionary from the short values and add ...
        dict_request = {
            'format': format,
            'day': str(day).rjust(2, '0'),
            'month': str(month).rjust(2, '0'),
            'year': str(year).rjust(2, '0'),
            "area": area,
            **kwargs}
        
        # ... for variables a long list as default
        if len(variables) == 0 : dict_request["variable"] = VAR_DFLT
        else : dict_request["variable"] = variables
        
        # for time, every hour is default
        if len(times) == 0 : dict_request["time"] = TIME_DFLT
        else : dict_request["time"] = times
        
        return dict_request
# end CDSAPIFetcher