#!/usr/bin/env python

from typing import Union
import numpy
import xarray


def sklearn_flatten_df(
    input_xr: Union[xarray.Dataset, xarray.DataArray]
) -> numpy.array:
    """
    A function which reshapes an xarray Dataset or DataArray with spatial and
    optionally temporal indexes into a numpy.array with the spatial and temporal
    dimensions flattened into one dimension. This allows the input data to be
    used within the scikit-learn.

    This function is edited from the dea_tools module.

    :param input_xr: xarray.Dataset or xarray.DataArray that must have dimensions
                     'x' and 'y' or 'latitude' and 'longitude', may have dimension
                     'time'. Dimensions other than 'x', 'y' or 'latitude' and
                     'longitude' and 'time' are unaffected by the flattening.
    :return: A numpy array corresponding with dimensions 'x', 'y', 'latitude',
             'longitude' and 'time' flattened into a single dimension, which is
             the first axis of the returned array.

    """
    # Cast input Datasets to DataArray
    if isinstance(input_xr, xarray.Dataset):
        input_xr = input_xr.to_array()

    proj_dims = True
    if "latitude" in input_xr.dims:
        proj_dims = False

    if proj_dims:
        if not (("x" in input_xr.dims) and ("y" in input_xr.dims)):
            raise Exception(
                "If input has projected spatial index then x and y must be provided"
            )
    else:
        if not (("latitude" in input_xr.dims) and ("longitude" in input_xr.dims)):
            raise Exception(
                "If input is not a projected spatial index "
                "then latitude and longitude must be provided"
            )

    # Stack across pixel dimensions, handling time series if necessary
    if "time" in input_xr.dims:
        if proj_dims:
            stacked = input_xr.stack(z=["x", "y", "time"])
        else:
            stacked = input_xr.stack(z=["longitude", "latitude", "time"])
    else:
        if proj_dims:
            stacked = input_xr.stack(z=["x", "y"])
        else:
            stacked = input_xr.stack(z=["longitude", "latitude"])

    # Finding 'bands' dimensions in each pixel - these will not be
    # flattened as their context is important for sklearn
    pxdims = []
    for dim in stacked.dims:
        if dim != "z":
            pxdims.append(dim)

    # Mask NaNs - mask pixels with NaNs in *any* band, as sklearn cannot
    # accept NaNs as input
    mask = numpy.isnan(stacked)
    if len(pxdims) != 0:
        mask = mask.any(dim=pxdims)

    # Turn the mask into a numpy array (boolean indexing with xarrays acts weird)
    mask = mask.data

    # The dimension we are masking along ('z') needs to be the first
    # dimension in the underlying numpy array for the boolean indexing to work
    stacked = stacked.transpose("z", *pxdims)
    input_np = stacked.data[~mask]

    return input_np


def sklearn_unflatten_np(
    input_np: numpy.array, ref_xr: Union[xarray.Dataset, xarray.DataArray]
) -> xarray.DataArray:
    """
    A function which reshapes a numpy array into to xarray DataArray with spatial and
    optionally temporal indexes. The input numpy array should have missing elements
    where NaN values are presented within the reference xarray Dataset/DataArray.
    This allows outputs from a scikit-learn model to be remapped to pixels.

    This function is edited from the dea_tools module.

    :param input_np: numpy.array where the first dimension's length should correspond
                     to the number of valid (non-NaN) pixels in ref_xr.
    :param ref_xr: xarray.Dataset or xarray.DataArray that must have dimensions
                   'x' and 'y' or 'latitude' and 'longitude', may have dimension
                   'time'. Dimensions other than 'x', 'y' or 'latitude' and
                   'longitude' and 'time' are unaffected by the flattening. This
                   array is used as a reference for the output size of the
                   xarray.DataArray
    :return: An xarray.DataArray with the same dimensions 'x', 'y' or 'latitude'
             and 'longitude' and 'time' as ref_xr, and the same valid (non-NaN)
             pixels. These pixels are set to match the data in input_np.

    """
    # The output of a sklearn model prediction should just be a numpy array
    # with size matching x*y*time for the input DataArray/Dataset.

    # cast input Datasets to DataArray
    if isinstance(ref_xr, xarray.Dataset):
        ref_xr = ref_xr.to_array()

    proj_dims = True
    if "latitude" in ref_xr.dims:
        proj_dims = False

    if proj_dims:
        if not (("x" in ref_xr.dims) and ("y" in ref_xr.dims)):
            raise Exception(
                "If input has projected spatial index then x and y must be provided"
            )
    else:
        if not (("latitude" in ref_xr.dims) and ("longitude" in ref_xr.dims)):
            raise Exception(
                "If input is not a projected spatial index then "
                "latitude and longitude must be provided"
            )

    # Stack across pixel dimensions, handling time series if necessary
    if "time" in ref_xr.dims:
        if proj_dims:
            stacked = ref_xr.stack(z=["x", "y", "time"])
        else:
            stacked = ref_xr.stack(z=["longitude", "latitude", "time"])
    else:
        if proj_dims:
            stacked = ref_xr.stack(z=["x", "y"])
        else:
            stacked = ref_xr.stack(z=["longitude", "latitude"])

    pxdims = []
    for dim in stacked.dims:
        if dim != "z":
            pxdims.append(dim)

    mask = numpy.isnan(stacked)
    if len(pxdims) != 0:
        mask = mask.any(dim=pxdims)

    # Handle multivariable output
    output_px_shape = ()
    if len(input_np.shape[1:]):
        output_px_shape = input_np.shape[1:]

    # use the mask to put the data in all the right places
    output_ma = numpy.ma.empty((len(stacked.z), *output_px_shape))
    output_ma[~mask] = input_np
    output_ma[mask] = numpy.ma.masked

    # set the stacked coordinate to match the input
    output_xr = xarray.DataArray(
        output_ma,
        coords={"z": stacked["z"]},
        dims=["z", *["output_dim_" + str(idx) for idx in range(len(output_px_shape))]],
    )
    output_xr = output_xr.unstack()

    return output_xr
