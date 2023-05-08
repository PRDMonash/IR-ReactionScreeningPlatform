from array import *
import numpy as np
import os
import pandas as pd
import csv
import matplotlib.pyplot as plt
import plotly
import scipy.linalg
import plotly.graph_objs as go
from mpl_toolkits import mplot3d
from string import ascii_uppercase
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score 


path = r"C:\Users\ansil\Desktop\BP-100C.txt"
path_t = r"C:\Users\ansil\Desktop"
filename =  os.path.splitext(os.path.split(path)[1])[0]
rawdata = np.loadtxt(path) 

#simulation Reactor, for last part for time and money to synthesis the desired Mn, to synthesis specific monomer
Vreactor = 1 # the volume of reactor is 1 ml
C_Monomer = 6 #float(input('\033[1;31mPlease input the initial concentration of your Monomer(M):>> \033[0m'))
C_RaftAgent = 0.5 #float(input('\033[1;31mPlease input the initial concentration of your RaftAgent (M):>> \033[0m'))
C_Initiator = 0.05 #float(input('\033[1;31mPlease input the initial concentration of your initiator (M):>> \033[0m'))

M_polymer = 0.5 # the molar of monomer needed
DesiredMn = 4000 # the desired molecular weight of polymer
targetdp= (DesiredMn - 350)/86.09
MonomerCon = 3

OriDP = []
OriResidencetime = []
OriConversion = []

print(len(rawdata[0]))

#for each DP for sorting the matrix
for i in range(109):
     for j in range(120):
        DPList = rawdata[i]
        dp = 50 + j *1
        residencetime = (60 + i *5)/60
        conversion = DPList[j]

        OriDP.append(dp)
        OriResidencetime.append(residencetime)
        OriConversion.append(conversion)
           
        

# save converison vaeries from time data to csv file
with open(r'{}\{}-Data.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'DP':OriDP,
        'Residence time/minute':OriResidencetime, #redisence time for each DP, gives all the conversion% from the matrix data
        'Conversion/%':OriConversion,
      
}
        
column_names = ['DP','Residence time/minute','Conversion/%']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-Data.csv'.format(path_t,filename), columns = column_names)   

#generate a formula for the data from the matrix
# 3-D surface fitting 
X = np.array(OriDP); Y = np.array(OriResidencetime); Z = np.array(OriConversion)
data = np.c_[X,Y,Z]

def func(X, A, B, C, D, E, F, G, H, I, J):
    """
    X is concentration; Y is Residence time; Z is Conversion
    """
    x,y,Z = X.T 
    return (A*x**3 + B*y**3 + C*x*y**2 + D*y*x**2 + E*x**2 + F*y**2 + G*x*y + H*x + I*y + J) #equation for fitting

popt, _ = curve_fit(func, data, data[:,2])

coefficient = []
for i, j in zip(popt, ascii_uppercase):
    # print(f"{j} = {i:.3f}")
    coefficient.append(i)
#the coeffiecnet for the fitted plots
A = float(coefficient[0]); B = float(coefficient[1]); C = float(coefficient[2]); D = float(coefficient[3]); E = float(coefficient[4]); F = float(coefficient[5]); G = float(coefficient[6])
H = float(coefficient[7]); I = float(coefficient[8]); J = float(coefficient[9])

for i, j in zip(popt, ascii_uppercase):
    print(f"{j} = {i:.3f}")
    coefficient.append(i)

print(coefficient)
Zdata = A*X**3 + B*Y**3 + C*X*Y**2 + D*Y*X**2 + E*X**2 + F*Y**2 + G*X*Y + H*X + I*Y + J
R_squared = r2_score(Z, Zdata) #r2 value of the fitted plots

print(f'the R_squared value of 3 dimensional surface plot fitting is {R_squared}')

#prints the 3D plots (orignial)
fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1,2,1, projection='3d')
ax.scatter3D(X, Y, Z, c='r')
ax.set_xlabel('DP')
ax.set_ylabel('Residence time (minute)')
ax.set_zlabel('Conversion (%)')
ax.set_title('Original Plot')

#fitted plot
X, Y = np.meshgrid(X, Y)
zdata = A*X**3 + B*Y**3 + C*X*Y**2 + D*Y*X**2 + E*X**2 + F*Y**2 + G*X*Y + H*X + I*Y + J
ax = fig.add_subplot(1,2,2, projection='3d')
surf = ax.plot_surface(X, Y, zdata, cmap = plt.cm.rainbow, linewidth=0, antialiased=False, rcount=100, ccount=100)
ax.set_xlabel('DP')
ax.set_ylabel('Residence time (minute)')
ax.set_zlabel('Conversion (%)')
ax.set_title('Fitting Plot')
plt.savefig(f'{path_t}/{filename}')


############# Reaction Study
"""
Calculate the reaction rate only chose 16 data point in the concentration range(0.5:5), and for each concentration only chose 19 different residence time data points.
"""
def func (X:float,Y:float)->float:
    '''
    X: Concentration of monomer, unit: M; Y Residence time of reaction,unit:minute
    ''' 
    return(A*X**3 + B*Y**3 + C*X*Y**2 + D*Y*X**2 + E*X**2 + F*Y**2 + G*X*Y + H*X + I*Y + J)

kobsDP= []
Kt = []
R2= []
kobsdp = []
KobsLne = []
KobsResidencetime= []

#reaction rate constant for each DP
for i in range(121):

    kobs_dp = 50 + 1*i
    kobsDP.append(kobs_dp)
    KobsResidence= []
    Lne = []
    KobsResidence.append(0)
    Lne.append(0)

    KobsResidencetime.append(0)
    kobsdp.append(kobs_dp)
    KobsLne.append(0)
   #calculate rate constant for each DP at a specific residence time, for every 30 seconds
    for j in range(19):
        
        kobsdp.append(kobs_dp)
        kobsresidencetime = (60 + j*30)/60
        # print(kobsresidencetime)
        KobsResidencetime.append(kobsresidencetime)
        KobsResidence.append(kobsresidencetime)
        kobsconversion = func(kobs_dp,kobsresidencetime)
        # print(kobsconversion)
        #Conversion.append(conversion)
        M = MonomerCon * (100-kobsconversion)/100 #real time concentration value of monomer
        # print(f'Ao is {A0}')
        #print(A0)
        lne = np.log(M/MonomerCon)
        # print(f'lne is {lne}')
        #print(lne)
        Lne.append(lne)
        KobsLne.append(lne)

        with open(r'{}\{}-kobs-originalData.csv'.format(path_t, filename), 'w') as f:
            pass 

        data = {
                'DP':kobsdp,
                'Residencetime':KobsResidencetime,
                'lne':KobsLne,
        }
                
        column_names = ['DP','Residencetime','lne']

        df = pd.DataFrame(data, columns = column_names) #columns = column_names
        df.to_csv(r'{}\{}-kobs-originalData.csv'.format(path_t,filename), columns = column_names)    


    KobsResidence = np.array(KobsResidence)
    KobsResidence = KobsResidence[:,np.newaxis]
    a, _, _, _ = np.linalg.lstsq(KobsResidence, Lne, rcond=None) #linear fit of residence time log value of M/M0
    Ratecoefficient = abs(a[0]) #the slope of the previus linear fitting
    Kt.append(Ratecoefficient)
    data = a * KobsResidence
    
    R_squared = r2_score(Lne, data)
    R2.append(R_squared) #R2 value of residence time vs Ln(M/M0)
    # print(R_squared)

    # plt.scatter(KobsResidence, Lne, color = 'r')
    # plt.plot(KobsResidence, data, color = 'b')
    # plt.xlabel('residencetime /minute')
    # plt.ylabel('ln(M/MO)')
    # plt.savefig(f'{path_t}/{C_Monomer}.png')
    # plt.close()



# save converison vaeries from time data to csv file

with open(r'{}\{}-kobs-Data.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'DP':kobsDP,
        'Reactionrate':Kt,
        'R2 value':R2,
}
        
column_names = ['DP','Reactionrate','R2 value']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-kobs-Data.csv'.format(path_t,filename), columns = column_names)
       

######## Reaction conditions for Desired polymer  

def Calresidue(targetconversion,X,Y)->float:
    '''
    Explanation: this function is used to calculate the residence time
    '''
    residue = abs(targetconversion-(A*X**3 + B*Y**3 + C*X*Y**2 + D*Y*X**2 + E*X**2 + F*Y**2 + G*X*Y + H*X + I*Y + J))

    return(residue)




Polymercon = []
TotalFlowrate = []
Timecomsumed = []
FlowMonomer = []; FlowRaft = []; FlowSolvent = []; FlowInitiator = []
VolumeMonomer = []; VolumeRaft = []; VolumeSolvent = []; VolumeInitiator = []
Money = []
Efactor = []
DP = []
Residencetime = []
Conversion = []
conresi = []


#how much money, time, E-factor
for j in range(121):
     
    dporder = 50 + 1 *j

    for i in range(541):
        time = (60 + i *1)/60
        targetconversion = targetdp*100/dporder

        left = Calresidue(targetconversion, dporder, time)

        if  left <= 0.5: 
            residencetime = time
            print(f"DP is {dporder}" )
            print (residencetime)
            gotconversion = func(dporder, time)
            Conversion.append(gotconversion)
            DP.append(dporder)
            flowrate = Vreactor/residencetime     
            FRmonomer = MonomerCon * flowrate / C_Monomer
            # print(f"monomer flow rate is {FRmonomer}")
            FRraft = FRmonomer * C_Monomer / (targetdp * C_RaftAgent)
            FRInitiator = MonomerCon * flowrate /(1000 * C_Initiator) 
            FRSolvent = flowrate - FRmonomer - FRraft - FRInitiator 
            FlowMonomer.append(FRmonomer); FlowRaft.append(FRraft); FlowSolvent.append(FRSolvent); FlowInitiator.append(FRInitiator)
            polymercon = MonomerCon * (flowrate / 1000) * targetconversion/100 / ((DesiredMn - 350)/86.09)
            Polymercon.append(polymercon)
            Time_need = M_polymer/polymercon + 2
            # print(Time_need)
            Timecomsumed.append(Time_need)
            volumeMonomer = Time_need * FRmonomer
            volumeRaft = FRraft * Time_need
            volumeSolvent = FRSolvent * Time_need
            volumeInitiator = FRInitiator * Time_need
            VolumeMonomer.append(volumeMonomer); VolumeRaft.append(volumeRaft); VolumeSolvent.append(volumeSolvent); VolumeInitiator.append(volumeInitiator)
            MoneyConsumed = volumeMonomer* 0.032 + volumeRaft * 0.95 + volumeSolvent * 0.0312 + volumeInitiator * 0.11902
            efactor = (volumeMonomer * 1 + volumeSolvent * 1.1 + volumeRaft *0.94137 + volumeInitiator * 1.11 - DesiredMn*M_polymer)/(DesiredMn*M_polymer)     
            Efactor.append(efactor)
            Money.append(MoneyConsumed)
            conresi.append([dp,residencetime])
            Residencetime.append(residencetime)
            TotalFlowrate.append(flowrate)
        else:
            pass

# save converison vaeries from time data to csv file
with open(r'{}\{}-calculation-Data.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'DP/M':DP,
        'Conversion/%':Conversion,
        'Residence time/minute':Residencetime,
        'Polymerconcentration/ M/min':Polymercon,
        'TotalFlowrate/ ml/min':TotalFlowrate,
        'Timeconsumed/min':Timecomsumed,
        'FlowMonomer/ml/min':FlowMonomer, 'FlowRaft/ ml/min':FlowRaft, 'FlowSolvent/ ml/min': FlowSolvent, 'FlowInitiator/ ml/min': FlowInitiator,
        'VolumeMonomer/ ml':VolumeMonomer,'VolumerRaft/ ml':VolumeRaft, 'VolumeSolvent/ ml':VolumeSolvent,'VolumeInitiator/ ml':VolumeInitiator,
        'Money/$':Money,
        'efactor':Efactor
}   

column_names = ['DP/M','Conversion/%','Residence time/minute','Polymerconcentration/ M/min','TotalFlowrate/ ml/min','Timeconsumed/min',
                'FlowMonomer/ml/min', 'FlowRaft/ ml/min', 'FlowSolvent/ ml/min', 'FlowInitiator/ ml/min', 'VolumeMonomer/ ml', 'VolumerRaft/ ml', 'VolumeSolvent/ ml', 'VolumeInitiator/ ml', 'Money/$','efactor'
]

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-calculation-Data.csv'.format(path_t,filename), columns = column_names)   