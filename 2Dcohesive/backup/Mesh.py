## Author: Jianming Zeng

from copy import *
from treeNode import *
from graphNode import *

class Mesh:
        name = None
        
        nodes = None 
        nodeTracker = None
        nodeSet = None  ## record node set info directly from input file
        cohNode = None
        nodeTree = None

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
            # tree = self.makeTree(aList)
            root = int(6)
            joinList = []
            self.makeGraph(aList)
            fringe = [root]
            visited = set()
            change = set()
            unchange = set()
            # cycle = 0
            while fringe:

                # cycle += 1
                newFringe = []
                for parent in fringe:
                    
                    parentNode = self.nodeTree[parent]

                    ## Update mechanics
                    for childNode in parentNode.neighbours:
                        if childNode.ID in visited:
                            continue
                        else:
                            if childNode.number == 1:
                                continue
                            newFringe += [childNode.ID]

                    if parentNode.number > 2:
                        joinList += [parent]
                        visited.add(parent)
                    ## Edge point 
                    elif parentNode.number == 1:
                        childNode = parentNode.neighbours[0]
                        if parent > childNode.ID:
                            edge = childNode.ID, parent
                        else:
                            edge = parent, childNode.ID
                        


                        surf1, surf2 = self.edgeTracker[edge]
                        element1 = list(self.elements[int(surf1[0])])
                        element2 = list(self.elements[int(surf2[0])])
                        nodeA = edge[0]
                        nodeB = edge[1]
                        newNodeA = self.updateNode(nodeA)
                        newNodeB = self.updateNode(nodeB)
                        if len(change) == 0:
                            change = change|set(element1) - set(edge)
                            unchange = unchange|set(element2) - set(edge)
                            

                        # Test memebership
                        if self.isInside(element1, change):
                            change = change|set(element1) - set(edge)
                            element1 = self.updateElement(element1, nodeA, newNodeA, nodeB, newNodeB)
                            self.elements[int(surf1[0])] = tuple(element1)
                        else:
                            change = change|set(element2) - set(edge)
                            element2 = self.updateElement(element2, nodeA, newNodeA, nodeB, newNodeB)
                            self.elements[int(surf2[0])] = tuple(element2)

                        
                        ## Surface
                        self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
                        self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
                        ## CP
                        self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
                        self.surfaceCount += 2  

                        self.CZE.append([str(nodeA), str(nodeB), str(newNodeB), str(newNodeA)])

                        visited.add(childNode.ID)

                    ## 
                    elif parentNode.number == 2:
                        ## since there are only two neightbours and one doesn't work
                        ## safe to assume 

                        if parentNode.neighbours[0].ID in visited:
                            childNode = parentNode.neighbours[1]
                        else:
                            childNode = parentNode.neighbours[0]

                        
                        ## establish edge
                        if parent > childNode.ID:
                            edge = childNode.ID, parent
                        else:
                            edge = parent, childNode.ID

                        ## two scenarios 
                        ## either it's the start of a new crack
                        ## or it's in the middle of the crack
                        ## testing is to check if the current parent node in cohNode
                        ## get the two surface
                        surf1, surf2 = self.edgeTracker[edge]
                        element1 = list(self.elements[int(surf1[0])])
                        element2 = list(self.elements[int(surf2[0])])
                        nodeA = edge[0]
                        nodeB = edge[1]



                        # if (nodeA in visited and nodeB in visited):
                        #     continue
                        # elif nodeA in visited:
                        #     newNodeA = self.nodeTracker[nodeA][-1]
                        #     newNodeB = self.updateNode(nodeB)
                        # elif nodeB in visited:
                        #     newNodeA = self.updateNode(nodeA)
                        #     newNodeB = self.nodeTracker[nodeB][-1]
                        # else:
                        #     newNodeA = self.updateNode(nodeA)
                        #     newNodeB = self.updateNode(nodeB)
                        if nodeA in visited and nodeB in visited:
                            newNodeA = self.nodeTracker[nodeA][-1]
                            newNodeB = self.nodeTracker[nodeB][-1]
                        elif nodeA in visited and nodeB not in visited:
                            newNodeA = self.nodeTracker[nodeA][-1]
                            newNodeB = self.updateNode(nodeB)
                        elif nodeA not in visited and nodeB in visited:
                            newNodeA = self.updateNode(nodeA)
                            print nodeB, visited
                            
                            newNodeB = self.nodeTracker[nodeB][-1]
                        # else:
                        #     newNodeA = self.updateNode(nodeA)
                        #     newNodeB = self.updateNode(nodeB)



                        if self.isInside(element1, change):
                            change = change|set(element1) - set(edge)
                            unchange = unchange|set(element2) - set(edge)
                            element1 = self.updateElement(element1, nodeA, newNodeA, nodeB, newNodeB)
                            self.elements[int(surf1[0])] = tuple(element1)
                        else:
                            change = change|set(element2) - set(edge)
                            uncahnge = unchange|set(element2) - set(edge)
                            element2 = self.updateElement(element2, nodeA, newNodeA, nodeB, newNodeB)
                            self.elements[int(surf2[0])] = tuple(element2)
                        
                        ## Surface
                        self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
                        self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
                        ## CP
                        self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
                        self.surfaceCount += 2  

                        self.CZE.append([str(nodeA), str(nodeB), str(newNodeB), str(newNodeA)])
                        visited.add(childNode.ID)
                    ## update visited here to make sure no revisit
                    
                if len(newFringe) != 0: 
                    fringe = newFringe
                else:
                    fringe = None


            
            for node in joinList:
                check = True
                base1 = None
                base2 = None
                for neighbour in self.nodeTree[node].neighbours:
                    ID = neighbour.ID
                    if node > ID:
                        edge = ID, node
                    else:
                        edge = node, ID
                    surf1, surf2 = self.edgeTracker[edge]
                    element1 = list(self.elements[int(surf1[0])])
                    element2 = list(self.elements[int(surf2[0])])
                    if len(set(element1).intersection(set(element2))) == 0:
                        base1 = element1
                        base2 = element2
                        break

                for neighbour in self.nodeTree[node].neighbours:
                    ID = neighbour.ID
                    if node > ID:
                        edge = ID, node
                    else:
                        edge = node, ID

                    surf1, surf2 = self.edgeTracker[edge]
                    ## Surface
                    self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
                    self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
                    ## CP
                    self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
                    self.surfaceCount += 2  
                    element1 = list(self.elements[int(surf1[0])])
                    element2 = list(self.elements[int(surf2[0])])

                    if len(set(element1).intersection(set(element2))) == 0:
                        if check:
                            check = False
                            continue   

                    if self.nodeTree[ID].neighbours[0].ID == node:
                        child = self.nodeTree[ID].neighbours[1].ID
                    else:
                        child = self.nodeTree[ID].neighbours[0].ID
                    if child > ID:
                        edge1 = ID, child
                    else:
                        edge1 = child, ID
                    surf3, surf4 = self.edgeTracker[edge1]
                    element3 = list(self.elements[int(surf3[0])])
                    element4 = list(self.elements[int(surf4[0])])

                    if len(set(element1).intersection(set(element3))) == 2 or len(set(element1).intersection(set(element4))) == 2:
                        ## Element1 is unchanged
                        for i in range(0, len(element2)):
                            if element2[i] in self.nodeTracker.keys() and self.nodeTracker[element2[i]] != []:
                                if element2[i] == node:
                                    continue
                                element2[i] = self.nodeTracker[element2[i]][-1]   


                    elif len(set(element2).intersection(set(element4))) == 2 or len(set(element2).intersection(set(element3))) == 2:
                        ## Element2 is unchanged
                        for i in range(0, len(element1)):
                            if element1[i] == node:
                                continue
                            if element1[i] in self.nodeTracker.keys() and self.nodeTracker[element1[i]] != []:
                                element1[i]  = self.nodeTracker[element1[i]][-1]

                
                    # print element1, element2
                    # if self.isNeighbour(element1, base1, node):
                    #     # # element1[element1.index(node)] = self.nodeTracker[node][-1]
                    #     # if node not in base1:
                    #     #     element1[element1.index(node)] = self.nodeTracker[node][-1]
                    #     element2[element2.index(node)] = self.updateNode(node)

                    # # elif self.isNeighbour(element1, base2, node):
                    # #     if node not in base2:
                    # #         element1[element1.index(node)] = self.nodeTracker[node][0]

                    # elif self.isNeighbour(element2, base1, node):
                    #     if node not in base1:
                    #         element2[element2.index(node)] = self.nodeTracker[node][-1]
                    #     element1[element1.index(node)] = self.updateNode(node)
                    # elif self.isNeighbour(element2, base2, node):
                    #     if node not in base2:
                    #         element2[element2.index(node)] = self.nodeTracker[node][0]
                    # else:
                    #     if node in element1:
                    #         element1[element1.index(node)] = self.updateNode(node)
                    #     elif node in element2:
                    #         element2[element2.index(node)] = self.updateNode(node)

                    # # print element1, element2

                    # self.elements[int(surf1[0])] = tuple(element1)
                    # self.elements[int(surf2[0])] = tuple(element2)


                    nodeA, nodeB = edge
                    ## element1
                    if nodeA in element1:
                        nodeC = nodeA
                    else:
                        for i in element1:
                            if i in self.nodeTracker[nodeA]:
                                nodeC = i
                    if nodeB in element1:
                        nodeD = nodeB
                    else:
                        for i in element1:
                            if i in self.nodeTracker[nodeB]:
                                nodeD = i
                    #element2
                    if nodeA in element2:
                        nodeE = nodeA
                    else:
                        for i in element2:
                            if i in self.nodeTracker[nodeA]:
                                nodeE = i
                    if nodeB in element2:
                        nodeF = nodeB
                    else:
                        for i in element2:
                            if i in self.nodeTracker[nodeB]:
                                nodeF = i
                    # for i in element1:
                    #     if i in self.nodeTracker.keys() and len(self.nodeTracker[i]) == 0:
                    #         continue
                    #     CZE += [str(i)]
                    # for i in element2:
                    #     if i in self.nodeTracker.keys() and len(self.nodeTracker[i]) == 0:
                    #         continue
                    #     CZE += [str(i)]
                    self.CZE.append([str(nodeC), str(nodeD), str(nodeF), str(nodeE)])
                    # print ([str(nodeC), str(nodeD), str(nodeF), str(nodeE)])
                    # update all the nodes within the element to its latest.  
                    # Element1 First


        def isNeighbour(self, element1, element2, node):
            i = 0
            for nodeA in element1:
                if nodeA == node:
                    continue
                if nodeA in element2:
                    i += 1
            if i >= 1:
                return True
            return False

        def isInside(self, element, group):
            for node in element:
                if node in group:
                    return True
            return False


            # fringe = [root]
            # while fringe:
            #     newFringe = []
            #     for parent in fringe:
            #         children = parent.child
            #         newFringe += children
            #         if (parent.num == 1):
            #             if parent.ID > children[0].ID:
            #                 edge = (children[0].ID, parent.ID)
            #             else:
            #                 edge = (parent.ID, children[0].ID)
            #             surf1, surf2 = self.edgeTracker[edge]
            #             element1 = list(self.elements[int(surf1[0])])
            #             element2 = list(self.elements[int(surf2[0])])
            #             change = change|set(element1) - set(edge)
            #             unchange = unchange|set(element2) - set(edge)
            #             nodeA = edge[0]
            #             nodeB = edge[1]
            #             newNodeA = self.updateNode(nodeA)
            #             newNodeB = self.updateNode(nodeB)
            #             element1 = self.updateElement(element1, nodeA, newNodeA, nodeB, newNodeB)
            #             self.elements[int(surf1[0])] = tuple(element1)

            #             self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
            #             self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
            #             ## CP
            #             self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
            #             self.surfaceCount += 2  
            #             self.CZE.append([nodeA, nodeB, newNodeB, newNodeA])


            #         elif (parent.num == 2):
            #             print k
            #             print(parent.ID)
            #             if parent.ID > children[0].ID:
            #                 edge = (children[0].ID, parent.ID)
            #             else:
            #                 edge = (parent.ID, children[0].ID)
            #             surf1, surf2 = self.edgeTracker[edge]
            #             element1 = list(self.elements[int(surf1[0])])
            #             element2 = list(self.elements[int(surf2[0])])
            #             nodeA = edge[0]
            #             nodeB = edge[1]
            #             newNodeA = self.updateNode(nodeA)
            #             newNodeB = self.updateNode(nodeB)

            #             if (set(element1) & change):
            #                 change = change|set(element1) - set(edge)
            #                 unchange = unchange|set(element2) - set(edge)
            #                 element1 = self.updateElement(element1,nodeA,newNodeA,nodeB,newNodeB)
            #                 self.elements[int(surf1[0])] = tuple(element1)
            #             else:
            #                 change = change|set(element2) - set(edge)
            #                 unchange = unchange|set(element1) - set(edge)

            #                 element2 = self.updateElement(element2,nodeA,newNodeA,nodeB,newNodeB)
            #                 self.elements[int(surf2[0])] = tuple(element2)
            #         else:
            #             joinList += [parent.ID]
            #         k+= 1
              

            #     fringe = newFringe

 
                           
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
# ##        def CZEcrackHelper(self, edge, ID1, ID2):
#         def constructEdge(self, edge1, edge2):
#             if edge1 > edge2:
#                 return (edge2, edge1)
#             else:
#                 return (edge1, edge2)  
        
#         def neighbourTest(self, ID, visited):
#             element = list(self.elements[ID])
#             edges = self.CPE4Edges(element)
#             # for i in visited:

        def makeGraph(self, aList):

            currentNode = int(aList.pop(0))
            self.nodeTree = dict()  ## this set keep track of Graphnodes
            root = self.makeGraphNode(currentNode)
            visited = set()

            while (aList):
                for node in aList:
                    node = int(node)

                    if node > currentNode:
                        edge = (currentNode, node)
                    else:
                        edge = (node, currentNode)

                    if edge in visited:
                        continue
                    if edge in self.edgeTracker:
                        visited.add(edge)
                        graphNodeA = self.makeGraphNode(currentNode)
                        graphNodeB = self.makeGraphNode(node)

                        graphNodeA.addNeighbour(graphNodeB)
                        graphNodeB.addNeighbour(graphNodeA)

                currentNode = int(aList.pop(0))
                        
                        


        def makeGraphNode(self, ID):
            if ID not in self.nodeTree.keys():
                graphnode = graphNode(ID)
                self.nodeTree[ID] = graphnode
                return self.nodeTree[ID]
            else:
                return self.nodeTree[ID]

        def updateElement(self, element, nodeA, newNodeA, nodeB, newNodeB):
            try:
                element[element.index(nodeA)] = newNodeA
            except:
                pass
            try:
                element[element.index(nodeB)] = newNodeB
            except:
                pass
            
            return element

        # def makeTree(self, aList):
        #     self.nodeTree = dict()
        #     currentNode = int(aList.pop(0))
        #     visited = set()
        #     root = treeNode(currentNode)
        #     self.nodeTree[currentNode] = root
        #     fringe = [currentNode]

        #     while (fringe) :
        #         newFringe = []
        #         for currentNode in fringe:
        #             for node in aList:
        #                 node = int(node)
        #                 if node > currentNode:
        #                     edge = (currentNode, node)
        #                 else:
        #                     edge = (node, currentNode)

        #                 if edge in visited:
        #                     continue

        #                 if edge in self.edgeTracker.keys():
        #                     newFringe += [node]
        #                     visited.add(edge)
        #                     nodeA = self.makeTreeNode(currentNode)
        #                     nodeB = self.makeTreeNode(node)
        #                     nodeA.addChild(nodeB)
        #                     nodeB.addParent(nodeA)
                
        #         if len(newFringe) == 0:
        #             fringe = None
        #         else:
        #             fringe = newFringe

        # def makeTreeNode(self, node):
        #     if node in self.nodeTree.keys():
        #         return self.nodeTree[node]
        #     else:
        #         treenode = treeNode(node)
        #         self.nodeTree[node] = treenode
        #         return self.nodeTree[node]


            #             if edge in self.edgeTracker: 
            #                 if (currentNode in visited):
            #                     currentTreeNode = tree[currentNode]
            #                 else:
            #                     currentTreeNode = treeNode(currentNode)
            #                     tree[currentNode] = currentTreeNode

            #                 if (node in visited): 
            #                     tree[node].addParent(currentTreeNode)
            #                     currentTreeNode.addChild(tree[node])
            #                     # currentTreeNode.addParent(tree[node])
            #                     # tree[node].addChild(currentTreeNode)
            #                 else:
            #                     child = treeNode(node)
            #                     tree[node] = child
            #                     currentTreeNode.addChild(child)
            #                     child.addParent(currentTreeNode)
                                
            #                 if (node not in visited):
            #                     visited.add(node)
            #                     newFringe += [node]

            #     fringe = newFringe
            # return tree
        
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
                
                
                 # visited = set()
            # for key in self.nodeTree.keys():
            #     currentNode = self.nodeTree[key]
            #     if currentNode.number == 1:
            #         edge = (currentNode.ID, currentNode.neighbours[0].ID)
            #         surf1, surf2 = self.edgeTracker[edge]
            #         element1 = list(self.elements[int(surf1[0])])
            #         element2 = list(self.elements[int(surf2[0])])
            #         change = change|set(element1) - set(edge)
            #         unchange = unchange|set(element2) - set(edge)
            #         nodeA = edge[0]
            #         nodeB = edge[1]
            #         newNodeA = self.updateNode(nodeA)
            #         newNodeB = self.updateNode(nodeB)
            #         element1 = self.updateElement(element1, nodeA, newNodeA, nodeB, newNodeB)
            #         self.elements[int(surf1[0])] = tuple(element1)
            #     elif currentNode.number == 2:
            #         neighbourA, neighbourB = currentNode.neighbours
            #         if neighbourA.ID in self.cohNode:
            #             node = int(neighbourB.ID)
            #         else:
            #             node = int(neighbourA.ID)

            #         if (currentNode.ID > node):
            #             edge = (node, currentNode.ID)
            #         else:
            #             edge = (currentNode.ID, node)

            #         surf1, surf2 = self.edgeTracker[edge]
            #         element1 = list(self.elements[int(surf1[0])])
            #         element2 = list(self.elements[int(surf2[0])])
            #         nodeA = edge[0]
            #         nodeB = edge[1]
            #         visited.add(edge)
            #         newNodeA = self.updateNode(nodeA)
            #         newNodeB = self.updateNode(nodeB)

            #         if edge not in visited:
            #             if (set(element1) & change):
            #                 change = change|set(element1) - set(edge)
            #                 unchange = unchange|set(element2) - set(edge)
            #                 element1 = self.updateElement(element1,nodeA,newNodeA,nodeB,newNodeB)
            #                 self.elements[int(surf1[0])] = tuple(element1)
            #             else:
            #                 change = change|set(element2) - set(edge)
            #                 unchange = unchange|set(element1) - set(edge)
            #                 element2 = self.updateElement(element2,nodeA,newNodeA,nodeB,newNodeB)
            #                 self.elements[int(surf2[0])] = tuple(element2)
            #     else:
            #         joinList += [currentNode]
            
            # for node in change:
            #     print node



        




# # Test case for tree ##
#             fringe = [tree[2]]
#             while fringe:
#                 printList = []
#                 newFringe = []
#                 for i in fringe:
#                     printList += [i.ID]
#                     newFringe += i.child
#                 print(printList)
#                 if newFringe:
#                     fringe = newFringe
#                 else:
#                     fringe = None

            ########
            # fringe = [root]
            # membership = []
            # visited = []
            # while fringe:
            #     newFringe = []

            #     for parentNode in fringe:
            #         children = parentNode.child
            #         ## Three scenarios, zero child, one child, and more than one  children
            #         if children: 
            #             if parentNode.num == 1:
            #                 childNode = children[0]
            #                 ## this is a key
            #                 edge = self.constructEdge(parentNode.ID, childNode.ID)
            #                 surf1, surf2 = self.edgeTracker[edge]
            #                 ID1 = int(surf1[0])
            #                 ID2 = int(surf2[0])

            #                 if len(visited) == 0:
            #                     visited.append(self.CPE4Edges(list(self.elements[ID1])))
            #                     visited.append(self.CPE4Edges(list(self.elements[ID2])))
            #                     self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
            #                     self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
            #                     ## CP
            #                     self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
            #                     self.surfaceCount += 2
            #                     ## CZE
            #                     ## update 1
            #                     childNode1 = self.updateNode(childNode)
            #                     parentNode1 = self.updateNode(parentNode)
            #                     element1 = list(self.elements[ID1])
            #                     index = element1.index(childNOde)
            #                     element1[index] = childNode1
            #                     index = element1.index(parentNode)
            #                     element1[index] = parentNode1
            #                     self.elements[ID1] = tuple(element1)
            #                     ## update 2
            #                     childNOde2 = self.updateNode(childNOde)
            #                     parentNode2 = self.updateNode(parentNode)
            #                     index = element2.index(childNOde)
            #                     element1[index] = childNode2
            #                     index = element2.index(parentNode)
            #                     element1[index] = parentNode2
            #                     self.elements[ID2] = tuple(element2)

            #                     self.CZE.append([parentNode1, childNode1, childNOde2, parentNode2])

            #                 else:
            #                     element1 = list(self.elements[ID1])
            #                     element2 = list(self.elements[ID2])
            #                     for 

                            
                            


                    
                        # ## CZE
                        # """ three cases
                        #     1. Neither child nor parent node is modified (first encounter)
                        #         just insert and change one side element 
                        #     2. Only parent is modified
                        #         found out which side is different, found which element is on the same side,
                        #         add cze accordingly 
                        #     3. Both parent and child are modified
                                 


                        # """
            

                # sortList = []
                # edgeList = []
                # sortList.append(aList.pop(0))
                # self.updateNode(sortList[0])
                # while (aList):
                        
                #         head = sortList[0]
                #         edge1 = None
                #         tail = sortList[-1]
                #         edge2 = None
                        
                #         for node in aList:
                #                 if node > head:
                #                         edge1 = (head, node)
                #                 else:
                #                         edge1 = (node, head)
                #                 if node > tail:
                #                         edge2 = (tail, node)
                #                 else:
                #                         edge2 = (node, tail)


                #                 if edge1 in self.edgeTracker:
                #                         sortList = [node] + sortList
                #                         edgeList = [edge1] + edgeList
                #                         self.updateNode(node)
                #                         aList.remove(node)
                #                         break
                #                 elif edge2 in self.edgeTracker:
                #                         sortList = sortList + [node]
                #                         edgeList = edgeList + [edge2]
                #                         self.updateNode(node)
                #                         aList.remove(node)
                #                         break
       
                
                # for edge in edgeList:
                #         surf1, surf2 = self.edgeTracker[edge]
                #         self.surfList.append(["surface"+str(self.surfaceCount), surf1[0], surf1[1]])
                #         self.surfList.append(["surface"+str(self.surfaceCount+1), surf2[0], surf2[1]])
                #         ## CP
                #         self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
                #         self.surfaceCount += 2
                #         ## CZE
                #         nodeA = edge[0]
                #         nodeB = edge[1]
                #         updateA = self.nodeTracker[nodeA][-1]
                #         updateB = self.nodeTracker[nodeB][-1]

                #         if (sortList.index(nodeA) < sortList.index(nodeB)):## flip order
                #                 self.CZE.append([str(nodeB), str(nodeA), str(updateA), str(updateB)])
                #         else:
                #                 self.CZE.append([str(nodeA), str(nodeB), str(updateB), str(updateA)])
                #                 edge = edge[::-1]

                #         element1 = self.elements[int(surf1[0])]
                #         element2 = self.elements[int(surf2[0])]
                #         newElement = []
                #         if (element1.index(edge[0]) < element1.index(edge[1])): ## same order
                #                 for i in range(0, len(element2)):
                #                         if element2[i] == nodeA:
                #                                 newElement = newElement + [updateA]
                #                         elif element2[i] == nodeB:
                #                                 newElement = newElement + [updateB]
                #                 self.elements[int(surf2[0])] = tuple(newElement)
                #         else:
                #                 for i in range(0, len(element1)):
                #                         if element1[i] == nodeA:
                #                                 newElement = newElement + [updateA]
                #                         elif element1[i] == nodeB:
                #                                 newElement = newElement + [updateB]
                #                 self.elements[int(surf1[0])] = tuple(newElement)
          
                
