#-*- coding:utf-8 -*-
# Author : Jiwon Cha
# Date : 2018.11.26.
# Contact : jwcha@gridwiz.com
# Purpose : Energy Toolbase Raw Data 불러오기

import pandas as pd
from datetime import datetime


def refineRawData(df):
    """
    Energy Toolbase에서 출력한 데이터 형식을 약간 손봐서 DF에 맞게끔 수정
    :param df: type (pandas DataFrame)
    :return: type (pandas DataFrame)
    """
    colnames = df.columns
    ans = df.drop(columns=[df.columns[-1]], axis=1)
    ans.columns = \
    ['12:00 AM', '12:15 AM', '12:30 AM', '12:45 AM', '1:00 AM', '1:15 AM', '1:30 AM', '1:45 AM', '2:00 AM', '2:15 AM',
     '2:30 AM', '2:45 AM', '3:00 AM', '3:15 AM', '3:30 AM', '3:45 AM', '4:00 AM', '4:15 AM', '4:30 AM', '4:45 AM',
     '5:00 AM', '5:15 AM', '5:30 AM', '5:45 AM', '6:00 AM', '6:15 AM', '6:30 AM', '6:45 AM', '7:00 AM', '7:15 AM',
     '7:30 AM', '7:45 AM', '8:00 AM', '8:15 AM', '8:30 AM', '8:45 AM', '9:00 AM', '9:15 AM', '9:30 AM', '9:45 AM',
     '10:00 AM', '10:15 AM', '10:30 AM', '10:45 AM', '11:00 AM', '11:15 AM', '11:30 AM', '11:45 AM',
     '12:00 PM', '12:15 PM', '12:30 PM', '12:45 PM', '1:00 PM', '1:15 PM', '1:30 PM', '1:45 PM', '2:00 PM',
     '2:15 PM', '2:30 PM', '2:45 PM', '3:00 PM', '3:15 PM', '3:30 PM', '3:45 PM', '4:00 PM', '4:15 PM',
     '4:30 PM', '4:45 PM', '5:00 PM', '5:15 PM', '5:30 PM', '5:45 PM', '6:00 PM', '6:15 PM', '6:30 PM',
     '6:45 PM', '7:00 PM', '7:15 PM', '7:30 PM', '7:45 PM', '8:00 PM', '8:15 PM', '8:30 PM', '8:45 PM',
     '9:00 PM', '9:15 PM', '9:30 PM', '9:45 PM', '10:00 PM', '10:15 PM', '10:30 PM', '10:45 PM', '11:00 PM',
     '11:15 PM', '11:30 PM', '11:45 PM']
    return ans

def addWeekday(df):
    """
    Add Weekday Column (Monday = 0)
    :param df: type (pandas DataFrame) shape 365 x 96
    :return: type (pandas DataFrame) shape 365 x 97
    """
    df["Weekday"] = [datetime.strptime(df.index[i], '%m/%d/%Y').weekday() \
                     for i in range(df.shape[0])]
    return df


def getRawLoad():
    """
    Raw CSV file needed
    Metering Time means Starting time
    :return:
    """
    # return addWeekday(refineRawData(pd.read_csv("../raw/CurrentUsage.csv")))
    return refineRawData(pd.read_csv("../raw/CurrentUsage.csv"))

def getRawPV():
    # return addWeekday(refineRawData(pd.read_csv("../raw/EnergyStoragePerformance.csv")))
    return refineRawData(pd.read_csv("../raw/EnergyStoragePerformance.csv"))


def getRawES():
    # return addWeekday(refineRawData(pd.read_csv("../raw/SolarPVGeneration.csv")))
    return refineRawData(pd.read_csv("../raw/SolarPVGeneration.csv"))

def getRawNet():
    # return addWeekday(refineRawData(pd.read_csv("../raw/NetUsage.csv")))
    return refineRawData(pd.read_csv("../raw/NetUsage.csv"))

# if __name__ == '__main__':
#     load = refineRawData(pd.read_csv("../raw/CurrentUsage.csv"))
#     pv = refineRawData(pd.read_csv("../raw/EnergyStoragePerformance.csv"))
#     es = refineRawData(pd.read_csv("../raw/SolarPVGeneration.csv"))
#     net = refineRawData(pd.read_csv("../raw/NetUsage.csv"))
