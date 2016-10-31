## Author: Jianming Zeng

from copy import *


class Mesh:
        name = None
        
        nodes = None 
        nodeTracker = None
        nodeSet = None  ## record node set info directly from input file
        cohNode = None

        elementInfo = None
        elements = None
        elementsCopy = None
        elementSet = None
        edgeTracker = None
        edgeSet = None

        ##
        CZE = None
        surfaceCount = None
        surfList = None
        CPList = None
        


        
        def __init__(self):
                # Nodes
                self.nodes = dict()
                self.nodeTracker = dict()
                self.nodeSet = dict()
                self.nodeSet[1] = dict()
                self.nodeSet[2] = dict()
                self.cohNode = set()

                # Elements
                self.elements = dict()
                self.elementSet = dict()
                self.elementSet[1] = dict()
                self.elementSet[2] = dict()
                self.edgeTracker = dict()
                self.edgeSet = set()

                # CZE
                self.CZE = []
                self.surfaceCount = 1
                self.surfList = []
                self.CPList = []
                

##        def addPart(self, name):
##                self.nodes[name] = dict()
##
##        def addNode(self, part,aList):
##                ID = int(aList.pop(0))
##                self.nodes[part][ID] = tuple(aList)                        
##                ## establish a tracker for later
##                self.nodeTracker[ID] = []

        def addNode(self, aList):
                ID = int(aList.pop(0))
                for i in range(0, len(aList)):
                        aList[i] = float(aList[i].strip())                
                self.nodes[ID] = tuple(aList)                        
                ## establish a tracker for later
                self.nodeTracker[ID] = []


        def addElement(self, aList):
                ID = int(aList.pop(0))
                for i in range(0, len(aList)):
                        aList[i] = int(aList[i].strip())
                self.elements[ID] = tuple(aList)
                S1, S2, S3, S4 = self.CPE4Edges(aList)
                if S1 in self.edgeTracker:
                        self.edgeTracker[S1].append((str(ID), "S1"))
                else:
                        self.edgeTracker[S1] = [(str(ID), "S1")]
                if S2 in self.edgeTracker:
                        self.edgeTracker[S2].append((ID, "S2"))
                else:
                        self.edgeTracker[S2] = [(str(ID), "S2")]
                if S3 in self.edgeTracker:
                        self.edgeTracker[S3].append((str(ID), "S3"))
                else:
                        self.edgeTracker[S3] = [(str(ID), "S3")]
                if S4 in self.edgeTracker:
                        self.edgeTracker[S4].append((str(ID), "S4"))
                else:
                        self.edgeTracker[S4] = [(str(ID), "S4")]
                
                        
        def CPE4Edges(self, aList):
                A, B, C, D = aList
                if (A < B):
                    edge1 = (A, B)
                else:
                    edge1 = (B, A)
                if (B <C):
                    edge2 = (B, C)
                else:
                    edge2 = (C, B)
                if (C < D):
                    edge3 = (C, D)
                else:
                    edge3 = (D, C)
                if (A < D):
                    edge4 = (A, D)
                else:
                    edge4 = (D, A)
                return edge1, edge2, edge3, edge4



        def cohesiveFunction(self, ID):
                element = list(self.elementsCopy[ID])
                edges = list(self.CPE4Edges(element))
                for i in range(0,4):  ## update nodes first 
                        element[i] = self.updateNode(element[i])
                self.elements[ID] = tuple(element)

                for i in range(0,4):
                        edge = edges[i]
                        if (edge not in self.edgeSet and len(self.edgeTracker[edge]) == 2):
                                self.edgeSet.add(edge)
                        elif (edge in self.edgeSet):
                                ## edgeSet keeps track of elements within geometry
                                ## Surface
                                ## surface is in the form (ID, elementID, S#)
                                surf1, surf2 = self.edgeTracker[edge]
                                self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
                                self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
                                ## CP
                                self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
                                self.surfaceCount += 2
                                ## CZE
                                ## updating current elements is guaranteed two correct nodes
                                if (int(surf1[0]) == ID): 
                                        self.CZEhelper(element, i, list(self.elements[int(surf2[0])]), surf2[1])
                                else:
                                        self.CZEhelper(element, i, list(self.elements[int(surf1[0])]), surf1[1])

                                self.edgeSet.remove(edge)
                                        
        def cohesiveFunction2(self):
                for edge in self.edgeSet:
                        surf1, surf2 = self.edgeTracker[edge]
                        self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
                        self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
                        ## CP
                        self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
                        self.surfaceCount += 2
                        ## CZE
                        ## updating current elements is guaranteed two correct nodes
                        element = self.elements[int(surf1[0])]
                        edgeNum = int(surf1[1][1])
                        if edgeNum == 1: #S1
                                edge = element[0:2]
                        elif edgeNum == 2: #S2
                                edge = element[1:3]
                        elif edgeNum == 3: #S3
                                edge = element[2:4]
                        else: #S4
                                edge = [element[0]] + [element[3]]

                        element1 = self.elements[int(surf2[0])]
                        edgeNum1 = int(surf2[1][1])
                        if edgeNum1 == 1: #S1
                                edge1 = element1[0:2]
                        elif edgeNum1 == 2: #S2
                                edge1 = element1[1:3]
                        elif edgeNum1 == 3: #S3
                                edge1 = element1[2:4]
                        else: #S4
                                edge1 = [element1[0]] + [element1[3]]

                        if (self.nodes[int(edge[0])] == self.nodes[int(edge1[0])]):
                                edge1 = edge1[::-1]

##                        print(element, edgeNum, edge)
##                        print(element1, edgeNum1, edge1)
                        output = list(edge) + list(edge1)
                        for i in range(0,4): ##convert back to string before append to list
                                output[i] = str(output[i])
                        self.CZE.append(output[::-1])
                        
        def CZEhelper(self, element, edgeNum, otherElement, otherEdgeNum):
                # Local var
                edgeNum += 1
                edge = None
                otherEdge = None
                output = None
                                    
                if edgeNum == 1: #S1
                        edge = element[0:2]
                elif edgeNum == 2: #S2
                        edge = element[1:3]
                elif edgeNum == 3: #S3
                        edge = element[2:4]
                else: #S4
                        edge = [element[0]] + [element[3]]
                        
                if (otherEdgeNum == "S1"):
                        otherEdge = otherElement[0:2]
                elif (otherEdgeNum == "S2"):
                        otherEdge = otherElement[1:3]
                elif (otherEdgeNum == "S3"):
                        otherEdge = otherElement[2:4]
                else:
                        otherEdge = [otherElement[0]] + [otherElement[3]]

                ## CZE is in form [A, B, newB, newA]
                ## form [A, B, newA, newB] cause error
                if (self.nodes[int(edge[0])] == self.nodes[int(otherEdge[0])]):
                        otherEdge = otherEdge[::-1]
                
                output = edge + otherEdge
                for i in range(0,4): ##convert back to string before append to list
                        output[i] = str(output[i])
                self.CZE.append(output[::-1])
                      

        def cohesiveFunctionCrack(self, aList):
                sortList = []
                edgeList = []
                sortList.append(aList.pop(0))
                self.updateNode(sortList[0])
                while (aList):
                        
                        head = sortList[0]
                        edge1 = None
                        tail = sortList[-1]
                        edge2 = None
                        
                        for node in aList:
                                if node > head:
                                        edge1 = (head, node)
                                else:
                                        edge1 = (node, head)
                                if node > tail:
                                        edge2 = (tail, node)
                                else:
                                        edge2 = (node, tail)


                                if edge1 in self.edgeTracker:
                                        sortList = [node] + sortList
                                        edgeList = [edge1] + edgeList
                                        self.updateNode(node)
                                        aList.remove(node)
                                        break
                                elif edge2 in self.edgeTracker:
                                        sortList = sortList + [node]
                                        edgeList = edgeList + [edge2]
                                        self.updateNode(node)
                                        aList.remove(node)
                                        break
       
                
                for edge in edgeList:
                        surf1, surf2 = self.edgeTracker[edge]
                        self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
                        self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
                        ## CP
                        self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
                        self.surfaceCount += 2
                        ## CZE
                        nodeA = edge[0]
                        nodeB = edge[1]
                        updateA = self.nodeTracker[nodeA][-1]
                        updateB = self.nodeTracker[nodeB][-1]

                        if (sortList.index(nodeA) < sortList.index(nodeB)):## flip order
                                self.CZE.append([str(nodeB), str(nodeA), str(updateA), str(updateB)])
                        else:
                                self.CZE.append([str(nodeA), str(nodeB), str(updateB), str(updateA)])
                                edge = edge[::-1]

                        element1 = self.elements[int(surf1[0])]
                        element2 = self.elements[int(surf2[0])]
                        newElement = []
                        if (element1.index(edge[0]) < element1.index(edge[1])): ## same order
                                for i in range(0, len(element2)):
                                        if element2[i] == nodeA:
                                                newElement = newElement + [updateA]
                                        elif element2[i] == nodeB:
                                                newElement = newElement + [updateB]
                                self.elements[int(surf2[0])] = tuple(newElement)
                        else:
                                for i in range(0, len(element1)):
                                        if element1[i] == nodeA:
                                                newElement = newElement + [updateA]
                                        elif element1[i] == nodeB:
                                                newElement = newElement + [updateB]
                                self.elements[int(surf1[0])] = tuple(newElement)

                           
##                topElement = None
##                topID = None
##                for i in range(0, len(sortList) - 1):
##                        edge = None
##                        if (sortList[i] < sortList[i+1]):
##                                edge = (sortList[i], sortList[i+1])
##                        else:
##                                edge = (sortList[i+1], sortList[i])
##
##                        surf1, surf2 = self.edgeTracker[edge]
##                        self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
##                        self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
##                        ## CP
##                        self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
##                        self.surfaceCount += 2
##
##                        element1 = self.elements[int(surf1[0])]
##                        element2 = self.elements[int(surf2[0])]
##
##
##                        
##                        if topElement:
##                                if (set(topElement) - set(element1)) == 2:
##                                        topElement = list(element1)
##                                        topID = int(surf1[0])
##                                else:
##                                        topElement = list(element2)
##                                        topID = int(surf2[0])
##
##                                for i in range(0,4):
##                                        if topElement[i] in self.cohNode:
##                                                temp = topElement[i]
##                                                topElement[i] = self.updateNode(topElement[i])
##                                                self.cohNode.remove(temp)
##                                self.elements[topID] = topElement
##                                
##                                if topID == int(surf1[0]):
##                                        cze1 = list(set(topElement) - set(element1))
##                                        cze2 = list(set(element1) - set(topElement))
##                                        cze = cze1[::-1] + cze2
##                                        for i in range(0, len(cze)):
##                                                cze[i] = str(cze[i])
##                                        self.CZE.append(cze)
##                                else:
##                                        
##                                        cze1 = list(set(topElement) - set(element2))
##                                        cze2 = list(set(element2) - set(topElement))
##                                        cze = cze1[::-1] + cze2
##                                        for i in range(0, len(cze)):
##                                                cze[i] = str(cze[i])
##                                        self.CZE.append(cze)
##                                
##
##                        else:
##                                topElement = list(element1)
##                                topID = int(surf1[0])
##                                for i in range(0,4):
##                                        temp = topElement[i]
##                                        topElement[i] = self.updateNode(topElement[i])
##                                        self.cohNode.remove(temp)
##                                self.elements[topID] = topElement
##                                cze1 = list(set(topElement) - set(element1))
##                                cze2 = list(set(element1) - set(topElement))
##                                cze = cze1[::-1] + cze2
##                                for i in range(0, len(cze)):
##                                        cze[i] = str(cze[i])
##                                self.CZE.append(cze)
##                        ## First find out which element is on top, intially element1 is on top
##                        if topElement:
##                                if len(topELement - element1) == 2:
##                                        topElement = element1
##                                        topID = int(surf1[0])
##                                else:
##                                        topELement = element2
##                                        topID = int(surf2[0]
##
##                                ## Consider the order of nodes
##                                element = []
##                                for i in range(0, 4):
##                                        if topElement[i] in edge:
##                                                element = element + self.updateNode(topElement[i])
##                                        else:
##                                                element = element + [topElement[i]]
##                                self.elements[topID] = element
##                        else:
##                                topElement = element1
                                

                                
##        def CZEcrackHelper(self, edge, ID1, ID2):
                
                                        
        
        def updateNode(self, node):
                if node in self.cohNode:
                        ID = len(self.nodes.keys())+1
                        self.nodes[ID] = self.nodes[node]
                        self.nodeTracker[node].append(ID)
                else:
                        self.cohNode.add(node)
                        return node
                return ID
                
                



        def copyElements(self):
                self.elementsCopy = deepcopy(self.elements)
                
                
                
                
