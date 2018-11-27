import numpy as np
from src import dao as dao
from src import rate as rate
from src.storage import Storage

import holidays
from datetime import date, datetime

df = dao.getRawLoad()
st = Storage(df=df, RATE=rate.TOU8_OPTION_B)

def getNCD(st, month):
    # for month in range(1,13):
    return round(st.df.iloc[st.get_idx_by_month(month=month)].max().max(), 0)

def getONPEAK(st, month):
    if np.sum(st.rate_table[month - 1] == 'ONPEAK') < 1:
        return 0

    rowidx = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule < 13)) if value]
    colidx = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'ONPEAK']

    return round(df.iloc[rowidx, colidx].max().max(), 0)

def getMIDPEAK(st, month):
    if st.RATE["SEASON"][month - 1] == 'WINTER':
        return 0
    rowidx = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule < 13)) if value]
    colidx = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'MIDPEAK']

    return round(df.iloc[rowidx, colidx].max().max(), 0)


def getDemandCharge(st, month):
    s = st.RATE["SEASON"][month-1]

    if s == "SUMMER":
        ONPEAK = st.RATE["DC_ON_S"]
        MIDPEAK = st.RATE["DC_MIDS"]
    else:
        ONPEAK = st.RATE["DC_ON_W"]
        MIDPEAK = st.RATE["DC_MIDW"]

    dc = getNCD(st, month) * rate.TOU8_OPTION_B["FR"] \
        + getONPEAK(st=st, month=month) * ONPEAK \
        + getMIDPEAK(st=st, month=month) * MIDPEAK \

    return dc

def getEnergyCharge(st, month):
    if st.RATE["SEASON"][month - 1] == 'WINTER':
        [on_rate, mid_rate, off_rate] = [st.RATE["ON_W"], st.RATE["MIDW"], st.RATE["OFFW"]]
    else:
        [on_rate, mid_rate, off_rate] = [st.RATE["ON_S"], st.RATE["MIDS"], st.RATE["OFFS"]]

    rowidx_weekday = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule < 13)) if value]
    rowidx_weekend = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule == 13)) if value]

    colidx_off = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'OFFPEAK']
    colidx_mid = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'MIDPEAK']
    colidx_on = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'ONPEAK']

    ec_on = st.df.iloc[rowidx_weekday, colidx_on].sum().sum() * on_rate * 0.25  # kW-15min to kWh
    ec_mid = st.df.iloc[rowidx_weekday, colidx_mid].sum().sum() * mid_rate * 0.25  # kW-15min to kWh
    ec_off = st.df.iloc[rowidx_weekday, colidx_off].sum().sum() * off_rate * 0.25  # kW-15min to kWh

    ec_weekend = st.df.iloc[rowidx_weekend, [i for i in range(96)]].sum().sum() * off_rate * 0.25  # kW-15min to kWh

    return ec_off, ec_mid, ec_on, ec_weekend, (ec_mid + ec_off + ec_on + ec_weekend)

if __name__ == '__main__':
    month = 1
    for month in range(1,13):
    # k = st.df.iloc[st.get_idx_by_month_bizday(month=month)]

        print("**************************")
        print(month)
        print("NCD", getNCD(st, month))
        print("ONPEAK", getONPEAK(st, month))
        print("MIDPEAK", getMIDPEAK(st, month))
        print("DemandCharge", getDemandCharge(st, month))
        print("EnergyCharge", getEnergyCharge(st, month))
