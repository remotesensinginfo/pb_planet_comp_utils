#!/usr/bin/env python

import rasterio


def get_img_metadata(img_file):
    img_data_obj = rasterio.open(img_file)
    img_bounds = img_data_obj.bounds
    img_bbox = [img_bounds.left, img_bounds.bottom, img_bounds.right, img_bounds.top]
    img_x_res, img_y_res = img_data_obj.res
    if img_y_res > 0:
        img_y_res = img_y_res * (-1)
    img_data_obj = None
    return img_bbox, img_x_res, img_y_res


def get_img_band_array(img_file, band=1):
    img_data_obj = rasterio.open(img_file)
    img_arr = img_data_obj.read(band)
    img_data_obj = None
    return img_arr
