import os

def make_name_outfile(directory, dict_request, prefix="era5", suffix="nc"):
    """make_name_outfile

    Assemble name of file to download ERA5 data

    Args:
        directory (_type_): _description_
        dict_request (_type_): _description_
        prefix (str, optional): Defaults to "era5".
        suffix (str, optional): Defaults to "nc".

    Returns:
        _type_: _description_
    """
    dr = dict_request
    str_area = "_".join([str(int(a)) for a in dr["area"]])
    name_file = (f"{prefix}_{dr['year']}_{dr['month']}_{dr['day']}_"
                 f"{str_area}.{suffix}")
    return os.path.join(directory, name_file)