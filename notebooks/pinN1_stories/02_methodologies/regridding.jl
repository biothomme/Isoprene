using IntervalSets: OpenInterval

const GLAT_MIN, GLAT_MAX = -90., 90.
const GLON_MIN, GLON_MAX = -180., 180.

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

Create a RegridAxis object with flexibility for swapped min and max coordinates.
"""
function RegridAxis(name::String, coordmin::FT, coordmax::FT,
        coordcard::IT) where {IT<:Integer, FT<:AbstractFloat}
    coords = [coordmin, coordmax]
    RegridAxis{IT, FT}(name, minimum(coords), maximum(coords), coordcard)
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
    map(ax -> (OpenInterval(ax-stepsize(rga)/2, ax+stepsize(rga)/2)), range(rga))
end

"""
    Regridder{IT, FT}

Abstract type for tools that allow multidimensional regridding based on 
orthogonal RegridAxis{IT, FT}.
"""
abstract type Regridder{IT<:Integer, FT<:AbstractFloat}
    # regridding is performed on multiple axes
end

Base.size(rg::RG) where RG<:Regridder = tuple(map(length, rg.axes)...)
cardinality(rg::RG) where RG<:Regridder = Dict(ax.name => length(ax) for ax
        in rg.axes)

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



















































