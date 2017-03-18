"""Author: Jianming Zeng"""

############################################################################################################
"""
Package import goes here
"""
############################################################################################################
import sys
import time
from graph import *


############################################################################################################
"""
Variable declaration
Although python doesn't require predefine variable, it's a good practice to 
initiate here, and also good for debuging 
"""
############################################################################################################

## temp
file = open("3D.inp", "r")
infoList=  []
cohNodeSet = None
cohElementSet = None

line = file.readline()
############################################################################################################
"""
This section is for extracting information from input text file.
Each if statement will check for specific location and store the 
information into the graph(data structure) for later Use
"""
############################################################################################################
while line:

    ################################

    ################################
    if "*Part" in line:
        partName = line.split("=")[1]
        myGraph = graph(partName)
        
        infoString = ""
        while "*End Part" not in line:
            infoString += line
            line = file.readline()
        infoList.append(infoString)


    ################################

    ################################
    elif "*Node" in line:
        infoList.append(line)
        line = file.readline() ## pointer moves a line down the file
        while "*" not in line:
            info = line.split()
            myGraph.addNode(info) 
            line = file.readline()


    ################################

    ################################
    elif "*Element" in line:
        infoList.append(line)
        line = file.readline() ## pointing to the first element
        while "*" not in line:
            info = line.split()
            myGraph.addElement(info)
            line = file.readline()


    ################################

    ################################
    elif "*Nset" in line:
        infoList.append(line)
        if "Set-1" in line:
            cohNodeSet = file.readline()
        line = file.readline()


    ################################

    ################################
    elif "*Elset" in line:
        infoList.append(line)
        if "Set-1" in line:
            cohElementSet = file.readline()
        line = file.readline()


    ################################

    ################################
    elif "*End Assembly" in line:
        infoList += [line, file.readlines()]
        line = None


    ################################

    ################################
    else:
        line = file.readline()

############################################################################################################
"""
At this point, we should have all the information store inside the graph. 
Based on user's desire, choose the appropriate model inside graph object.
Ex. Homogeneous function. Call graph.homogeneous(set). This call will create the homogeneous
model based on the provided set. The provided set is the place where cohesive zone elements go
"""
############################################################################################################




############################################################################################################
"""

"""
############################################################################################################


