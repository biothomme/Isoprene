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
        println(dim_itvs, dest_itv)
        push!(index_wghts, intsect_intervals(dim_itvs, dest_itv))
    end
    println(index_wghts)
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
    Dict(x.name => intervals(x) for x in values(regridder.axes))
end


"""
    nm_weighted(data::AbstractArray, wghts::AbstractArray, operation)

Apply mathematical array operation to `data` array
that accounts for respective weights `wghts` of each
entry inside the array.
"""
function nm_weighted(data::AbstractArray{FT}, wghts::AbstractArray{FT}, operation) where FT<:AbstractFloat
    # for minimum and maximum we do not use weights
    if operation ∈ [maximum, minimum]
        operation(data)
    else
        operation(data, weights(wghts))
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

"""
    deepcopy(rga::RegridAxis) -> RegridAxis

Make deep copy if `RegridAxis`.
"""
function Base.deepcopy(rga::RegridAxis)
    RegridAxis(rga.name, rga.coordmin, rga.coordmax, rga.coordcard)
end

"""
    deepcopy(rgd::Regridder) -> Any

Make deep copy if `Regridder` subtype.
"""
function Base.deepcopy(rgd::RG) where RG<:Regridder
    newaxes = map(deepcopy, rgd.axes)
    Regridder(newaxes)
end

"""
    alter_regridder3D(rgd::RG; latcard, loncard, indcard, latmin,
        latmax, latname, lonmin, lonmax, lonname, indmax, indmin,
        indname)

Make an altered deeep copy of a `Regridder3D` instance.
"""
function alter_regridder3D(rgd::RG; latcard=nothing, loncard=nothing, indcard=nothing, latmin=nothing,
        latmax=nothing, latname=nothing, lonmin=nothing,
        lonmax=nothing, lonname=nothing, indmax=nothing,
        indmin=nothing, indname=nothing) where RG<:Regridder
    
    # fill missing args from input regridder
    function fillfromregridder!(rgdder, axdict, axname, newdict)
        ax = rgdder.axes[axname]
        newaxdict = Dict()
        newaxdict["card"] = axdict["card"]===nothing ? ax.coordcard : axdict["card"]
        newaxdict["min"] = axdict["min"]===nothing ? ax.coordmin : axdict["min"]
        newaxdict["max"] = axdict["max"]===nothing ? ax.coordmax : axdict["max"]
        newaxdict["name"] = axdict["name"]===nothing ? ax.name : axdict["name"]
        newdict[axname] = newaxdict
    end 
    
    # convert all numbers to same types
    function promoteall!(fullaxesdict, defaultcard, defaultcoord)
        fullaxesdict["min"] = convert(defaultcoord, fullaxesdict["min"])
        fullaxesdict["max"] = convert(defaultcoord, fullaxesdict["max"])

        fullaxesdict["card"] = convert(defaultcard, fullaxesdict["card"])
    end
    
    axesvarsplit = Dict("lat" => Dict("card"=>latcard, "min"=>latmin, "max"=>latmax, "name"=>latname),
                        "lon" => Dict("card"=>loncard, "min"=>lonmin, "max"=>lonmax, "name"=>lonname),
                        "ind" => Dict("card"=>indcard, "min"=>indmin, "max"=>indmax, "name"=>indname))
    newaxesvarsplit = Dict()

    kys = collect(keys(axesvarsplit))
    map(x -> fillfromregridder!(rgd, axesvarsplit[x], x, newaxesvarsplit), kys)

    card_default = typeof(newaxesvarsplit["lat"]["card"])
    coord_default = typeof(newaxesvarsplit["lat"]["max"])
    map(x -> promoteall!(newaxesvarsplit[x], card_default, coord_default), kys)
    latdict, londict, inddict = newaxesvarsplit["lat"], newaxesvarsplit["lon"], newaxesvarsplit["ind"]
    Regridder3D(latdict["card"], londict["card"], inddict["card"]; 
        latmin=latdict["min"], latmax=latdict["max"], latname=latdict["name"], 
        lonmin=londict["min"], lonmax=londict["max"], lonname=londict["name"],
        indmin=inddict["min"], indmax=inddict["max"], indname=inddict["name"])
end