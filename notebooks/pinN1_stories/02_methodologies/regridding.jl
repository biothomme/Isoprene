using IntervalSets: OpenInterval

const GLAT_MIN, GLAT_MAX = -90., 90.
const GLON_MIN, GLON_MAX = -180., 180.
const GIND_MIN, GIND_MAX = 1., 12.


"""
    RegridAxis{IT, FT}

Discrete axis that provides minimal and maximal values as well as cardinality
for regridding axes.
"""
mutable struct RegridAxis{IT<:Integer, FT<:AbstractFloat}
    # axis should have a name
    name::String

    # regridding needs min, max of axis
    coordmin::FT
    coordmax::FT

    # define number of steps - the cardinality
    coordcard::IT
end

"""
    RegridAxis{IT, FT}(name::string, coordmin::FT, coordmax::FT, coordcard::IT)

Create a `RegridAxis` object that recognizes swapped min and max coordinates.
"""
function RegridAxis(name::String, coordmin::FT, coordmax::FT,
        coordcard::IT) where {IT<:Integer, FT<:AbstractFloat}
    coords = [coordmin, coordmax]
    RegridAxis{IT, FT}(name, minimum(coords), maximum(coords), coordcard)
end

"""
    RegridAxis(name::String, pointrange::AbstractArray{FT})

Create a `RegridAxis` object with a numericàrray that represents a
range of points. Maximum, minimum and carinality of the array are
used as defining characteristics of the `RegridAxis`.
"""
function RegridAxis(name::String, 
        pointrange::AbstractArray{FT}) where FT<:AbstractFloat
    prsz½ = stepsize(pointrange) / 2
    prmin = minimum(pointrange) - prsz½
    prmax = maximum(pointrange) + prsz½
    prcard = length(pointrange)

    RegridAxis{Int64, FT}(name, prmin, prmax, prcard)
end


# length of axes
Base.length(rga::RegridAxis) = rga.coordcard

# min-max distance of axes and stepsize of given cardinality
minmaxdist(rga::RegridAxis) = rga.coordmax - rga.coordmin
stepsize(rga::RegridAxis) = minmaxdist(rga) / rga.coordcard

# minima and maxima of the discrete points on the axis
Base.minimum(rga::RegridAxis) = rga.coordmin + stepsize(rga)/2
Base.maximum(rga::RegridAxis) = rga.coordmax - stepsize(rga)/2

# range of all points and interval boarders on the axis
Base.range(rga::RegridAxis) = minimum(rga):stepsize(rga):maximum(rga)
function intervals(rga::RegridAxis) 
    map(ax -> (OpenInterval(ax-stepsize(rga)/2, ax+stepsize(rga)/2)),
        range(rga))
end


# Regridding of NetCDF files can be performed using Regridder subtypes
"""
    Regridder{IT, FT}

Abstract type for tools that allow multidimensional regridding based on
orthogonal RegridAxis{IT, FT}.
"""
abstract type Regridder{IT<:Integer, FT<:AbstractFloat}
    # regridding is performed on multiple axes
end

"""
     Regridder(ncds::NCDatasets.NCDataset; kwargs...)

Create a Regridder subtype (Regridder2D, Regridder3D) using an existing NetCDF dataset
`ncds`. The dimensionality of `ncds` is recognized.
"""
function Regridder(ncds::NCDatasets.NCDataset; kwargs...)
    let ndim = length(keys(ncds.dim))
        if ndim == 2
            Regridder2D(ncds; kwargs...)
        elseif ndim == 3
            Regridder3D(ncds; kwargs...)
        end
    end
end

Base.size(rg::RG) where RG<:Regridder = tuple(map(length, rg.axes)...)
cardinality(rg::RG) where RG<:Regridder = Dict(ax.name => length(ax) for ax
        in rg.axes)
ranges(rg::RG) where RG<:Regridder = Dict(ax.name => range(ax) for ax
        in rg.axes)


# Regridder2D - for lat+lon
"""
    Regridder2D{IT, FT}

Tool that allow 2 dimensional regridding based on orthogonal
RegridAxis{IT, FT}. As default axes are assumed to be latitude and longitude.
"""
mutable struct Regridder2D{IT<:Integer, FT<:AbstractFloat} <: Regridder{IT, FT}
    axes::Array{RegridAxis{IT, FT}, 1}
end

"""
    Regridder2D{IT, FT}(latmin::FT, latmax::FT, lonmin::FT, lonmax::FT,
        latcard::IT, loncard::IT)

Create a Regridder2D object from latitude and logitude minima and maxima as well
as cardinality for regridding.
"""
function Regridder2D(latcard::IT, loncard::IT; latmin::FT=GLAT_MIN,
        latmax::FT=GLAT_MAX, lonmin::FT=GLON_MIN,
        lonmax::FT=GLON_MAX) where {IT<:Integer, FT<:AbstractFloat}
    # regridding needs min, max of longitude and latitude
     axes = [
        RegridAxis("lat", latmin, latmax, latcard),
        RegridAxis("lon", lonmin, lonmax, loncard)
    ]
    Regridder2D(axes)
end

"""
    Regridder2D{IT, FT}(ncds::NCDatasets.NCDataset; lonname::String="lon",
        latname::String="lat")

Create a Regridder2D object from an existing NetCDF file wrapped by
`NCDatasets.NCDataset`. Default variable names for longitude and
latitude are `lon` and `lat`.
"""
function Regridder2D(ncds::NCDatasets.NCDataset; lonname::String="lon",
        latname::String="lat")
    latcard, loncard= length(ncds[latname]), length(ncds[lonname])
    latmin, latmax = extrema(ncds[latname])
    lonmin, lonmax = extrema(ncds[lonname])

    Regridder2D(latcard, loncard; latmin, latmax, lonmin, lonmax)
end


# Regridder3D - for lat+lon+time(cycle index)
"""
    Regridder3D{IT, FT}

Tool that allow 3 dimensional regridding based on orthogonal
RegridAxis{IT, FT}. As default axes are assumed to be latitude, longitude and
cycle index.
"""
mutable struct Regridder3D{IT<:Integer, FT<:AbstractFloat} <: Regridder{IT, FT}
    axes::Array{RegridAxis{IT, FT}, 1}
end

"""
    Regridder3D{IT, FT}(latmin::FT, latmax::FT indcard::FT; lonmin::FT, lonmax::FT,
        latcard::IT, loncard::IT, indmin::IT, indmax::IT)

Create a Regridder3Dis object from latitude, logitude and cycle index minima and maxima
as well as cardinality for regridding.
"""
function Regridder3D(latcard::IT, loncard::IT, indcard::IT; latmin::FT=GLAT_MIN,
        latmax::FT=GLAT_MAX, lonmin::FT=GLON_MIN, lonmax::FT=GLON_MAX,
        indmax::FT=GIND_MAX, indmin::FT=GIND_MIN) where {IT<:Integer, FT<:AbstractFloat}
    # regridding needs min, max of longitude and latitude
     axes = [
        RegridAxis("lat", latmin, latmax, latcard),
        RegridAxis("lon", lonmin, lonmax, loncard),
        RegridAxis("ind", indmin, indmax, indcard)
    ]
    Regridder3D(axes)
end

"""
    Regridder3D{IT, FT}(ncds::NCDatasets.NCDataset; lonname::String="lon",
        latname::String="lat", indname::String="ind")

Create a Regridder3D object from an existing NetCDF file wrapped by
`NCDatasets.NCDataset`. Default variable names for longitude, latitude
and cycle index are `lon`, `lat` and `ind`.
"""
function Regridder3D(ncds::NCDatasets.NCDataset; lonname::String="lon",
        latname::String="lat", indname::String="ind")
    latcard, loncard, indcard = (x -> length(ncds[x])).([latname, lonname, indname])
    
    latmin, latmax = extrema(ncds[latname])
    lonmin, lonmax = extrema(ncds[lonname])
    indmin, indmax = promote(extrema(ncds[indname])..., lonmin)[1:2]
    
    Regridder3D(latcard, loncard, indcard; latmin, latmax, lonmin, lonmax, indmin, indmax)
end









###############################
function regrid_data(regridder::RG, ncds::NCDataset, variables::AbstractArray{String}, operation::Function; kwargs...) where RG<:Regridder
    regridder_ncds = Regridder(ncds; kwargs...)
    ncdims = keys(ncds.dim)

    dim_itvs = map(x -> dimwise_intervals(regridder)[x], ncdims)
    dim_itvs_ncds = map(x -> dimwise_intervals(regridder_ncds)[x], ncdims)
    
    regridded_template = init_regridded(tuple(map(x -> cardinality(regridder)[x], ncdims)...))
    regridded_ncds = Dict(var => deepcopy(regridded_template)
        for var in variables)

    for idx in CartesianIndices(axes(regridded_template))
        idxs = Tuple(idx)
        tile = map(((x,y),) -> x[y], zip(dim_itvs, idxs))
        rgrd_values = regrid_cell(ncds, [tile...], dim_itvs_ncds, variables, operation)

        for (j, var) in enumerate(variables)
            if rgrd_values[j] > 0
                regridded_ncds[var][idxs...] = rgrd_values[j]
            end
        end
    end
    regridded_ncds
end

function regrid_dataset(filename::String, regridder::RG, ncds::NCDataset, 
        variables::AbstractArray{String}, operation::Function; force::Bool=false, 
        kwargs...) where RG<:Regridder
    # as default we avoid overwriting
    if ispath(filename) 
        !force ? (return) : rm(filename)
    end
    
    # in the first step we regrid the data
    regridded_ncds = regrid_data(regridder, ncds, variables, operation; kwargs...)

    # then we instantiate the new NetCDF file.
    new_ncds = NCDataset(filename,"c")
    
    # we run through all dimensions and add them
    ncdims = keys(ncds.dim)
    for ncdim in ncdims
        defDim(new_ncds, ncdim, cardinality(regridder)[ncdim])
        dim_levels = collect(ranges(regridder)[ncdim])
        defVar(new_ncds, ncdim, eltype(dim_levels), tuple(ncdim))
        new_ncds[ncdim][:] = dim_levels
    end
    
    # finally we copy the data
    for var in variables
        defVar(new_ncds, var, eltype(regridded_ncds[var]), tuple(ncdims...))
        new_ncds[var][:,:] = regridded_ncds[var]
    end
    new_ncds
end

###############################






# UTILS
"""
    minmaxdist(pointrange::AbstractArray{FT})

Retrieve the difference between minimum and maximum of a given numeric
Array (Float).
"""
function minmaxdist(pointrange::AbstractArray{FT}) where FT<:AbstractFloat
    diff([extrema(pointrange)...])[1] /
        length(pointrange) * (length(pointrange)+1)
end


"""
    stepsize(pointrange::AbstractArray{FT})

Retrieve the average difference between two points of a numeric array,
assuming all points are equally distributed between the extrema of it.
"""
stepsize(pointrange::AbstractArray{FT}) where FT<:AbstractFloat = (
    minmaxdist(pointrange)/length(pointrange))


"""
    intsect_intervals(src_itvs::AT, dest_itv::Interval)

Select intervals from a list of `src_itvs` that intersect with a aimed interval
`dest_itv`.
"""
function intsect_intervals(src_itvs::AbstractArray, dest_itv::Interval)
    # first get width and index for intersecting intervals
    map(
        ((j, itv),) -> 
        let isct = dest_itv ∩ itv
                isempty(isct) ? nothing : [j, width(isct)/width(itv)]
        end, 
        enumerate(src_itvs)) |>
    # filter the nothings
    x -> filter(!isnothing, x) |>
    # adjust the type of the array
    x -> isempty(x) ? (return nothing) : convert(Array{eltype(x).b}, x) |>
    x -> reduce(hcat, x)
end


"""
    extract_cell(ncds::NCDataset, itvs::AbstractArray, itvs_ncds::AbstractArray, variables::AbstractArray{String})

Select cell within NetCDF dataset given intervals `itvs`
and dimension variables `variables`
"""
function extract_cell(ncds::NCDataset, itvs::AbstractArray, itvs_ncds::AbstractArray, variables::AbstractArray{String})
    map(var -> extract_subarray(ncds[var], itvs_ncds, itvs), variables)
end


"""
    extract_subarray(data::NCDatasets.CFVariable, 
        dimension_vectors::AbstractArray, dest_itvs::AbstractArray)

Extract subarray of NetCDF dataset that is stretches over the `dest_itvs`.
The selected dimensions for the destination `dataset` are defined in 
`dimension_vectors`.
"""
function extract_subarray(data::NCDatasets.CFVariable,
        dimension_vectors::AbstractArray, dest_itvs::AbstractArray)
    index_wghts = []
    for (dim_itvs, dest_itv) in zip(dimension_vectors, dest_itvs)
        push!(index_wghts, intsect_intervals(dim_itvs, dest_itv))
    end
    indices = map(j -> convert(Array{Int}, index_wghts[j][1,:]),
            1:length(index_wghts))
    wghts = map(j -> index_wghts[j][2,:], 1:length(index_wghts))

    # the nans of the dataset are converted to zeroes 
    fillnan(data[indices...]), vectors_product(wghts')
end


"""
    regrid_cell(ncds::NCDataset, itvs::AbstractArray, itvs_ncds::AbstractArray, 
            variables::AbstractArray{String}, operation::Function)

Apply an `operation` to regrid cell within NetCDF dataset given intervals `itvs`
and dimension variables `variables`.
"""
function regrid_cell(ncds::NCDataset, itvs::AbstractArray,
        itvs_ncds::AbstractArray, variables::AbstractArray{String},
        operation::Function)
    map(((dt,wt),) -> nm_weighted(dt, wt, operation),
        extract_cell(ncds, itvs, itvs_ncds, variables))
end


"""
    fillnan(numericarray::AbstractArray{NT})

Fill all `NaN`in numeric Array with zeros of the type of the array and
return altered array.
"""
function fillnan(numericarray::AbstractArray{NT}) where NT<:Number
    typezero = convert(eltype(numericarray), 0)
    replace(numericarray, NaN => typezero)
end


"""
    init_regridded(ncdims::Tuple; ft::Type{N}=Float64)

Create a zero filled array with `ndims` dimensions to be
used as a storage for the regridded dataset.
"""
function init_regridded(ncdims::Tuple; ft::Type{N}=Float64) where N<:Number
    zeros(ft, ncdims)
end


"""
    dimwise_intervals(regridder::RG)

Retrieve arrays of intervals for all axes of a `Regridder`.
The output is a dictionary that maps axes name to its 
intervals.
"""
function dimwise_intervals(regridder::RG) where RG<:Regridder
    Dict(x.name => intervals(x) for x in regridder.axes)
end


"""
    nm_weighted(data::AbstractArray, wghts::AbstractArray, operation)

Apply mathematical array operation to `data` array
that accounts for respective weights `wghts` of each
entry inside the array.
"""
function nm_weighted(data::AbstractArray{FT}, wghts::AbstractArray{FT}, operation) where FT<:AbstractFloat
    # to avoid multiple use of marginal extrema, we only use them if more than
    # 50 % lies within grid cell
    if operation ∈ [maximum, minimum]
        let sel_data = data[wghts.>.5]
            isempty(sel_data) ? 0 : operation(sel_data)
        end
    else
        operation(data.*wghts)/sum(wghts)
    end
end


"""
    colrowvector_multiply(vec1, vec2)

Apply multiplication of column (n x 1) and row (1 x m) vector producing
vec1 * vec2 matrix with (n x m).
"""
function colrowvector_multiply(vec1::AbstractArray, vec2::AbstractArray)
    let z=vec1'*vec2
        reshape(z, (1, length(z)))
    end
end

"""
    vectors_product(vectorbases::AbstractArray)

Build tensor of `length(vectorbases)` axes byèlementwise multiplication of all
vectors in `vectorbases` with each other.
"""
function vectors_product(vectorbases::AbstractArray)
    flat_tensor = reduce(colrowvector_multiply, vectorbases)
    reshape(flat_tensor, (length.(vectorbases)...))
end




















