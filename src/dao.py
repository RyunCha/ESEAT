import pandas as pd
import numpy as np

load = pd.read_csv("../raw/CurrentUsage.csv")
pv = pd.read_csv("../raw/EnergyStoragePerformance.csv")
es = pd.read_csv("../raw/SolarPVGeneration.csv")
net = pd.read_csv("../raw/NetUsage.csv")



