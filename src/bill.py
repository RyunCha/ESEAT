import numpy as np
from src import dao as dao
from src import rate as rate
from src.storage import Storage

def getNCD(st, month):
    # for month in range(1,13):
    return round(st.df.iloc[st.get_idx_by_month(month=month)].max().max(), 0)

def getONPEAK(st, month):
    if np.sum(st.rate_table[month - 1] == 'ONPEAK') < 1:
        return 0

    rowidx = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule < 13)) if value]
    colidx = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'ONPEAK']

    return round(st.df.iloc[rowidx, colidx].max().max(), 0)

def getMIDPEAK(st, month):
    if st.RATE["SEASON"][month - 1] == 'WINTER':
        return 0
    rowidx = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule < 13)) if value]
    colidx = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'MIDPEAK']

    return round(st.df.iloc[rowidx, colidx].max().max(), 0)


def getDemandCharge(st, month):
    s = st.RATE["SEASON"][month-1]

    if s == "SUMMER":
        ONPEAK = st.RATE["DC_ON_S"]
        MIDPEAK = st.RATE["DC_MIDS"]
    else:
        ONPEAK = st.RATE["DC_ON_W"]
        MIDPEAK = st.RATE["DC_MIDW"]

    dc = getNCD(st, month) * st.RATE["FR"] \
        + getONPEAK(st=st, month=month) * ONPEAK \
        + getMIDPEAK(st=st, month=month) * MIDPEAK \

    return dc

def getEnergyCharge(st, month):
    # TODO
    # energy cost is not correct

    if st.RATE["SEASON"][month - 1] == 'WINTER':
        r = np.array([st.RATE["ON_W"], st.RATE["MIDW"], st.RATE["OFFW"]]) + st.RATE["DLV"] - st.RATE["NBC"]
    else:
        r = np.array([st.RATE["ON_S"], st.RATE["MIDS"], st.RATE["OFFS"]]) + st.RATE["DLV"] - st.RATE["NBC"]

    rowidx_weekday = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule < 13)) if value]
    rowidx_weekend = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule == 13)) if value]

    colidx_off = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'OFFPEAK']
    colidx_mid = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'MIDPEAK']
    colidx_on = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'ONPEAK']

    on_energy = st.df.iloc[rowidx_weekday, colidx_on].sum().sum() * 0.25
    mid_energy = st.df.iloc[rowidx_weekday, colidx_mid].sum().sum() * 0.25
    off_energy = st.df.iloc[rowidx_weekday, colidx_off].sum().sum() * 0.25

    weekend_energy = st.df.iloc[rowidx_weekend, [i for i in range(96)]].sum().sum() * 0.25

    energy_use = np.array([on_energy, mid_energy, off_energy + weekend_energy])
    nbc = energy_use.sum() * st.RATE["NBC"]
    ec = (energy_use * r).sum()

    # TODO : rounding
    ec = round(ec)
    nbc = round(nbc)
    return ec, nbc, energy_use


if __name__ == '__main__':
    # df = dao.getRawLoad()
    netdf = dao.getRawNet()
    # st = Storage(df=netdf, RATE=rate.TOU8_OPTION_B)
    st = Storage(df=netdf, RATE=rate.TOU8_OPTION_R)

    for month in range(1,13):
        print("**************************")
        print(month)
        print("NCD", getNCD(st, month))
        print("MIDPEAK", getMIDPEAK(st, month))
        print("ONPEAK", getONPEAK(st, month))
        print("DemandCharge", getDemandCharge(st, month))
        print("EnergyCharge", getEnergyCharge(st, month))
