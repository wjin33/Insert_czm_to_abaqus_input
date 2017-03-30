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
infoList2 = []
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
while "*End Instance" not in line:

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
    else:
        infoList.append(line)
        line = file.readline()

infoList2 = file.readlines()

############################################################################################################
"""
At this point, we should have all the information store inside the graph. 
Based on user's desire, choose the appropriate model inside graph object.
Ex. Homogeneous function. Call graph.homogeneous(set). This call will create the homogeneous
model based on the provided set. The provided set is the place where cohesive zone elements go
"""
############################################################################################################
start, end, step = cohNodeSet.split(",")
start = int(start.strip())
end = int(end.strip())
step = int(step.strip())
myGraph.homogeneous(start, end, step)

# print("Cohesive Zone Element")
# for i in myGraph.cohList:
#     print i
# print("Defining Surface List")
# for i in myGraph.surfList:
#     print i
# print("Contact property: Surface pair")
# for i in myGraph.CPList:
#     print i
############################################################################################################
"""

"""
############################################################################################################
## writing input file ##
output = open("return.inp", "w")
line = infoList.pop(0)
while "*End Instance" not in line:
    if "*Node" in line:
        output.write(str(line))
        for i in range(1, myGraph.nodes + 1): 
            node = myGraph.nodeMap[i]
            temp = str(i) + ", " + str(node.x) + ", " + str(node.y) + ", " + str(node.z)
            output.write(temp + "\n")  
        line = infoList.pop(0)
    elif "*Element" in line:
        output.write(str(line))
        for i in range(1, myGraph.elements + 1):
            element = myGraph.elementMap[i]
            output.write(str(i) + ", " + element.getString())

        output.write("*Element, type=COH3D8 \n")
        for i in range(0, len(myGraph.cohList)):
            output.write(str(i+myGraph.elements+1) + ", "
                + ', '.join(str(x) for x in myGraph.cohList[i]) + "\n") 
        line = infoList.pop(0)
    elif "*Nset, nset=Set-1" in line:
        output.write(line)
        output.write("1, " + str(myGraph.nodes) + ", 1\n")
        line = infoList.pop(0)

    elif "*Elset, elset=Set-1" in line:
        output.write(line)
        output.write("1, " + str(myGraph.elements) + ", 1\n")   
        line = infoList.pop(0)
        output.write("*Elset, elset=CZE, generate\n")
        output.write( 
            str(myGraph.elements+1) + ", " +
            str(myGraph.elements+len(myGraph.cohList)) + ", 1\n"
            ) 
    else:
        output.write(line)
        try: 
            line = infoList.pop(0)
        except:
            break

output.write("*End Instance")

line = infoList2.pop(0)
while line:
    if "*Nset, nset=Set-1" in line:
        output.write(line)
        output.write("1, " + str(myGraph.nodes) + ", 1\n")
        line = infoList2.pop(0)

    elif "*Elset, elset=Set-1" in line:
        output.write(line)
        output.write("1, " + str(myGraph.elements) + ", 1\n")   
        line = infoList2.pop(0)

    elif "*End Assembly" in line:
        for i in range(0, len(myGraph.surfList)):
            surface = myGraph.surfList[i]
            output.write("*Surface, type=ELEMENT, name=" + surface[0] + "\n")
            output.write("Element" + surface[1] + ", " + surface[2] + "\n")
        line = infoList2.pop(0)
    elif "** BOUNDARY CONDITIONS" in line:
        output.write("*Surface Interaction, name=IntProp-1\n1.,\n*Friction\n0.,\n*Surface Behavior, pressure-overclosure=HARD\n")
        for i in range(0, len(myGraph.CPList)):
            output.write("*Contact Pair, interaction=IntProp-1, small sliding, type=SURFACE TO SURFACE, adjust=0.0\n")
            output.write(myGraph.CPList[i][0] + ", " + myGraph.CPList[i][1] + "\n")
        for line in infoList2:
            output.write(line)
        line = None
    else:
        output.write(line)
        try:
            line = infoList2.pop(0)
        except:
            line = None
