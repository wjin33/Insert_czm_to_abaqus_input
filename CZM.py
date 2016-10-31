##Author: Jianming Zeng

## Additional package goes here
import sys
from Mesh import *
from tkinter import *
import time

##########################################################
## GUI variables go here
##########################################################
nodeType = None
elementType = None
outputName = None
filename = None
cohElementSet = None
CZMMaterialName = None
Mode = None
ENUM = ["ALL", "part", "Along crack"]


##########################################################
## Ask for input, continue loop until a file is found or 5 attempts is reached##
attempt = 5
while True and attempt > 0: 
        try:
            filename = input("File Name: ")
            outputName = input("Output Name:")
            cohElementSet = input("CZE set:")
            CZMMaterialName = input ("CZM material name:")
            for i in range(0, len(ENUM)):
                    print(str(i+1) + ". " + ENUM[i])
        
            Mode = int(input("Choose a function, input the integer:"))
            file = open(filename, 'r')
            break
        
                 
        except FileNotFoundError:
            attempt -= 1
            if attempt == 0:
                print("Python exit.")
                sys.exit()
            print("No such file in the directory, try again(letter case and file type sensitive).")
            print("You have {key} attempts left".format(key = attempt))
###########################################################
##print("New implementation")
##startTime = time.time()
##print("start time: " + str(startTime))
#### LOOP SET-UP ####
## Local instantce set-up

assembly = "*Assembly, name="
part = "*Part, name="
element = "*Element, type="
nset = "*Nset, nset="
elset = "*Elset, elset="
section = "*Solid Section, "
#####
##string1 = ""  ## store Nset elset
## cohesize zone elemts store here
string2 = "" ## store section
string3 = "" ## surface
flag  = 0

#####

#### READ ####
############################################################
#### LOOP THROUGH file until Assembly  ####
mesh = Mesh()
current = file.readline()
while (assembly not in current):
        if part in current:
                partName = current.split("=")[1]
                mesh.name = partName
##                mesh.addPart(partName)
                file.readline()
                current = file.readline()
                line =current.strip().split(",")
                while(len(mesh.nodes.keys())+1 == int(line[0])):
                        mesh.addNode(line)
                        current =file.readline()
                        if ("*" in current):
                                break
                        else:
                                line = current.strip().split(",")
                
        elif element in current:
                mesh.elementInfo = current
                current = file.readline()
                line = current.strip().split(",")
                while (len(mesh.elements.keys()) + 1 ==int(line[0])):
                        mesh.addElement(line)
                        current = file.readline()
                        if ("*" in current):
                                break
                        else:
                                line = current.strip().split(",")
        ## Element set info may be useful to be put into a dict for creating CZE!!!!!
        ## do a check if CZEsetInfo in here or later 
        elif (nset in current):
                flag = 1
                name = current.split("=")[1].split(",")[0]
                if "generate" in current:
                        mesh.nodeSet[1][name] = current + file.readline()
                        current = file.readline()
                else:
                        currentString = current
                        current = file.readline()
                        while("*" not in current):
                                currentString += current
                                current = file.readline()
                        mesh.nodeSet[1][name] = currentString
        elif(elset in current):
                flag = 1
                name = current.split("=")[1].split(",")[0]
                if "generate" in current:
                        mesh.elementSet[1][name] = current + file.readline()
                        current = file.readline()
                else:
                        currentString = current
                        current = file.readline()
                        while("*" not in current):
                                currentString += current
                                current = file.readline()
                        mesh.elementSet[1][name] = currentString
        elif ("*End Part" in current):
                string2 += "** Section: cohe\n" + "*Cohesive Section, elset=CZE, material=" +CZMMaterialName+ ", response=TRACTION SEPARATION\n1,\n"
                string2 += current
                current = file.readline()
        elif ("*" in current and flag):
                string2 += current
                current = file.readline()
        else:
                current = file.readline()
## Cohesive Section ##
############################################################
#### Assembly ####
##Advance till meeting the first nset ##
while (nset not in current):
        if ("*Instance, name=" in current):
                instance = current.split("=")[1].split(",")[0]
        string2 += current
        current = file.readline()

##Advance till the end of Assembly ##
while ("*End Assembly" not in current):
        if (nset in current):
                name = current.split("=")[1].split(",")[0]
                if "generate" in current:
                        mesh.nodeSet[2][name] = current + file.readline()
                        current = file.readline()
                else:
                        currentString = current
                        current = file.readline()
                        while("*" not in current):
                                currentString += current
                                current = file.readline()
                        mesh.nodeSet[2][name] = currentString
        elif(elset in current):
                name = current.split("=")[1].split(",")[0]
                if "generate" in current:
                        mesh.elementSet[2][name] = current + file.readline()
                        current = file.readline()
                else:
                        currentString = current
                        current = file.readline()
                        while("*" not in current):
                                currentString += current
                                current = file.readline()
                        mesh.elementSet[2][name] = currentString
        else:
                string3 += current
                current = file.readline()
##print(mesh.nodeSet[2])
##print(mesh.elementSet[2])
## Cohesive Zone Elements, Surface and Contact Property
if (Mode == 1):
##        if (cohElementSet):
        mesh.copyElements()
        elementSetInfo = mesh.elementSet[1][cohElementSet]
        if "generate" in elementSetInfo:
                start, stop, step = elementSetInfo.split()[-3:]
                start = start.split(",")[0]
                stop = stop.split(",")[0]
                if int(step) ==1:
                        for ID in range(int(start), int(stop)+1, int(step)):
                                mesh.cohesiveFunction(ID)
        else:
                aList = elementSetInfo.split()[3:]
                for i in range(0, len(aList)):
                        if "," in aList[i]:
                                aList[i] = aList[i][0:-1]
                        aList[i] = int(aList[i])
                for ID in aList:
                        mesh.cohesiveFunction(ID)
elif (Mode == 2):
        mesh.copyElements()
        
        elementSetInfo = mesh.elementSet[1][cohElementSet]
        nodeSetInfo = mesh.nodeSet[2]["Boundary"]
        
        
        aList = []

        if "generate" in nodeSetInfo:
                start, stop, step = nodeSetInfo.split()[-3:]
                start = start.split(",")[0]
                stop = stop.split(",")[0]
                if int(step) == 1:
                        for ID in range(int(start), int(stop)+1, int(step)):
                                mesh.cohNode.add(ID)
        else:
                for i in nodeSetInfo.split(','):
                        try:
                                mesh.cohNode.add(int(i))
                        except:
                                for j in i.split("\n"):
                                        try:
                                                mesh.cohNode.add(int(j.strip()))
                                        except:
                                                pass

        if "generate" in elementSetInfo:
                start, stop, step = elementSetInfo.split()[-3:]
                start = start.split(",")[0]
                stop = stop.split(",")[0]
                if int(step) ==1:
                        for ID in range(int(start), int(stop)+1, int(step)):
                                mesh.cohesiveFunction(ID)
        else:
                aList = elementSetInfo.split()[3:]
                for i in range(0, len(aList)):
                        if "," in aList[i]:
                                aList[i] = aList[i][0:-1]
                        aList[i] = int(aList[i])
                for ID in aList:
                        mesh.cohesiveFunction(ID)
                        
        mesh.cohesiveFunction2()
elif (Mode == 3):
        nodeSetInfo = mesh.nodeSet[2][cohElementSet]
        aList = []
        if "generate" in nodeSetInfo:
                start, stop, step = nodeSetInfo.split()[-3:]
                start = start.split(",")[0]
                stop = stop.split(",")[0]
                if int(step) == 1:
                        for ID in range(int(start), int(stop)+1, int(step)):
                                aList += [ID]
                                mesh.cohNode.add(ID)
        else:
                aList = nodeSetInfo.split()[3:]
                for i in range(0, len(aList)):
                        if "," in aList[i]:
                                aList[i] = aList[i][0:-1]
                        aList[i] = int(aList[i])
                        mesh.cohNode.add(aList[i])
        mesh.cohesiveFunctionCrack(aList)

                
        
        
############################################################
## writing input file ##
output = open(outputName+".inp", "w")
## Nodes ##
output.write("*Part, name=" + mesh.name ) ## part could be more than one in the future
output.write("*Node\n")
for i in range(1, len(mesh.nodes.keys())+ 1):
        temp = str(i)
        for j in mesh.nodes[i]:
                temp += ", " + str(j)
        output.write(temp + "\n")
        
## Elements ##
output.write(mesh.elementInfo)
for i in range(1,len(mesh.elements.keys())+1):
        temp = str(i)
        for j in mesh.elements[i]:
                temp += ", " + str(j)
        output.write(temp + "\n")
output.write("*Element, type=COH2D4 \n")
for i in range(0, len(mesh.CZE)):
        temp = ", ".join(mesh.CZE[i])
        output.write(str(i+1+len(mesh.elements))+ ", " + str(temp )+  "\n")

## Nset, Elset, Cohesive Zone##
for key in mesh.nodeSet[1].keys():
        output.write(mesh.nodeSet[1][key])
for key in mesh.elementSet[1].keys():
        output.write(mesh.elementSet[1][key])
output.write("*Elset, elset=CZE, generate\n")
output.write(str(len(mesh.elements)+1 ) + ", " + str(len(mesh.elements) + len(mesh.CZE))+ ",  1\n")
output.write(string2)
## Assembly Nset, Elset, Surface ##
for key in mesh.nodeSet[2].keys():
        line = mesh.nodeSet[2][key]
        if "generate" in line:
                output.write(''.join(line.split()[0:-3]) + '\n')
                
                start, stop, step = line.split()[-3:]
                start = start.split(",")[0]
                stop = stop.split(",")[0]
                length = 0
                for i in range(int(start), int(stop), int(step)):
                        output.write(str(i))
                        if (mesh.nodeTracker[i] != []):
                                for j in mesh.nodeTracker[i]:
                                        if (length >= 40):
                                                output.write("\n")
                                                length = 0
                                        output.write(  ", " + str(j))
                                        length += len( ", "+ str(j))           
                                output.write( ", ")
                        else:
                                output.write(",")
                        if (length >= 40):
                                output.write("\n")
                                length = 0
                output.write("\n")
        else:
                length = 0
                output.write(line.split('\n')[0] + "\n")
                
                for i in ",".join(line.split('\n')[1:]).split(","):
                        if i == "" or i == ' ':
                                continue
                        output.write(i)
                        if (mesh.nodeTracker[int(i)] != []):
                                for j in mesh.nodeTracker[int(i)]:
                                        output.write(  ", " + str(j))
                                        length += len( ", "+ str(j))
                                output.write( ", ")
                        else:
                                output.write(",")
                        if (length >= 40):
                                output.write("\n")
                                length = 0
                output.write("\n")
for key in mesh.elementSet[2].keys():
        output.write(mesh.elementSet[2][key])
output.write(string3)
## Surface and contact property
for i in range(1, len(mesh.elements)+1):
        output.write("*Elset, elset=Element" + str(i)+", instance=" + instance +'\n' + str(i) + '\n')
for i in mesh.surfList:
        output.write("*Surface, type=ELEMENT, name=" + str(i.pop(0))+ "\n")
        output.write("Element"+ str(i.pop(0)) + ", " + str(i.pop(0))+ '\n')

## End Assembly ##
output.write(current)
current = file.readline()
while (current):
        if "*Surface Interaction, name=" in current:
                contact = current.split("=")[1].split('\n')[0]
        if ("*Surface Behavior," in current):
                output.write(current)
                for i in mesh.CPList:
                        output.write("*Contact Pair, interaction="+contact+", small sliding, type=SURFACE TO SURFACE, adjust=0.0\n")
                        output.write(", ".join(i))
                        output.write("\n")

        else:
                output.write(current)
        current = file.readline()
        



######## DEBUG ###########
##print(mesh.nodes[partName].keys())
##for key in mesh.nodes[partName].keys():
##        print(mesh.nodes[key])
##print(mesh.nodes[partName])
##print(mesh.nodeTracker.keys())
##print(mesh.elements.keys())
##for key in mesh.nodeSet.keys():
##        print(mesh.nodeSet[key])
##for key in mesh.elementSet.keys():
##        print(mesh.elementSet[key])
##print(mesh.nodeSet.keys())
##print(mesh.elementSet.keys())
##print(mesh.edgeTracker.keys())
##for key in mesh.edgeTracker.keys():
##        print(mesh.edgeTracker[key])
##print(len(mesh.nodes))
##print(len(mesh.elements))
##print(len(mesh.CZE))
##print(mesh.nodeSet[2]["Set-1"])
##print(mesh.edgeSet)


file.close()
output.close()
