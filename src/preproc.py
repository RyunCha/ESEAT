import numpy as np

def preproc_peaktype(peaktype_list_by_month, strPeakType):
    peaktype_list = peaktype_list_by_month.reshape([-1])
    # strPeakType = "ONPEAK", "MIDPEAK", "OFFPEAK"
    return np.array([idx for idx, value in enumerate(peaktype_list) if value == strPeakType])

def preproc_df(df):
    return np.array(df).reshape([-1])

def preproc_cost(st):
    # date count == len(rate_schedule)
    ans = [0] * len(st.rate_schedule)

    for idx, rs in enumerate(st.rate_schedule):
        month = int(rs - 1)  # 1~13 -> 0~12
        if month > 11:
            r = np.array([st.RATE["DC_ON_W"], st.RATE["DC_MIDW"], st.RATE["FR"]])
        elif st.RATE["SEASON"][month] == 'WINTER':
            r = np.array([st.RATE["ON_W"], st.RATE["MIDW"], st.RATE["OFFW"]]) + st.RATE["DLV"] - st.RATE["NBC"]
        else:
            r = np.array([st.RATE["ON_S"], st.RATE["MIDS"], st.RATE["OFFS"]]) + st.RATE["DLV"] - st.RATE["NBC"]

        ans[idx] = np.array(st.rate_table[month] == "ONPEAK") * r[0] \
                + np.array(st.rate_table[month] == "MIDPEAK") * r[1] \
                + np.array(st.rate_table[month] == "OFFPEAK") * r[2]
    return np.array(ans).reshape([-1])

def preproc_demand_rate_m(st, strPeakType):
    # strPeakType = "ONPEAK", "MIDPEAK", "OFFPEAK"
    # date count == len(rate_schedule)
    ans = [0] * len(st.rate_schedule)
    for idx, rs in enumerate(st.rate_schedule):
        # month = int(st.list_month[idx] - 1)  #
        month = int(rs - 1) # 1~13 -> 0~12
        if month > 11:
            r = np.array([st.RATE["DC_ON_W"], st.RATE["DC_MIDW"], st.RATE["FR"]])
        elif st.RATE["SEASON"][month] == 'WINTER':
            r = np.array([st.RATE["DC_ON_W"], st.RATE["DC_MIDW"], st.RATE["FR"]])
        else:
            r = np.array([st.RATE["DC_ON_S"], st.RATE["DC_MIDS"], st.RATE["FR"]])

        if strPeakType == "ONPEAK":
            ridx = 0
        elif strPeakType == "MIDPEAK":
            ridx = 1
        else:
            ridx = 2  # OFFPEAK

        ans[idx] = r[ridx]
    return np.array(ans)

def preproc_demand_rate_t(st, strPeakType):
    # strPeakType = "ONPEAK", "MIDPEAK", "OFFPEAK"
    # date count == len(rate_schedule)
    ans = [0] * len(st.rate_schedule)
    for idx, rs in enumerate(st.rate_schedule):
        month = st.list_month[idx]
        if st.RATE["SEASON"][month] == 'WINTER':
            r = np.array([st.RATE["DC_ON_W"], st.RATE["DC_MIDW"], st.RATE["FR"]])
        else:
            r = np.array([st.RATE["DC_ON_S"], st.RATE["DC_MIDS"], st.RATE["FR"]])

        if strPeakType == "ONPEAK":
            ridx = 0
        elif strPeakType == "MIDPEAK":
            ridx = 1
        else:
            ridx = 2  # OFFPEAK

        ans[idx] = np.array(st.rate_table[month] == "strPeakType") * r[ridx]
    return np.array(ans).reshape([-1])