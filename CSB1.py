#ceriascript

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
"""
Section 1 indentifiers:

the following functions form dataframes using pandas based on information from SUMMARY.TXT
"""
# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
def testrun():
    print('werqing')



        
def identifyexperiments():
    """
    e.g. variable = identifyexperiments()
    
    variable is set as a pandas dataframe:
    columns: ['Number','Object','date','time','secs','experiment']
    these will be read directly from SUMMARY.TXT. Many aspects will require certain processes before being usable.
        one example of this sort of processing is 'Number'. which takes the format ('ENG' +str(opqrs)) where lmnop are integers different integers
        'Number' is queried to find the relevant filename. the file name will have the format ('ENGINX'+str(lmn)+str(opqrs)) qrs is identified in later scripts
        
    It is a requirement that the program is able to access SUMMARY.TXT. The file can be downloaded from my github as a zipfile 
    
    
    """
   
    col_names = ['Number','Object','date','time','secs','experiment']
    col_width = [(0,28),(28,52),(52,63),(63,72),(72,80),(80,88)]
    data = pd.read_fwf('C:\SUMMARY.TXT',names = col_names, colspecs = col_width, na_filter = False, encoding = 'cp1252')
    df = pd.DataFrame(data)
    ceriadat = df[df['Object'].str.contains('ceo2|CeO2|CEO2|ceria|Ceria')]
    return ceriadat
ceriadat = identifyexperiments()
print(ceriadat)



def getprefix(ceriadat):
    """
    e.g. variable2  = getprefix(variable1)
    variable1 will be required to have a column called 'date'. this condition will be met by dataframes set by identifyexperiments()
    variable2 will be identical to variable1 except for having an extra column called 'prefixes'. 
    each entry is a string formed of three integers, which I refer to in docstrings as lmn
    the afformentioned prefix so that the file name can be formed from numbers in the dataframe
    
    
    numbers lmn will be one of: 001,002,003,999
    the former three are genuine prefiexes that are used file accessing
    999 marks it as using the pre 2008 file format. as of now I how not prepared scripts for these. This is on my to do list.
    """
    date_aframe = ceriadat['date'] #essentially makes a pandas list 

    rows = len(date_aframe) #find number of experiments
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
            #marks out  pre 2008 experiments
        if date1<date and date<date2:
            prefix='001'
            n.append(prefix)
            #2008-2012 marked 001 etc...
        if date2<date and date<date3:
            prefix='002'
            n.append(prefix)
        if date3<date:
            prefix='003'
            n.append(prefix)
        i=i+1
    ceriadat['prefixes'] = n
    return ceriadat

"""
Section 2 loaders:
these functions should do the following:
take info from previosuly contructed dataframes
access files
load the contained data as a workspace based on preselected parameters
    load(filename, OutputWorkspace=name,SpectrumMin=min, SpectrumMax=max) is a function from mantid.simpleapi, it is used here but not made by me.

filepaths will need to have been set for the IDE in use. in mantid workbench this involves:
    File    
        Manage User Directories
            *naviagate to folder*
                Select
    I know this method is tedious. Esspecially given that at the current version is designed to load from any one of 50+ folders, each one would needed to added individually.
    I've already attempted once to make a more succinct process but it proved time consuming and wanted to make better use of office hours.

        

"""

def loadfromexn(expnumber,min,max,name,explist):
    """
    Loader function 1: loads experiment from 5 digit number 
    
    inputs are  expnumber: a 5 digit code associated with the experiment in question
                min: the first spectrum from the experiment that'll be used
                max: the final spectrum
                name: a string for which will be used for the workspace name      
           
    this number will be the very same 5 digit number the dataframe,'Number' characters[3:8] (in python's indexing) 
    
    
    function is very simple given that mantid api was already able to take the correct file name and load based on that information
    loadfromexn constructs the file name based on info provided by summary.txt
   
    """
    
    exp = ('ENG'+str(expnumber))
    #print(exp)
    row1 = explist[explist['Number'].str.contains(exp)] #finds experiments information from the data drame
    pref=row1['prefixes']# experiment file will have 8 digits, pref is the first three that aren't included in summary.txt   
    filename = ('ENGINX'+pref+str(expnumber)+'.RAW')#file name has this structure e.g. 'ENG00113579.RAW' where expnumber is '13579'
    filename = (str(filename))#file name converted from object to string
    filename= filename[10:28] #extra information removed
     
    pref = (str(pref)) #convert to string
    pref= pref[10:13]# extra information removed
    
    
    #if experiment is pre2008, it won't load
    if pref !=999:
        cyc= 0
        
        filename = ('ENGINX'+pref+str(expnumber)+'.RAW')
        filename = (str(filename))
        filename= filename#[0:28]
        #reasserts filename
        #print('loading: ',filename) # 
        Load(filename, OutputWorkspace=name,SpectrumMin=min, SpectrumMax=max)



def loadfromrecent(i,n,min,max,name):
    """
    Loader function 2: gets experiment with the ith largerst data set from the n most recent:
    it's very similar to loadfromexn
    
    inputs are as follows:
        i: i stands for integer. function considers the i most recent experiments and sorts them for largest number of detections
        n: n is also an integer. the function will load the nth most numerous data set
        min: the first spectrum from the experiment that'll be used
        max: the final spectrum
        name: a string for which will be used for the workspace name 
    
    the process finds experiement info
    constructs file name
    loads from file
    """
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
        
def itrload(expnumber,totalmin,totalmax,generalname,parts,explist,i):
    """
    this function uses loadfromexn, it takes similar inputs:
        expnumber: a 5 digit code associated with the experiment in question
        totalmin: the first spectrum from the experiment that'll be used
        totalmax: the final spectrum
            totalmin and totalmax are functionally identical to min and max in loadfromexn
        generalname: a string that will be part of the worksapce name followed by an integer relating to which detector set it is. 
        parts: number of distinct parts the function will load
        explist: the dataframe (I know it's not used for the other loaders, I found it helpful to have it callable while developing this. I will remove it in a later version)
        i: i is an integer. function only considers the i most recent experiements
        
    many analyses require distinct processing of different sets of detectors from the same experiment
        for example: analysing one detector bank of engin x and considering the five modules sepatately
    
    
     
    process:
    chops all except (i) most recent
    
    looped loadfromexn
    
    
    """
    recent = explist.tail(i)
    b=0
    partmax=[]
    for b in range(parts):
       
        c=b+1 #adds one because I want indexing to start at 1 not 0
        spacing=totalmax/parts# spacing is the size of module
        max=((spacing) *(c))
        min=(spacing*b)+1
        min=int(min)
        max=int(max)
        name=(generalname+str(c))
        loadfromexn(expnumber,min,max,name,recent)

"""
CSF: Convert Sum Fit
"""
def csf(name):
    ConvertUnits(InputWorkspace=name, OutputWorkspace='converted'+str(name[3:5]), Target='dSpacing', AlignBins=True) # 2023-01-16T15:09:36.804687000 execCount: 36
    SumSpectra(InputWorkspace='converted'+str(name[3:5]), OutputWorkspace='SUMMED'+str(name[3:5]), StartWorkspaceIndex=1) # 2023-01-16T15:09:49.676719000 execCount: 37
    FindPeaks(InputWorkspace='SUMMED'+str(name[3:5]), WorkspaceIndex=0, PeaksList='SUMMED_PeakList_tmp') # 2023-01-16T15:11:05.315466000 execCount: 38
    Fit(Function='name=BackToBackExponential,I=100404,A=1124.77,B=433.477,X0=2.708,S=0.00501462,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=2.91249e+06,A=1124.77,B=433.477,X0=1.91428,S=0.00232302,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=361676,A=1124.77,B=433.477,X0=1.63244,S=0.00191117,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=207668,A=1124.77,B=433.477,X0=1.56295,S=0.00193105,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=511539,A=1124.77,B=433.477,X0=1.35339,S=0.00119148,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=140218,A=1124.77,B=433.477,X0=1.24192,S=0.00129303,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=210639,A=1124.77,B=433.477,X0=1.21044,S=0.00102504,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=727003,A=1124.77,B=433.477,X0=1.10482,S=0.00054056,ties=(A=1124.77,B=433.477);name=BackToBackExponential,I=159239,A=1124.77,B=433.477,X0=0.956601,S=0.000258897,ties=(A=1124.77,B=433.477)', InputWorkspace='SUMMED'+str(name[3:5]), Output='SUMMED'+str(name[3:5]), OutputCompositeMembers=True, StartX=0.305361381969526, EndX=2.8622057917670776, Normalise=True)

"""
find Theoreticals
"""
def bcctheo(Length):
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
    #print(max3)
    i=0
    peakposition=[]
    for i in range(max3):

        entry = Length/M[i]
        peakposition.append(entry)
        i=i+1
    return(peakposition,max3)

"""
reader of experimental vals
"""
def readexperiment(m):
    n=str(m)
    SaveAscii(InputWorkspace='SUMMED'+n+'_Parameters', Filename='C:/Users/yth69564/atmpt1.CSV',Separator="CSV")
    column_names='target id' ,'value', 'error'
    col_width = [(0,2),(3,5),(6,15),(16,30),]
    data = pd.read_csv('C:/Users/yth69564/atmpt1.CSV',names = column_names, na_filter = False, encoding = 'cp1252')
    data = pd.DataFrame(data)
    x0data =data.iloc[::5, :]
    x0vals = x0data.value 
    x0max=len(x0data)
    return(data,x0data,x0vals,x0max)
    
"""
compare theory to experiment
"""


            
def offsetchart(x0vals,x0max,max3,peakposition):
    b=1
    x0vals.drop(index=[0])



    a=1
    y=[]
    x=[]
    for a in range(x0max+1):
        try:
            currentrow=x0vals.iloc[a]
            Athval=currentrow
            print(Athval)
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
            print('expected is ',nearest,'offset is ',rel,'%')
            print('______________________________________')
        except:
            pass
        a=a+1


    """
    plot:
    """
    plt.figure()
    plt.xlabel('calculated spacing position (Amstrong)')
    plt.ylabel('offset %')
    plt.plot(x,y)
    plt.plot(x,y,'ro')
    print(y)
    
    
