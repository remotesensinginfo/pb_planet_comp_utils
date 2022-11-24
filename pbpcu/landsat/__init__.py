#!/usr/bin/env python

import numpy


def expand_ls_qa_pixel_msks(scn_xa, qa_pxl_msk="QA_PIXEL"):
    scn_lcl_xa = scn_xa.copy()
    unq_img_vals = numpy.unique(numpy.squeeze(scn_xa[qa_pxl_msk].values))

    fill_da = scn_xa[qa_pxl_msk].copy()
    fill_da[...] = 0
    fill_da = fill_da.astype(numpy.uint8)

    dilated_clouds_da = scn_xa[qa_pxl_msk].copy()
    dilated_clouds_da[...] = 0
    dilated_clouds_da = dilated_clouds_da.astype(numpy.uint8)

    cirrus_da = scn_xa[qa_pxl_msk].copy()
    cirrus_da[...] = 0
    cirrus_da = cirrus_da.astype(numpy.uint8)

    clouds_da = scn_xa[qa_pxl_msk].copy()
    clouds_da[...] = 0
    clouds_da = clouds_da.astype(numpy.uint8)

    cloud_shadows_da = scn_xa[qa_pxl_msk].copy()
    cloud_shadows_da[...] = 0
    cloud_shadows_da = cloud_shadows_da.astype(numpy.uint8)

    snow_da = scn_xa[qa_pxl_msk].copy()
    snow_da[...] = 0
    snow_da = snow_da.astype(numpy.uint8)

    clear_da = scn_xa[qa_pxl_msk].copy()
    clear_da[...] = 0
    clear_da = clear_da.astype(numpy.uint8)

    water_da = scn_xa[qa_pxl_msk].copy()
    water_da[...] = 0
    water_da = water_da.astype(numpy.uint8)

    all_clouds_da = scn_xa[qa_pxl_msk].copy()
    all_clouds_da[...] = 0
    all_clouds_da = all_clouds_da.astype(numpy.uint8)

    for val in unq_img_vals:
        val_bin = numpy.flip(
            numpy.unpackbits(numpy.flip(numpy.array([val]).view(numpy.uint8)))
        )

        if val_bin[0] == 1:
            fill_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if val_bin[1] == 1:
            dilated_clouds_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if val_bin[2] == 1:
            cirrus_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if val_bin[3] == 1:
            clouds_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if val_bin[4] == 1:
            cloud_shadows_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if val_bin[5] == 1:
            snow_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if val_bin[6] == 1:
            clear_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if val_bin[7] == 1:
            water_da.values[scn_xa[qa_pxl_msk].values == val] = 1
        if (
            (val_bin[1] == 1)
            or (val_bin[2] == 1)
            or (val_bin[3] == 1)
            or (val_bin[4] == 1)
        ):
            all_clouds_da.values[scn_xa[qa_pxl_msk].values == val] = 1

    scn_lcl_xa["FILL"] = fill_da
    scn_lcl_xa["DILATED_CLOUDS"] = dilated_clouds_da
    scn_lcl_xa["CIRRUS"] = cirrus_da
    scn_lcl_xa["CLOUDS"] = clouds_da
    scn_lcl_xa["CLOUD_SHADOWS"] = cloud_shadows_da
    scn_lcl_xa["SNOW"] = snow_da
    scn_lcl_xa["CLEAR"] = clear_da
    scn_lcl_xa["WATER"] = water_da
    scn_lcl_xa["ALL_CLOUDS"] = all_clouds_da
    return scn_lcl_xa
