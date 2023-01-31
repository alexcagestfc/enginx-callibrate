# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns',20)
import glob
from datetime import datetime



"""
user derfined function 1: loads experiment from 5 digit number  
"""
def loadfromexn(expnumber,min,max,name):
    exp = ('ENG'+str(expnumber))
    #print(exp)

    row1 = recent[recent['Number'].str.contains(exp)]
    pref=row1['prefixes']
    filename = ('ENGINX'+pref+str(expnumber)+'.RAW')
    filename = (str(filename))
    filename= filename[10:28]
     
    pref = (str(pref))
    pref= pref[10:13]
    #print(pref)
    if pref !=999:
        cyc= 0
        
        filename = ('ENGINX'+pref+str(expnumber)+'.RAW')
        filename = (str(filename))
        filename= filename#[0:28]
        print(filename)
        Load(filename, OutputWorkspace=name,SpectrumMin=min, SpectrumMax=max)
"""
function 2: gets experiment with the ith largerst data set from the n most recent:
"""
def loadfromrecent(i,n,min,max,name):
    recent = (ceriadat.tail(n))
    recent['secs'] = recent['secs'].astype(float)
    i=i-1

    recent = recent.sort_values(['secs'],ascending=False)
    #print(recent)
    row1=recent.iloc[i]
    expname=row1['Number']
    expnumber = (expname[3:8])
    pref=row1['prefixes']
    filename = ('ENGINX'+pref+str(expnumber)+'.RAW')
    filename = (str(filename))
    filename= filename[10:28]
     
    #pref = (str(pref))
    #pref= pref[10:13]
    print(pref)
    if pref !=999:
        cyc= 0
        
        filename = ('ENGINX'+pref+str(expnumber)+'.RAW')
        filename = (str(filename))
        filename= filename#[0:28]
        print(filename)
        Load(filename, OutputWorkspace=name,SpectrumMin=min, SpectrumMax=max)
"""
user defined fuction 3: iterative loading
"""
def itrload(expnumber,totalmin,totalmax,generalname,parts):
    b=0
    partmax=[]
    for b in range(parts):
        c=b+1
        spacing=totalmax/parts
        max=((spacing) *(c))
        min=(spacing*b)+1
        min=int(min)
        print(min)
        max=int(max)
        print(max)
        name=(generalname+str(c))
        loadfromexn(expnumber,min,max,name)


"""
how to use:
this program will take an input of an experimental number and output a loaded file
it will also find the relevant experiments and list them so you can select the ideal experiment
"""

"""
this section locates ceria experiments
their info is stored on a dataframe called ceriadat
"""
ceriadat = []

def identifyexperiments():
    col_names = ['Number','Object','date','time','secs','experiment']
    col_width = [(0,28),(28,52),(52,63),(63,72),(72,80),(80,88)]
    data = pd.read_fwf('C:\SUMMARY.TXT',names = col_names, colspecs = col_width, na_filter = False, encoding = 'cp1252')
    df = pd.DataFrame(data)
    ceriadat = df[df['Object'].str.contains('ceo2|CeO2|CEO2|ceria|Ceria')]
    return ceriadat
ceriadat = identifyexperiments()

"""
the file naming convention changes slightly throughout the list, the following adjusts for that
"""
date_aframe = ceriadat['date']

rows = len(date_aframe)
i=1
date1 = datetime(2008,1,1)
date2 = datetime(2013,2,27)
date3 = datetime(2018,11,24)
n=[]

for i in range(rows):
    date = datetime.strptime(date_aframe.iloc[i],'%d-%b-%Y')
    
    if date < date1:
        prefix='999'
        n.append(prefix)
    if date1<date and date<date2:
        prefix='001'
        n.append(prefix)

    if date2<date and date<date3:
        prefix='002'
        n.append(prefix)
    if date3<date:
        prefix='003'
        n.append(prefix)
    i=i+1
ceriadat['prefixes'] = n

"""
select experiment number below by setting expnumber to be the preferred 5 digit number
"""
i=50
expnumber = 25226
min = 1
max=1200
recent = (ceriadat.tail(i))
name='spc1'
#print(recent)

#loadfromexn(expnumber,min,max,name)
    

"""
alternativly select the ith largerst data set from the n most recent:
"""
i=2
n=40
min = 241
max=480
recent = (ceriadat.tail(i))
name='spctest'
#loadfromrecent(i,n,min,max,name)

"""
simple partition, (loadfromexn script)
"""
i=50
expnumber = 25226
totalmin = 1
totalmax=1200
generalname='spc'
parts=5


recent = (ceriadat.tail(i))


#itrload(expnumber,totalmin,totalmax,generalname,parts)

"""
load by parts from nth most recent of i experiments
"""
n=2


i=70

totalmin = 1
totalmax=1200
generalname='spc'
parts=5

recent = (ceriadat.tail(i))
recent['secs'] = recent['secs'].astype(float)
n=n-1
recent = recent.sort_values(['secs'],ascending=False)
#print(recent)
row1=recent.iloc[n]
expname=row1['Number']


expnumber2 = (expname[3:8])
#print(expnumber)
#itrload(expnumber2,totalmin,totalmax,generalname,parts)