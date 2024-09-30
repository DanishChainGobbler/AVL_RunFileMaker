"""

This script is designed to read an input file, and generate a .run file for use
with Athena Vortex Lattice (AVL).

Visit https://web.mit.edu/drela/Public/web/avl/ for more information on AVL.

Author: Dane Jackson

Created: 09/26/2024

"""

# import packages

import os
import numpy as np
from pathlib import Path

# define paths and files

dir_path = os.path.dirname(os.path.realpath(__file__))
inFile = "input.csv"
templateFile = Path(str(dir_path) + "/data/template.run")
atmosFile = templateFile = Path(str(dir_path) + "/data/stdatmos.csv")
outFile = "cases.run"

# initialize lists

varNames = []
alt = []
M = []
alpha = []
Beta = []
tempLines = []
altList = []
tempList = []
pList = []
rhoList = []
aList = []
muList = []
caseatmos = []

# Create output messages

inpBegin = "Opening input file and reading variables"
inpComplete = "Input cases read successfully"
tempRead = "Reading template run file"

def getAtmos(alt):

    """
    This function interpolates standard atmospheric conditions
    for the given altitude
    """

    retCond = []

    retCond.append(np.interp(alt,altArray,tempArray))
    retCond.append(np.interp(alt,altArray,pArray))
    retCond.append(np.interp(alt,altArray,rhoArray))
    retCond.append(np.interp(alt,altArray,aArray))
    retCond.append(np.interp(alt,altArray,muArray))

    return retCond # Returns list of floats containing standard atmospheric
                   # conditions at provided altitude

# Reads standard atmospheric data for interpolation

with open(atmosFile, 'r') as aF:
    for i, line in enumerate(aF):
        if i > 2:
            templine = line.split(',')
            altList.append(templine[0])
            tempList.append(templine[1])
            pList.append(templine[2])
            rhoList.append(templine[3])
            aList.append(templine[4])
            muList.append(templine[5])

# Converts atmospheric data lists into arrays and deletes lists

altArray = np.asarray(altList, dtype = np.float32)
tempArray = np.asarray(tempList, dtype = np.float32)
pArray = np.asarray(pList, dtype = np.float32)
rhoArray = np.asarray(rhoList, dtype = np.float32)
aArray = np.asarray(aList, dtype = np.float32)
muArray = np.asarray(muList, dtype = np.float32)

del altList, tempList, pList, rhoList, aList, muList

# Reads input file and creates lists of variables for all cases

print(inpBegin)
with open(inFile, 'r') as iF:
    for i, line in enumerate(iF):
        if i == 0:
            templine = line.split()
            for j, k in enumerate(templine):
                varNames.append(templine[j])
        else:
            print("Reading inputs for case " + str(i) + " of " +
                str(len(varNames)))
            templine = line.split(',')
            alt.append(templine[0])
            M.append(templine[1])
            alpha.append(templine[2])
            Beta.append(templine[3].removesuffix('\n'))

print(inpComplete)

# Reads template run file to rebuild with case data

print(tempRead)

with open(templateFile, 'r') as tF:
    for line in tF:
        tempLines.append(line)
        caseAtmos = getAtmos(alt[0])
print('Template format loaded')
#with open(outFile, 'w') as oF:
    #for i in len(alt):
        #for i, line in enumerate(tempLines):
        # Modify each

