import numpy as np


def CalConcentration(peakarea)->float:
    '''
    Explanation: this function is used to convert the peak area of monomer into its concentration
    peakarea = -1.9038*concentration^2 + 5.7166*concentration + 1.3501, R^2 = 0.9969
    '''

    """
    concentration  = 0.2657*peakarea + 0.0952, R^2 = 0.9998 

    """
    x = 0.2657*float(peakarea) +0.0952
    return(x)

def CalConversion(x:float, y:float)->float:
    '''
    Explanation: This function is used to calculate the conversion of monomer:
    x: the real time concentration of Monomer  
    y: the initial concentration of Monomer
    '''
    Conversion = (1 - (x/y))*100
    return(Conversion)



def integrate(x, y):
    area = np.trapz(y=y, x=x)
    return area
