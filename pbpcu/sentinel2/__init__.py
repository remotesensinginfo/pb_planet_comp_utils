#!/usr/bin/env python

import numpy
import xarray


def apply_sen2_vld_msk(scns_xa, bands, qa_pxl_msk="SCL", out_no_data_val=0):
    scns_lcl_xa = scns_xa.copy()
    for band in bands:
        scns_lcl_xa[band].values[
            scns_lcl_xa[qa_pxl_msk].values == 0
        ] = out_no_data_val  # No Data
        scns_lcl_xa[band].values[
            scns_lcl_xa[qa_pxl_msk].values == 1
        ] = out_no_data_val  # Saturation
        scns_lcl_xa[band].values[
            scns_lcl_xa[qa_pxl_msk].values == 2
        ] = out_no_data_val  # Cast Shadow
        scns_lcl_xa[band].values[
            scns_lcl_xa[qa_pxl_msk].values == 3
        ] = out_no_data_val  # Cloud Shadows
        scns_lcl_xa[band].values[
            scns_lcl_xa[qa_pxl_msk].values == 8
        ] = out_no_data_val  # Cloud Medium Probability
        scns_lcl_xa[band].values[
            scns_lcl_xa[qa_pxl_msk].values == 9
        ] = out_no_data_val  # Cloud High Probability
        scns_lcl_xa[band].values[
            scns_lcl_xa[qa_pxl_msk].values == 10
        ] = out_no_data_val  # Thin Cirrus
    return scns_lcl_xa


def apply_sen2_offset(sen2_scns_xa, offset=-1000):

    # Define the date splitting whether the offset should be applied.
    off_date = numpy.datetime64("2022-01-25")
    # Get Minimum date in timeseries
    time_min = sen2_scns_xa.time.min().values
    # Get Maximum date in timeseries
    time_max = sen2_scns_xa.time.max().values

    # Get the list of variables
    bands = list(sen2_scns_xa.data_vars)
    # List of all bands for which offset should be applied if present.
    s2_img_bands = [
        "B01",
        "B02",
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B8A",
        "B09",
        "B10",
        "B11",
        "B12",
    ]

    if (time_min < off_date) and (time_max > off_date):
        # Crosses the offset data and therefore part of the dataset needs offset applying
        sen2_scns_xa_pre_off = sen2_scns_xa.sel(time=slice(time_min, off_date))
        sen2_scns_xa_post_off = sen2_scns_xa.sel(time=slice(off_date, time_max))
        for band in bands:
            if band in s2_img_bands:
                sen2_scns_xa_post_off[band] = sen2_scns_xa_post_off[band] + offset
                sen2_scns_xa_post_off[band].where(sen2_scns_xa_post_off[band] < 0, 0)
                sen2_scns_xa_post_off[band].where(
                    sen2_scns_xa_post_off[band] > 10000, 0
                )
        sen2_scns_xa = xarray.concat(
            [sen2_scns_xa_pre_off, sen2_scns_xa_post_off], dim="time"
        )
    elif time_min > off_date:
        # All scenes after offset date apply to all
        for band in bands:
            if band in s2_img_bands:
                sen2_scns_xa[band] = sen2_scns_xa[band] + offset
                sen2_scns_xa[band].where(sen2_scns_xa[band] < 0, 0)
                sen2_scns_xa[band].where(sen2_scns_xa[band] > 10000, 0)
    # else: time_max < off_date:
    # Do nothing - no offset required
    return sen2_scns_xa
