Base.@kwdef mutable struct CDSFetcher
    variables = [
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
    
    # we define date by single units
    year::String
    month::String
    days::AbstractArray{String}

    # same for hours
    hours::AbstractArray{String}

    # we load latitudinal and longitudinal boundaries
    latmin::String
    latmax::String
    lonmin::String
    lonmax::String

    # we always take netCDF type
    format::String="netcdf"
end


function fetch(cdsf::CDSFetcher, directory::String)
    req = """
    {
        'variable': ['$(join(cdsf.variables, "', '"))', ],
        'year': '$(cdsf.year)',
        'month': '$(cdsf.month)',
        'day': ['$(join(cdsf.days, "', '"))', ],
        'time': ['$(join(cdsf.hours, "', '"))', ],
        
        'format': '$(cdsf.format)',
        'area': [
            $(cdsf.latmax), $(cdsf.lonmin), 
            $(cdsf.latmin), $(cdsf.lonmax),
        ],
    }
    """

    println(req, filename(cdsf, directory))
    # run the request
    #CDSAPI.retrieve(
    #    "reanalysis-era5-land",
    #    CDSAPI.py2ju(req, filename(cdsf, directory))
    #)
end

function filename(cdsf::CDSFetcher, directory::String)
    name = "era5hourly_$(cdsf.year)_$(cdsf.month)_$(cdsf.days[1])_$(replace(cdsf.hours[1], ':'=>'_')).nc"
    joinpath(directory, name)
end

function parse_date(string_date::String)
    match_regex = match(r"([^\-]*)\-([^\-]*)\-([^\ ]*) ([^\:]*:[^\:]*)", string_date)
    println(match_regex)
    Dict(
        "year" => match_regex[1],
        "month" => match_regex[2],
        "days" => [match_regex[3]],
        "hours" => [match_regex[4]]
    )
end

function CDSFetcher(string_date::String, latmin::String, latmax::String,
        lonmin::string, lonmax::String)
    dict_date = parse_date(string_date)
    CDSFetcher(
        year=dict_date["year"],
        month=dict_date["month"],
        days=dict_date["days"],
        hours=dict_date["hours"],
        latmin=latmin,
        latmax=latmax,
        lonmin=lonmin,
        lonmax=lonmax)
end

function fetch_csv(file_csv::String, directory::String)
    csv = CSV.File(open(file_csv, "r"))
    for row in csv
        cdsf = CDSFetcher(
            row["time"],
            row["latitude_min"],
            row["latitude_max"],
            row["longitude_min"],
            row["longitude_max"])
        fetch(cdsf, directory)
    end
end
