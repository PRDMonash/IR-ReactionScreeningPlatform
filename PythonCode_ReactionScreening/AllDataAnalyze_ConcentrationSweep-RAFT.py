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


path = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\MA\5s-step\3D surface data\110\110Zdata.txt"
path_t = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\MA\5s-step\3D surface data\110"
filename =  os.path.splitext(os.path.split(path)[1])[0]
rawdata = np.loadtxt(path) 


Vreactor = 1 # the volume of reactor is 1 ml
C_Monomer = 6 #float(input('\033[1;31mPlease input the initial concentration of your Monomer(M):>> \033[0m'))
C_RaftAgent = 0.5 #float(input('\033[1;31mPlease input the initial concentration of your RaftAgent (M):>> \033[0m'))
C_Initiator = 0.05 #float(input('\033[1;31mPlease input the initial concentration of your initiator (M):>> \033[0m'))

M_polymer = 0.5 # the molar of monomer needed
DesiredMn = 4000 # the desired molecular weight of polymer
targetconversion = (DesiredMn - 350)/86.09


Ori_Concentration = []
Ori_Residencetime = []
Ori_Conversion = []

# print(len(rawdata[0]))

for i in range(109):
     for j in range(121):
        ConversionList = rawdata[i]
        if ConversionList[j] <= 0 or 0.5 + j*0.0375 < 1:
            pass 

        else:
             concentration = 0.5 + j *0.0375
             residencetime = (60 + i *5)/60
             conversion = ConversionList[j]

             Ori_Concentration.append(concentration)
             Ori_Residencetime.append(residencetime)
             Ori_Conversion.append(conversion)
           
        

# save converison varies from time data to csv file
with open(r'{}\{}-rawData.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'Concentration/M':Ori_Concentration,
        'Residence time/minute':Ori_Residencetime,
        'Conversion/%':Ori_Conversion,
      
}
        
column_names = ['Concentration/M','Residence time/minute','Conversion/%']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-rawData.csv'.format(path_t,filename), columns = column_names) 


# 3-D surface fitting 
X = np.array(Ori_Concentration); Y = np.array(Ori_Residencetime); Z = np.array(Ori_Conversion)
data = np.c_[X,Y,Z]

def func(X, A, B, C, D, E, F, G, H, I, J):
    """
    X is concentration; Y is Residence time; Z is Conversion
    """
    x,y,Z = X.T 
    return (A*x**3 + B*y**3 + C*x*y**2 + D*y*x**2 + E*x**2 + F*y**2 + G*x*y + H*x + I*y + J)

popt, _ = curve_fit(func, data, data[:,2])

coefficient = []
for i, j in zip(popt, ascii_uppercase):
    print(f"{j} = {i:.3f}")
    coefficient.append(i)


A = float(coefficient[0]); B = float(coefficient[1]); C = float(coefficient[2]); D = float(coefficient[3]); E = float(coefficient[4]); F = float(coefficient[5]); G = float(coefficient[6])
H = float(coefficient[7]); I = float(coefficient[8]); J = float(coefficient[9])

# print(coefficient)
Zdata = A*X**3 + B*Y**3 + C*X*Y**2 + D*Y*X**2 + E*X**2 + F*Y**2 + G*X*Y + H*X + I*Y + J
R_squared = r2_score(Z, Zdata)
print(f'the R_squared value of 3 dimensional surface plot fitting is {R_squared}')


fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1,2,1, projection='3d')
ax.scatter(X, Y, Z, c='r')
ax.set_xlabel('Concentration (M)')
ax.set_ylabel('Residence time (minute)')
ax.set_zlabel('Conversion (%)')
ax.set_title('Original Plot')

X, Y = np.meshgrid(X, Y)
zdata = A*X**3 + B*Y**3 + C*X*Y**2 + D*Y*X**2 + E*X**2 + F*Y**2 + G*X*Y + H*X + I*Y + J
ax = fig.add_subplot(1,2,2, projection='3d')
surf = ax.plot_surface(X, Y, zdata, cmap = plt.cm.rainbow, linewidth=0, antialiased=False, rcount=100, ccount=100)
ax.scatter(1.5,9,73.8, c = 'y', s = 30)
ax.set_xlabel('Concentration (M)')
plt.xlim([0,5])
ax.set_ylabel('Residence time (minute)')
plt.ylim([0,10])
ax.set_zlabel('Conversion (%)')
# plt.zlim([0,100])
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

result = func(1.5,9)
print(f'result is {result}')

kobsMonomerConcentration = []
Kt = []
R2= []
kobsMonomercon = []
KobsLne = []
KobsResidencetime= []

for i in range(16):

    kobsC_Monomer = 0.5 + 0.3 *i
    kobsMonomerConcentration.append(kobsC_Monomer)
    KobsResidence= []
    Lne = []
    KobsResidence.append(0)
    Lne.append(0)
    for j in range(19):
        
        kobsMonomercon.append(kobsC_Monomer)
        kobsresidencetime = (60 + j*30)/60
        # print(kobsresidencetime)
        KobsResidencetime.append(kobsresidencetime)
        KobsResidence.append(kobsresidencetime)
        kobsconversion = func(kobsC_Monomer,kobsresidencetime)
        # print(kobsconversion)
        #Conversion.append(conversion)
        A0 = kobsC_Monomer * (100-kobsconversion)/100
        # print(f'Ao is {A0}')
        #print(A0)
        lne = np.log(A0/kobsC_Monomer)
        # print(f'lne is {lne}')
        #print(lne)
        Lne.append(lne)
        KobsLne.append(lne)

        with open(r'{}\{}-kobs-originalData.csv'.format(path_t, filename), 'w') as f:
            pass 

        data = {
                'Monomerconcentration/M':kobsMonomercon,
                'Residencetime':KobsResidencetime,
                'lne':KobsLne,
        }
                
        column_names = ['Monomerconcentration/M','Residencetime','lne']

        df = pd.DataFrame(data, columns = column_names) #columns = column_names
        df.to_csv(r'{}\{}-kobs-originalData.csv'.format(path_t,filename), columns = column_names)    


    KobsResidence = np.array(KobsResidence)
    KobsResidence = KobsResidence[:,np.newaxis]
    a, _, _, _ = np.linalg.lstsq(KobsResidence, Lne, rcond=None)
    Ratecoefficient = abs(a[0])
    Kt.append(Ratecoefficient)
    data = a * KobsResidence
    
    R_squared = r2_score(Lne, data)
    R2.append(R_squared)
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
        'Monomerconcentration/M':kobsMonomerConcentration,
        'Reactionrate':Kt,
        'R2 value':R2,
}
        
column_names = ['Monomerconcentration/M','Reactionrate','R2 value']

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
FlowMonomer = []; FlowRaft = []; FlowSolvent = []
VolumeMonomer = []; VolumeRaft = []; VolumeSolvent = []
Money = []
Efactor = []
GotResidencetime = []
GotConversion = []
GotMonomer = []
conresi = []

for j in range(81):
    gotconcentration = 1 + j* 0.05

    for i in range(541):

        time = (60 + i *1)/60
        left = Calresidue(targetconversion, gotconcentration, time)

        if  left <= 0.5: 
            GotMonomer.append(gotconcentration)
            gotresidencetime = time
            
            gotconversion = func(gotconcentration,gotresidencetime) 
            GotConversion.append(gotconversion)

            flowrate = Vreactor/gotresidencetime     
            FRmonomer = gotconcentration * flowrate / C_Monomer
            

            FRraft = FRmonomer * C_Monomer / (100 * C_RaftAgent)
            FRSolvent = flowrate - FRmonomer - FRraft 

            FlowMonomer.append(FRmonomer); FlowRaft.append(FRraft); FlowSolvent.append(FRSolvent)
            polymercon = (gotconcentration * flowrate / 1000) * targetconversion/100 / ((DesiredMn - 350)/86.09)
            Polymercon.append(polymercon)
            Time_need = M_polymer/polymercon + 2
            # print(Time_need)
            Timecomsumed.append(Time_need)
            volumeMonomer = Time_need * FRmonomer
            volumeRaft = FRraft * Time_need
            volumeSolvent = FRSolvent * Time_need
            VolumeMonomer.append(volumeMonomer); VolumeRaft.append(volumeRaft); VolumeSolvent.append(volumeSolvent)
            MoneyConsumed = volumeMonomer* 0.032 + volumeRaft * 0.126 + volumeSolvent * 0.0312 
            efactor = (volumeMonomer * 1 + volumeSolvent * 1.1 + volumeRaft *0.94137  - DesiredMn*M_polymer)/(DesiredMn*M_polymer)     
            Efactor.append(efactor)
            Money.append(MoneyConsumed)
            GotResidencetime.append(gotresidencetime)
            TotalFlowrate.append(flowrate)
        else:
            pass

# save converison vaeries from time data to csv file
with open(r'{}\{}-calculation-Data.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'Monomerconcentration/M':GotMonomer,
        'Conversion/%':GotConversion,
        'Residence time/minute':GotResidencetime,
        'Polymerconcentration/ M/min':Polymercon,
        'TotalFlowrate/ ml/min':TotalFlowrate,
        'Timeconsumed/min':Timecomsumed,
        'FlowMonomer/ml/min':FlowMonomer, 'FlowRaft/ ml/min':FlowRaft, 'FlowSolvent/ ml/min': FlowSolvent, 
        'VolumeMonomer/ ml':VolumeMonomer,'VolumerRaft/ ml':VolumeRaft, 'VolumeSolvent/ ml':VolumeSolvent,
        'Money/$':Money,
        'efactor':Efactor
}
        
# print(len(GotMonomer))
# print(len(GotResidencetime))
# print(len(Polymercon))
# print(len(TotalFlowrate))
# print(len(Timecomsumed))
# print(len(FlowMonomer))
# print(len(VolumeMonomer))
# print(len(Money))
# print(len(Efactor))




column_names = ['Monomerconcentration/M','Conversion/%','Residence time/minute','Polymerconcentration/ M/min','TotalFlowrate/ ml/min','Timeconsumed/min',
                'FlowMonomer/ml/min', 'FlowRaft/ ml/min', 'FlowSolvent/ ml/min','VolumeMonomer/ ml', 'VolumerRaft/ ml', 'VolumeSolvent/ ml','Money/$','efactor'
               ]

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-calculation-Data.csv'.format(path_t,filename), columns = column_names)   


        
with open(r'{}\{}-Data.csv'.format(path_t, filename), 'w') as f:
            pass 

data = {
        'C':Ori_Concentration,
        'T':Ori_Residencetime,
        'CONVERSION':Zdata,
}
                
column_names = ['C','T','CONVERSION']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-Data.csv'.format(path_t,filename), columns = column_names) 


T_concentration = []
T_residencetime = []
T_Conversion = []
time = [1,3,5,8,10]
for j in time:
    for i in range(121):
        con = 0.5 + 4.5*i/120
        therotical_conversion = func(con,j)
        if therotical_conversion < 0:
             conversion = 0
        else:
             conversion = therotical_conversion
        T_concentration.append(con);T_residencetime.append(j);T_Conversion.append(conversion)

with open(r'{}\{}-therotical_conversion_Data.csv'.format(path_t, filename), 'w') as f:
            pass 

data = {
        'C':T_concentration,
        'T':T_residencetime,
        'CONVERSION':T_Conversion,
}
                
column_names = ['C','T','CONVERSION']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-therotical_conversion_Data.csv'.format(path_t,filename), columns = column_names) 

