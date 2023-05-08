import datetime
import os 
import serial


def CreateDataFolder(ExperimentName, ParentFolder):
    """
    ExperimentName: the name of the experiment, should be the same as the one that you used to name your IR experiment----> str
    ParentFolder: the path where you save your data folder-----> str
    """ 
    # # creat file to save experiment data
    # print("Please input the name of you Experiment :>>")
    # ExperimentName = input(':>>')
    # # print("Please input the parentpath of saving your data")
    # ParentFolder = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\BA" #input(':>>') 

    # Obtain the year,month,date
    today = datetime.datetime.now()
    YearTime = today.strftime("%Y")
    MonthTime = today.strftime("%m")
    day = today.strftime("%d")
    print(YearTime,MonthTime,day)

    #Create Year folder
    YearFolderPath = r'{}\{}'.format(ParentFolder,YearTime)
    if not os.path.exists(YearFolderPath):
        os.makedirs(YearFolderPath)

    #Create Month folder under year folder
    MonthFolderPath = r'{}\{}\{}'.format(ParentFolder,YearTime, MonthTime)
    if not os.path.exists(MonthFolderPath):
        os.makedirs(MonthFolderPath)

    #Create day folder under Month
    DayFolderPath = r'{}\{}\{}\{}'.format(ParentFolder, YearTime, MonthTime,day)
    if not os.path.exists(DayFolderPath):
        os.makedirs(DayFolderPath)


    # Create Experiment folder under day and create subfolders under experiment to save all data
    ExperimentNameFolder = r'{}\{}\{}\{}\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName)
    ExperimentNameFolder_1 = r'{}\{}\{}\{}\{}_1'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName)
    ExperimentNameFolder_2 = r'{}\{}\{}\{}\{}_2'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName)
    ExperimentNameFolder_3 = r'{}\{}\{}\{}\{}_3'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName) 
            
    if not os.path.exists(ExperimentNameFolder):
        os.makedirs(ExperimentNameFolder)
        os.makedirs(r'{}\{}\{}\{}\{}\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'IR_RawData'))
        os.makedirs(r'{}\{}\{}\{}\{}\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'DeconvolutionPicture'))
        os.makedirs(r'{}\{}\{}\{}\{}\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'RealtimePicture'))
        path_t = ExperimentNameFolder
        return path_t
            
    elif not os.path.exists(ExperimentNameFolder_1):
        os.makedirs(ExperimentNameFolder_1)
        os.makedirs(r'{}\{}\{}\{}\{}_1\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'IR_RawData'))
        os.makedirs(r'{}\{}\{}\{}\{}_1\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'DeconvolutionPicture'))
        os.makedirs(r'{}\{}\{}\{}\{}_1\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'RealtimePicture'))
        path_t = ExperimentNameFolder_1
        return path_t

    elif not os.path.exists(ExperimentNameFolder_2):
        os.makedirs(ExperimentNameFolder_2)
        os.makedirs(r'{}\{}\{}\{}\{}_2\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'IR_RawData'))
        os.makedirs(r'{}\{}\{}\{}\{}_2\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'DeconvolutionPicture'))
        os.makedirs(r'{}\{}\{}\{}\{}_2\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'RealtimePicture'))
        path_t = ExperimentNameFolder_2
        return path_t

    else:
        os.makedirs(ExperimentNameFolder_3)
        os.makedirs(r'{}\{}\{}\{}\{}_3\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'IR_RawData'))
        os.makedirs(r'{}\{}\{}\{}\{}_3\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'DeconvolutionPicture'))
        os.makedirs(r'{}\{}\{}\{}\{}_3\{}'.format(ParentFolder,YearTime, MonthTime,day,ExperimentName,'RealtimePicture'))
        path_t = ExperimentNameFolder_3
        return path_t
