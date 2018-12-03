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

def get_NBC_EnergyCharge(st, month):

    if st.RATE["SEASON"][month - 1] == 'WINTER':
        r = np.array([st.RATE["ON_W"], st.RATE["MIDW"], st.RATE["OFFW"]]) + st.RATE["DLV"] - st.RATE["NBC"]
    else:
        r = np.array([st.RATE["ON_S"], st.RATE["MIDS"], st.RATE["OFFS"]]) + st.RATE["DLV"] - st.RATE["NBC"]

    rowidx = [idx for idx, value in enumerate(st.list_month == month) if value]
    rowidx_weekday = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule < 13)) if value]
    rowidx_weekend = [idx for idx, value in enumerate((st.list_month == month) * (st.rate_schedule == 13)) if value]

    colidx = [i for i in range(96)]
    colidx_off = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'OFFPEAK']
    colidx_mid = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'MIDPEAK']
    colidx_on = [idx for idx, value in enumerate(st.rate_table[month - 1]) if value == 'ONPEAK']

    on_energy = st.df.iloc[rowidx_weekday, colidx_on].sum().sum() * 0.25
    mid_energy = st.df.iloc[rowidx_weekday, colidx_mid].sum().sum() * 0.25
    off_energy = st.df.iloc[rowidx_weekday, colidx_off].sum().sum() * 0.25
    weekend_energy = st.df.iloc[rowidx_weekend, colidx].sum().sum() * 0.25

    # NEM 2.0 using 15min NEM, maybe using 1Hour
    tmp = np.array(st.df.iloc[rowidx, colidx])
    over_energy = (tmp * (tmp < 0)).sum().sum() * 0.25
    # if using 1Hour like residential, then ...
    # tmp = np.array(st.df.iloc[rowidx, colidx]).reshape([-1,4]).sum(axis=1)
    # over_energy = (tmp * (tmp < 0)).sum().sum() * 0.25

    energy_use = np.array([on_energy, mid_energy, off_energy + weekend_energy])
    nbc = (energy_use.sum() - over_energy) * st.RATE["NBC"]
    ec = (energy_use * r).sum()

    # TODO : maybe unnecessary rounding
    # ec = round(ec)
    # nbc = round(nbc)
    return ec, nbc #, energy_use, over_energy


def getMontlyTotalCharge(st,month):
    return sum([st.RATE["CC"] + sum(get_NBC_EnergyCharge())])

if __name__ == '__main__':
    year = 0
    elec_increase = 1.037
    df = dao.getRawLoad() * pow(elec_increase, year)
    pv = dao.getRawPV()
    netdf = dao.getRawNet()
    st = Storage(df=df, RATE=rate.TOU8_OPTION_B)
    # st = Storage(df=netdf, RATE=rate.TOU8_OPTION_R)

    total_charges = 0
    for month in range(1,13):
        print("**************************")
        print(month)
        print("NCD, MID, ON", getNCD(st, month), getMIDPEAK(st, month), getONPEAK(st, month))
        dc = getDemandCharge(st, month)
        print("DemandCharge", dc)
        nbc_ec = sum(get_NBC_EnergyCharge(st, month))
        print("NBC and EnergyCharge", nbc_ec)
        total_charges += dc + nbc_ec + st.RATE["CC"]

    print("**************************")
    print("TOTAL YEARLY CHARGE")
    print(total_charges)