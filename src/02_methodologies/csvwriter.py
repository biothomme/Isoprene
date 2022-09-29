import csv
import os

class CSVWriter:
    def __init__(self, name_csvfile, header=None, force=False, append=True):
        # force is epistatic to append
        if not os.path.exists(name_csvfile) or force:
            append = False
        if os.path.exists(name_csvfile) and not force and not append:
            raise FileExistsError(name_csvfile)
        
        # decide if we want to append or not
        if append : mode_open = "a"
        else : mode_open = "w"
        
        # we need a header
        assert header is not None, "Header for csv is neccessary."
        self.header = header
        
        self.handle = open(name_csvfile, mode_open)
        self.writer = csv.DictWriter(self.handle, header)
        if mode_open == "w":
            self.writer.writeheader()
            print(f"Created file for logging download process: {name_csvfile}.")
        else :
            print(f"Append file for logging download process: {name_csvfile}.")
        return
        
    def write_dictrow(self, dict_row):
        if set(self.header) != set(dict_row.keys()):
            raise ValueError("Keys of csv and dictionary do not align. csv:"
                             f" {self.header}; dictionary: {dict_row.keys()}")
        self.writer.writerow(dict_row)
        self.handle.flush()
        return
    
    def write_listrow(self, list_row):
        if len(list_row) != len(self.header):
            raise ValueError("Keys of csv and row are of different length: "
                             f"csv ({len(self.header)}; row: {len(list_row)}")
        return self.write_dictrow(dict(zip(self.header, list_row)))