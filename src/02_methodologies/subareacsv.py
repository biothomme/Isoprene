import dateutil
import os
import pandas as pd

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

