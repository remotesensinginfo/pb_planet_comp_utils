#!/usr/bin/env python

import numpy

def find_month_end_date(year, month):
    import calendar
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    max_day_month = numpy.array(month_days).flatten().max()
    return max_day_month

def zero_pad_num_str(
    num_val: float,
    str_len: int = 3,
    round_num: bool = False,
    round_n_digts: int = 0,
    integerise: bool = False,
    absolute: bool = False,
    gain: float = 1,
) -> str:
    if absolute:
        num_val = abs(num_val)
    if round_num:
        num_val = round(num_val, round_n_digts)
    if integerise:
        num_val = int(num_val * gain)

    num_str = "{}".format(num_val)
    num_str = num_str.zfill(str_len)
    return num_str