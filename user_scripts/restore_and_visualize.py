import sys
sys.path.append("..")
from mca.mca import *

import pickle

f = open("mca.pickle", 'rb')
m = pickle.load(f)
f.close()

m.plot()