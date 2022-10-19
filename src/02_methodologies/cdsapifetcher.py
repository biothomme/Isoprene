# Here one can find a class to fetch ERA5 data from CDS using CDS-API
from datetime import datetime
import numpy as np
import os
from urllib.parse import urljoin

from cdsapiclient import ClientMultiRequest
from csvwriter import CSVWriter
from subareacsv import SubareaCSV
from utils_cdsapi import make_name_outfile

class CDSAPIFetcher:
    def __init__(self, collection="reanalysis-era5-land",
                 # as alternative larger dataset:
                 # "reanalysis-era5-single-levels" but lower resolution.
                 wait_until_complete=True):
        # initialize cds api client
        self._initialize(wait_until_complete)
        
        # and store the collection key
        self.name_coll = collection
        return
    
    def _initialize(self, wait_until_complete):
        """_initialize

        Set up CDS API client for downloads.
        """        
        self.client = ClientMultiRequest(wait_until_complete=True)
        return
    
    def get_data(self, name_csvfile, dict_processlog={}, directory="",
                 name_logcsvfile=None, force=False, force_logger=False,
                 append_logger=True, offset=False, **kwargs):
        # we assign the logging file
        self.make_csv_logger(name_logcsvfile, directory, force=force_logger,
                            append=append_logger)
        
        # we wrap the csv file and iterate through all rows/requests
        sac = SubareaCSV(name_csvfile)
        for row in sac:
            # we make a unique name
            name_file = make_name_outfile(directory, row)
            # we avoid multiple requests and overwrite
            if name_file in dict_processlog.keys() : continue
            if os.path.exists(name_file) and not force : continue
            
            # if an additional offset (like a frame around the area) is given
            # we add it here:
            if offset:
                row["area"] = [f(v) for f, v in zip(
                    [np.ceil, np.floor, np.floor, np.ceil], row["area"])]
            
            # make the request
            request = self.assemble_request(**row, **kwargs)
            
            print(request)
            
            # submit it and wait
            timestamp_request = datetime.now()
            result = self.client._api("%s/resources/%s" % (
                self.client.url, self.name_coll), request, "POST")
            
            # download it
            result.download(target=name_file)
            
            # document the fetch
            dict_processlog[name_file] = result.reply
            list_log = [
                timestamp_request,                               # date_fetch
                urljoin(result._url, result.reply["location"]),  # url
                result.reply["request_id"],                      # id_request
                name_file,                                       # path
                f"{request['year']}-{request['month']}-{request['day']}",  # date_data
                os.path.getsize(name_file)                       # size
            ]
            self.logger_csv.write_listrow(list_log)
            
        # close the logger
        self.logger_csv.handle.close()
        del(self.logger_csv)
        
        return dict_processlog


    def assemble_request(self, day=None, month=None, year=None, format="netcdf",
                         variables=[], time=[], area=[90, -180, -90, 180],
                         **kwargs):
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
            "surface_net_solar_radiation",
            "surface_net_thermal_radiation",
            "surface_latent_heat_flux",
            "surface_solar_radiation_downwards",
            "surface_thermal_radiation_downwards",
            "total_precipitation",
            "volumetric_soil_water_layer_1",
            "volumetric_soil_water_layer_2",
            "volumetric_soil_water_layer_3",
            "volumetric_soil_water_layer_4" #,
            # "mean_surface_downward_short_wave_radiation_flux",
            # "mean_surface_direct_short_wave_radiation_flux"
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
        if len(time) == 0 : dict_request["time"] = TIME_DFLT
        else : dict_request["time"] = time
        
        return dict_request
    
    def make_csv_logger(self, name_csvfile, directory, **kwargs):
        LOGGING_HEADER = [
            "date_fetch", "url", "id_request", "path", "date_data", "size_file"]

        # we construct a name from the current time and date
        if name_csvfile is None:
            name_csvfile = datetime.now().strftime(
                "%Y_%m_%d_%H_%M_cdsapifetch.csv")
        path_csvfile = os.path.join(directory, name_csvfile)
        self.logger_csv = CSVWriter(path_csvfile, LOGGING_HEADER, **kwargs)
        return
# end CDSAPIFetcher