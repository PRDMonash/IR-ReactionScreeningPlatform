from CreateDataFolder import *
import csv
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
import matplotlib.ticker
from matplotlib import rcParams
import matplotlib
matplotlib.use('Agg')
import os
import datetime
import pandas as pd
from numpy import sqrt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import matplotlib.ticker
from syringepump import *
from SF10 import *
from Functions import *
from datetime import datetime
import threading

# Create a experiment file folder to save all the data  
print("Please input the name of you Experiment :>>")
ExperimentName = input(':>>')

# the path where we save the data
ParentFolder = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\BA" 
Experimentfolder_path = CreateDataFolder(ExperimentName,ParentFolder)

# the path of IR rawdata, which will be monitored by watchdog 
IRrawdata_path = r"C:\Users\IR112\Documents\iC IR Experiments\{}".format(ExperimentName) 
# the path in the shared drive where the IR raw data will be saved
SavedIRrawdata_path = r'{}/IR_RawData'.format(Experimentfolder_path) 

# create a empty csv file to save all the calsulated data 
with open(r'{}\{}-Data.csv'.format(Experimentfolder_path, ExperimentName), 'a') as f:
    pass 

# Open the reaction parameter file and load the data to data frame
ParameterFile_Path = r'\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\09. ROP\Python Code\CRSweepExperimentParameter_Checking.xlsx'
  # copy the experiment parameters file to the experiment folder
shutil.copy(ParameterFile_Path, Experimentfolder_path)
Parameter_df =  pd.read_excel(ParameterFile_Path, index_col=0)
PumpName = Parameter_df.iloc[:,0]; PumpPort = Parameter_df.iloc[:,1]; StockConcentration = Parameter_df.iloc[:,2] 
DesiredMonomerCon = Parameter_df.iloc[:,3][1]; QuenchingFlowRate = Parameter_df.iloc[:,4][3]; DesiredCR = Parameter_df.iloc[:,8][1];  
V_reactor = Parameter_df.iloc[:,5][1]; V_input = Parameter_df.iloc[:,6][1]; V_dead = Parameter_df.iloc[:,7][1]; dp = Parameter_df.iloc[:,11][1]
SweepStepLength = Parameter_df.iloc[:,9][1]; ResidenceTime = Parameter_df.iloc[:,10][1]

PumpMonmer = SyringePump('{}','{}',format(PumpPort[2],PumpName[2])); PumpCatalyst = SyringePump('{}','{}',format(PumpPort[2],PumpName[2]))
PumpSolvent = SyringePump('{}','{}', format(PumpPort[3],PumpName[3])); PumpQuenching = SF10('{}','{}', format(PumpPort[4],PumpName[4]))

# Concentration sweep flow rate calculation
FlowRateMonomer = []; FlowRateCatalyst = []; FlowRateSolvent = []; DP = []; ConcentrationMonomer = []; SleepTime = []; MonomerCon =[]; CRatio= []   
   # start point flow rate calculation
TotalFlowrate = V_reactor*60/ResidenceTime
FRMonomer =  TotalFlowrate*DesiredMonomerCon/StockConcentration[1]
FRCatalyst = TotalFlowrate* DesiredMonomerCon/(DesiredCR*StockConcentration[2])
FRsolvent = TotalFlowrate-FRMonomer-FRCatalyst
FlowRateMonomer.append(FRMonomer); FlowRateCatalyst.append(FRCatalyst); FlowRateSolvent.append(FRsolvent); DP.append(dp); CRatio.append(DesiredCR)

ClearTime = V_reactor*60/TotalFlowrate + V_dead*60/(TotalFlowrate+QuenchingFlowRate)+60
SleepTime.append(ClearTime)

# watchdog class for the data analysis
PeakArea = []; ScanTime = []; Initial_Con = []; Realtime_Con = []; Conversion = []; MCRatio = []; DoP = []

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        file_created = event.src_path
        print(file_created)
        listfile_created = os.listdir(IRrawdata_path)
        
        if len(listfile_created)*5 >= V_reactor*60/TotalFlowrate + V_dead*60/(TotalFlowrate+ QuenchingFlowRate):
            try:
                shutil.copy(file_created, SavedIRrawdata_path )
                sleep(1)

                with open(file_created) as csvfile:
                    rawdata = list(csv.reader(csvfile, delimiter = ","))
                
                # set scan time 
                listfile = os.listdir(SavedIRrawdata_path)
                j = len(listfile)
                scantime = j*5/60 
                ScanTime.append(scantime)
                print(f"{j} scan data collected ")

                exampledata = np.array(rawdata[1:],dtype = np.float64) # rawdata[1:], first line is the head, so we start from the second line
                data_x = exampledata[:,0]
                x_data = list(data_x)
                xdata = []

                for i in data_x:
                    if 1588 <= i <= 1662: # IR spectra are normalized at 1310 cm-1 (peak belongs to DMSO)
                        xdata.append(i)
                # print(xdata)
                indexlow = x_data.index(xdata[0])
                indexhigh = x_data.index(xdata[-1])
                # print(indexhigh, indexlow)
                ydata_1 = exampledata[indexlow:indexhigh+1,1]
                
                x_base = [1662, 1588]
                y_base = [ydata_1[0], ydata_1[-1]]

                Allarea = abs(integrate(xdata, ydata_1))
                Area2 = abs(integrate(x_base,y_base))
                peakarea = Allarea - Area2

                # print(Allarea, Area2, peakarea)
                PeakArea.append(peakarea)

                # Calculate concentration and conversion
                concentration = CalConcentration(peakarea)
                RealConcentration = (TotalFlowrate+QuenchingFlowRate)*concentration/TotalFlowrate
                Realtime_Con.append(RealConcentration)

                Initial_Con.append(MonomerCon[0]); DoP.append(DP[0]); MCRatio.append(CRatio[0])
                conversion = CalConversion(RealConcentration,MonomerCon[0])
                Conversion.append(conversion) 


                # save the calculated data to a new CSV file under ExperimentName folder 
                data = {
                    'scantime/minute':ScanTime,
                    'Peakarea':PeakArea,
                    'InitialConcentration':Initial_Con,
                    'DP':DoP,
                    'CatalystRatio':MCRatio,
                    'Concentration/M': Realtime_Con,
                    'Conversion/%':Conversion,
                }
                column_names = ['scantime/minute','Peakarea','InitialConcentration','DP','CatalystRatio','Concentration/M', 'Conversion/%']
                df = pd.DataFrame(data, columns = column_names) #columns = column_names
                df.to_csv(r'{}\{}-Data.csv'.format(Experimentfolder_path,ExperimentName), columns = column_names)

                fig = plt.figure()
                ax = fig.add_subplot(111)
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(2) 
                ax.tick_params(axis = 'both', which = 'major', labelsize = 12)
                ax.tick_params(axis = 'both', which = 'minor', labelsize = 12)
                plt.plot(ScanTime, PeakArea, color = 'red', linewidth = 4, linestyle = ':')
                plt.xlabel('Scantime/minute',fontsize = 14)
                plt.ylabel('Peakarea',fontsize = 14)
                plt
                plt.savefig(f'{Experimentfolder_path}/RealtimePicture/Scantime_Peakarea')
                plt.clf()
                plt.close()
                
                fig = plt.figure()
                ax = fig.add_subplot(111)
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(2) 
                ax.tick_params(axis = 'both', which = 'major', labelsize = 12)
                ax.tick_params(axis = 'both', which = 'minor', labelsize = 12)
                plt.plot(ScanTime, Realtime_Con, color = 'blue', linewidth = 3, linestyle = 'dotted')
                plt.plot(ScanTime, Initial_Con, color = 'red', linewidth = 3, linestyle = 'dotted')
                plt.legend(["real time", "Initial"])
                plt.xlabel('Scantime/minute', fontsize = 14)
                plt.ylabel('Concentration',fontsize = 14)
                plt.savefig(f'{Experimentfolder_path}/RealtimePicture/Scantime_Concentration')
                plt.clf()
                plt.close()
                
                fig = plt.figure()
                ax = fig.add_subplot(111)
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(2) 
                ax.tick_params(axis = 'both', which = 'major', labelsize = 12)
                ax.tick_params(axis = 'both', which = 'minor', labelsize = 12)
                plt.plot(ScanTime, Conversion, color = 'black', linewidth = 3, linestyle = '-')
                plt.xlabel('Scantime/minute', fontsize = 14)
                plt.ylabel('Conversion', fontsize = 14)
                plt.savefig(f'{Experimentfolder_path}/RealtimePicture/Scantime_Conversion')
                plt.clf()
                plt.close()

                fig = plt.figure()
                ax = fig.add_subplot(111)
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(2) 
                ax.tick_params(axis = 'both', which = 'major', labelsize = 12)
                ax.tick_params(axis = 'both', which = 'minor', labelsize = 12)
                plt.plot(ScanTime, Conversion, color = 'black', linewidth = 3, linestyle = '-')
                plt.xlabel('CatalystRatio', fontsize = 14)
                plt.ylabel('Conversion', fontsize = 14)
                plt.savefig(f'{Experimentfolder_path}/RealtimePicture/Catalystratio_Conversion')
                plt.clf()
                plt.close()

            except Exception:
                pass

        else:
            pass

def DataAnalysis():
    observer = Observer(); event_handler = Handler()
    observer.schedule(event_handler, IRrawdata_path, recursive = True)
    print('Observer start')
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def PumpControl():
    PumpMonmer.start(); PumpCatalyst.start(); PumpSolvent.start(), PumpQuenching.start()
    sleep(0.5)
    PumpMonmer.changeFlowrate(0);PumpCatalyst.changeFlowrate(0);PumpSolvent.changeFlowrate(0);PumpQuenching.changeFlowrate(0)
    sleep(0.5)
    
    today = datetime.now()
    CurrentTime = today.strftime("%H:%M:%S")
    PumpMonmer.changeFlowrate(FlowRateMonomer[0]);PumpCatalyst.changeFlowrate(FlowRateCatalyst[0])
    PumpSolvent.changeFlowrate(FlowRateSolvent[0]);PumpQuenching.changeFlowrate(QuenchingFlowRate)
    sleep(SleepTime[0])
    PumpMonmer.stop();PumpCatalyst.stop();PumpSolvent.stop();PumpQuenching.stop()


p1=threading.Thread(target=DataAnalysis)
p2=threading.Thread(target=PumpControl)    

p1.start();p2.start()
p1.join();p1.join()