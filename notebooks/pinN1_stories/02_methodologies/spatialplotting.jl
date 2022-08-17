using NCDatasets
using Plots

"""
    plot_ncdf(netcdfile::AbstractString)

Visualize geographical NetCDF file. File must list 2D geospatial scalar values
as `data` variable. The dimension axes must be named `lon` and `lat`.
"""
function plot_ncdf(netcdfile::AbstractString;
        palette::Union{String,Symbol}=:magma, width=1500, height=1000)
    # load dataset with NCDataset. Alternatively one could use NetCDF.jl,
    # but they should be merged one day (acc. to julia slack).
    ds = NCDataset(netcdfile)

    # store axis and z-data
    ranges = [dm ∈ ["lat", "lon"] ? range(1, stop=length(ds[dm])) : 1 for dm ∈ keys(ds.dim)]
    ncvar = ds["data"][ranges...]
    lon = ds["lon"][:]
    lat = ds["lat"][:]

    # make plot
    heatmap(lon, lat, fillnan(ncvar)', c=palette, size=(width, height),
        aspect_ratio=:equal)
    title!(splitdir(netcdfile)[2])
    xlabel!("longitude")
    ylabel!("latitude")
end


# TODO: move to utils
"""
    fillnan(numericarray::AbstractArray{NT})

Fill all `NaN`in numeric Array with zeros of the type of the array and
return altered array.
"""
function fillnan(numericarray::AbstractArray{NT}) where NT<:Number
    typezero = convert(eltype(numericarray), 0)
    replace(numericarray, NaN => typezero)
end
