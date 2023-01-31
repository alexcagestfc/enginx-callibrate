# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

def itrprocess(name,b):
    num=b+1
    print(name+str(num))
    ConvertUnits(InputWorkspace=name+str(num), OutputWorkspace='converted'+str(num), Target='dSpacing', AlignBins=True) # 2023-01-16T15:09:36.804687000 execCount: 36
    SumSpectra(InputWorkspace='converted'+str(num), OutputWorkspace='SUMMED'+str(num), StartWorkspaceIndex=1) # 2023-01-16T15:09:49.676719000 execCount: 37
    FindPeaks(InputWorkspace='SUMMED'+str(num), WorkspaceIndex=0, PeaksList='SUMMED_PeakList_tmp'+str(num)) # 2023-01-16T15:11:05.315466000 execCount: 38
    Fit(Function='name=BackToBackExponential,I=100404,A=1124.77,B=433.477,X0=2.708,S=0.00501462,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=2.91249e+06,A=1124.77,B=433.477,X0=1.91428,S=0.00232302,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=361676,A=1124.77,B=433.477,X0=1.63244,S=0.00191117,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=207668,A=1124.77,B=433.477,X0=1.56295,S=0.00193105,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=511539,A=1124.77,B=433.477,X0=1.35339,S=0.00119148,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=140218,A=1124.77,B=433.477,X0=1.24192,S=0.00129303,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=210639,A=1124.77,B=433.477,X0=1.21044,S=0.00102504,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=727003,A=1124.77,B=433.477,X0=1.10482,S=0.00054056,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=159239,A=1124.77,B=433.477,X0=0.956601,S=0.000258897,ties=(A=1124.77,B=433.477)', InputWorkspace='SUMMED'+str(num), Output='SUMMED'+str(num), OutputCompositeMembers=True, StartX=0.305361381969526, EndX=2.8622057917670776, Normalise=True)

"""
iterative for multiple workspace
"""
genname='spc'
numberofspaces=5
b=0
for b in range(numberofspaces):
    itrprocess(genname,b)
    
    
    
    
"""
find theoretical vals
"""



Length = 5.41 #CeO2 bondlength in Amstrong
#all possible indices for h,k,l <10
evnindexs= (np.linspace(0,10,6))
oddindexs= (np.linspace(1,9,5))

from itertools import combinations_with_replacement 
# 
indices1 = list(combinations_with_replacement(oddindexs,3))

shape= np.shape(indices1)

max1 = shape[0]
M=[]
i=0

for i in range(max1):
    b=(int(indices1[i][0])**2+int(indices1[i][1])**2+int(indices1[i][2])**2)
    M.append(np.sqrt(b))
    i=i+1

indices2 = list(combinations_with_replacement(evnindexs,3))


shape= np.shape(indices2)

max2 = shape[0]

i=0

for i in range(max1):
    b=(int(indices2[i][0])**2+int(indices2[i][1])**2+int(indices2[i][2])**2)
    M.append(np.sqrt(b))
    i=i+1


M=np.sort(M)
Mshape=np.shape(M)
max3 = Mshape[0]
print(max3)
i=0
peakposition=[]
for i in range(max3):

    entry = Length/M[i]
    peakposition.append(entry)
    i=i+1
    
    
print(peakposition[1:70])

"""
"""
c=0
plt.figure()
for c in range(numberofspaces):
    d=c+1
    #ws='sum-2_Parameters'
    savefile='col'+str(d)+'.CSV'
    #SaveAscii(InputWorkspace=ws,Filename=savefile,Separator="CSV")
    import os
    #print('saving...')
    SaveAscii(InputWorkspace='SUMMED'+str(d)+'_Parameters', Filename='C:/Users/yth69564/col'+str(d)+'.CSV',Separator="CSV")
    #print('save done, trying load...')
    import pandas as pd
    column_names='target id' ,'value', 'error'
    col_width = [(0,2),(3,5),(6,15),(16,30),]
    #colspecs = col_width
    data = pd.read_csv('C:/Users/yth69564/col'+str(d)+'.CSV',names = column_names, na_filter = False, encoding = 'cp1252')
    #print(data.head(16))
    data = pd.DataFrame(data)
    x0data =data.iloc[::5, :]
    #print(x0data.head(20))
    x0vals = x0data.value 
    x0max=len(x0data)
    print(x0vals)


    
    x0vals.drop(index=[0])
    a=1
    y=[]
    x=[]
    for a in range(x0max+1):
        try:
            currentrow=x0vals.iloc[a]
            Athval=currentrow
            
            Athval=float(Athval)
            #Athval=Athval.astype(float)
            j=1
            smallestdif=[100]
            
            for j in range(max3):
                closeness = abs(Athval-peakposition[j])
                if closeness< smallestdif:
                    smallestdif=closeness
                    nearest=peakposition[j]
                    
                    j=j+1
                else:
                    j=j+1
            offset=(Athval-nearest)
            rel=(offset/Athval)*100
            x.append(nearest)
            y.append(rel)
            #print(Athval)
            #print('expected is ',nearest,'offset is ',rel,'%')
            #print('______________________________________')
        except:
            pass
        a=a+1


    """
    plot:
    """
    
    
    colours=['r','b','c','g','m','k']
    colour=str(colours[c])
    plt.plot(x,y,'k')
    plt.plot(x,y,str(colours[c])+'o',label='sector'+str(d))
plt.title('offset vs position')
plt.xlabel('calculated spacing position (Amstrong)')
plt.ylabel('relative offset from theoretical (%)')
plt.legend(loc="upper left")    