##Author: Jianming Zeng

## Additional package goes here
import sys
import time
from graph import *

## temp
file = open("3D.inp", "r")
infoList=  []
cohNodeSet = None
cohElementSet = None

line = file.readline()
while line:
    ## Each if condition should be responsible of moving pointer to
    ## one line below their section
    # print line
    if "*Part" in line:
        partName = line.split("=")[1]
        myGraph = graph(partName)
        
        infoString = ""
        while "*End Part" not in line:
            infoString += line
            line = file.readline()
        infoList.append(infoString)

    elif "*Node" in line:
        infoList.append(line)
        line = file.readline() ## pointer moves a line down the file
        while "*" not in line:
            info = line.split()
            myGraph.addNode(info) 
            line = file.readline()

    elif "*Element" in line:
        infoList.append(line)
        line = file.readline() ## pointing to the first element
        while "*" not in line:
            info = line.split()
            myGraph.addElement(info)
            line = file.readline()

    elif "*Nset" in line:
        infoList.append(line)
        if "Set-1" in line:
            cohNodeSet = file.readline()
        line = file.readline()

    elif "*Elset" in line:
        infoList.append(line)
        if "Set-1" in line:
            cohElementSet = file.readline()
        line = file.readline()

    elif "*End Assembly" in line:
        infoList += [line, file.readlines()]
        line = None

    else:
        line = file.readline()



