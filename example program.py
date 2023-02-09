# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 10)

import os.path
import sys
sys.path.append('C:/Users/yth69564/OneDrive - Science and Technology Facilities Council/Documents/Alexinfo/working_scripts')
#print(sys.path)
from CSB1 import *

testrun()




ceriadat = identifyexperiments()
getprefix(ceriadat)



i=50
expnumber = 25226
totalmin = 1
totalmax=2400
generalname='spc'
parts=10


#loadfromexn(expnumber,totalmin,totalmax,'spc1',ceriadat)
itrload(expnumber,totalmin,totalmax,generalname,parts,ceriadat,i)


length =5.41
peakposition,max3 = bcctheo(length)



n=0
for n in range(parts):
    m = n+1
    name = generalname+str(m)
    csf(name)
    (data,x0data,x0vals,x0max)=readexperiment(m) #Fulldf,x0df,x0vals,x0len
    #print(x0max,'x0max')

    #peakposition=peakposition[1:]
    #print(x0vals)
    offsetchart(x0vals,x0max,max3,peakposition)

