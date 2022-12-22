#!/usr/bin/env python

import rasterio
import urllib.request
import urllib.error
import time


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


def test_asset_urls(signed_items):
    chkd_items = list()
    for scn_item in signed_items:
        assets_present = True
        for asset_name in scn_item.assets:
            try:
                if (
                    urllib.request.urlopen(scn_item.assets[asset_name].href).getcode()
                    != 200
                ):
                    assets_present = False
                    break
            except urllib.error.HTTPError:
                assets_present = False
                break
            time.sleep(0.1)
        if assets_present:
            chkd_items.append(scn_item)
    print(f"Before: {len(signed_items)}")
    print(f"After: {len(chkd_items)}")
    return chkd_items
