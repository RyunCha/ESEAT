import numpy as np
from src import dao as dao
from src import rate as rate
from src.storage import Storage
from src.preproc import preproc_peaktype, preproc_df, preproc_cost, preproc_demand_rate_m



if __name__ == '__main__':
    load = dao.getRawLoad()
    pv = dao.getRawPV()
    es = dao.getRawES()
    net = dao.getRawNet()

    # for test
    # load = dao.getRawLoad().drop(load.index[[i for i in range(31, 365)]])
    # pv = dao.getRawPV().drop(pv.index[[i for i in range(31, 365)]])
    # es = dao.getRawES().drop(es.index[[i for i in range(31, 365)]])
    # net = dao.getRawNet().drop(net.index[[i for i in range(31, 365)]])

    st = Storage(df=load, RATE=rate.TOU8_OPTION_R)
    cost_t = preproc_cost(st)
    load_t = preproc_df(load)
    pv_t = preproc_df(pv)

    r_nbc = st.RATE["NBC"]

    r_on_m = preproc_demand_rate_m(st, "ONPEAK")
    r_mid_m = preproc_demand_rate_m(st, "MIDPEAK")
    r_off_m = preproc_demand_rate_m(st, "OFFPEAK")

    c_whole = 0.05
    PCS_max = 500.0
    CAP_ESS = 1000.0
    SOC_min = 0.0
    SOC_max = 100.0
    CC = st.RATE["CC"]

    ef_c = 0.96
    ef_d = 0.96

    # do smth with pyomo