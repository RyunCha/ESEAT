import numpy as np
from src import dao as dao
from src import rate as rate

import holidays
from datetime import date, datetime


class Storage():
    def __init__(self, df, RATE):
        self.df = df
        self.RATE = RATE
        self.rate_table = get_rate_table(RATE=RATE)
        self.rate_schedule = get_rate_schedule(RATE=RATE, df=df)  # 1~13
        self.list_date = np.array([datetime.strptime(df.index[i], '%m/%d/%Y') for i in range(df.shape[0])])
        self.list_month = np.array([item.month for item in self.list_date])
        self.list_year = np.array([item.year for item in self.list_date])

    def get_idx_by_month_year(self, month, year):
        tmp = (self.list_year == year) * (self.list_month == month)
        return np.array([idx for idx, value in enumerate(tmp) if value])

    def get_idx_by_month(self, month):
        tmp = (self.list_month == month)
        return np.array([idx for idx, value in enumerate(tmp) if value])

    def get_idx_by_month_bizday(self, month):
        tmp = (self.list_month == month) * (self.rate_schedule < 12)
        return np.array([idx for idx, value in enumerate(tmp) if value])

    def get_idx_by_peak_type(self):
        ans = np.array([self.rate_table[int(table_type-1)] for idx, table_type in enumerate(self.rate_schedule)])
        return ans.reshape([-1])

def get_rate_table(RATE):
    schedule = np.array([["OFFPEAK"] * 96] * 13)
    for tgtMonth in range(0, 12):
        # SUMMER
        if tgtMonth in np.array(np.where(np.array(RATE['SEASON']) == 'SUMMER')):
            # 8:00 am to Noon and 6:00 pm to 11:00 pm
            for i in range(32, 92):
                schedule[tgtMonth][i] = "MIDPEAK"
            # Noon to 6:00 pm
            for i in range(48, 72):
                schedule[tgtMonth][i] = "ONPEAK"
        # WINTER
        else:
            # 8:00 am to 9:00 pm
            for i in range(32, 84):
                schedule[tgtMonth][i] = "MIDPEAK"
    return schedule


def get_rate_schedule(RATE, df):
    list_holiday = holidays.US(state='CA')

    list_date = [datetime.strptime(df.index[i], '%m/%d/%Y') for i in range(df.shape[0])]
    ans = np.zeros(len(list_date))

    for idx in range(len(list_date)):
        # TODO : ETB 는 holiday를 bizday로 계산
        # is_holiday = list_holiday.get(list_date[idx].date()) in RATE['HOLIDAY']
        # if is_holiday or (list_date[idx].weekday() > 4):
        if list_date[idx].weekday() > 4:
            ans[idx] = 13
        else:
            ans[idx] = list_date[idx].month
    return ans

if __name__ == '__main__':
    df = dao.getRawLoad()
    st = Storage(df=df, RATE=rate.TOU8_OPTION_B)
    print("Storage.py demo done")



