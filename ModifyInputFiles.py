# Created by Elias Ghadam Soltani
# This code is written to convert exfile to vtk file and ply to smesh. I use this approach to get the surface mesh from ParaView
# In this version of the code it just produces conectivities and positions on the screen so you need to copy and paste them
# into a vtk template file.
# Don't forget that the order of node numbering for an element in vtk and exfile is different. See Google slides for that

import numpy

# This block of code produces the conectivities i.e. nodes on the element e.g. 1 5 7 8 4 6 3 2
#localNodes=[0]*8
#with open('inputFiles/left_upper_limb.exelem','r') as f:
#  target=f.readlines()
#  for lineNum,line in enumerate(target):
#    target[lineNum] = target[lineNum].rstrip("\n\r").replace("\t"," ").replace(","," ").split()
#  for lineNum,line in enumerate(target):
#    if ((target[lineNum][0]=="Element:") and (int(target[lineNum][1]) != 0)):
#      localNodes[0]=int(target[lineNum+9][0])-1
#      localNodes[1]=int(target[lineNum+9][1])-1
#      localNodes[2]=int(target[lineNum+9][2])-1
#      localNodes[3]=int(target[lineNum+9][3])-1
#      localNodes[4]=int(target[lineNum+9][4])-1
#      localNodes[5]=int(target[lineNum+9][5])-1
#      localNodes[6]=int(target[lineNum+9][6])-1
#      localNodes[7]=int(target[lineNum+9][7])-1
#      print 8,localNodes[0],localNodes[1],localNodes[5],localNodes[4],localNodes[2],localNodes[3],localNodes[7],localNodes[6]

#This block of code produces Node positions such as 9.0 8.2 7.0
#with open('inputFiles/left_upper_limb.exnode','r') as f:
#  target=f.readlines()
#  for lineNum,line in enumerate(target):
#    target[lineNum] = target[lineNum].rstrip("\n\r").replace("\t"," ").replace(","," ").split()
#  for lineNum,line in enumerate(target):
#    if ((target[lineNum][0]=="Node:")):
#      print float(target[lineNum+1][0]),float(target[lineNum+2][0]),float(target[lineNum+3][0])



# Convert some ply files to smesh
def ply2smesh(FileName,RegionLabel,numberOfLocalNodes,offset=0):
  localNodes = [0]*numberOfLocalNodes
  NodeBegin = False
  nodeNumber = 0
  faceNumber = 0
  FaceBegin = False
  numberOfNodes = -1
  numberOfFaces = -1


  with open(FileName,'r') as f:
    target=f.readlines()
    for lineNum,line in enumerate(target):
      target[lineNum] = target[lineNum].rstrip("\n\r").replace("\t"," ").replace(","," ").split()
    for lineNum,line in enumerate(target):
      if target[lineNum][0] == "element":
        if (target[lineNum][1]=="vertex"):
          numberOfNodes = int(target[lineNum][2])
        elif ((target[lineNum][1]=="face")):
          numberOfFaces = int(target[lineNum][2])
          print numberOfFaces,numberOfNodes
      if NodeBegin:
        x = float(target[lineNum][0])
        y = float(target[lineNum][1])
        z = float(target[lineNum][2])
        print nodeNumber+offset, x, y,z, RegionLabel
        nodeNumber = nodeNumber+1
      if target[lineNum][0] == "end_header":
        NodeBegin = True

      if FaceBegin:
        numberOfLocalNodes = int(target[lineNum][0])
        string=""
        for i in range(numberOfLocalNodes):
          localNodes[i] = int(target[lineNum][i+1])+offset
          string=string+str("localNodes[%d]," %i)
        string="print numberOfLocalNodes,"+string+"RegionLabel"
        exec(string)
#        print numberOfLocalNodes, localNodes[0],localNodes[1],localNodes[2], RegionLabel
        faceNumber = faceNumber+1
      if nodeNumber == numberOfNodes:
        NodeBegin = False
        FaceBegin = True
      if faceNumber == numberOfFaces:
        FaceBegin = False 

numberOfRegions = 4      
totalNumberOfNodes = 256
totalNumberOfFaces = 510
FileName = "deleteIt.smesh"
# Creating template smesh textfile
def TemplateSmesh(FileName,totalNumberOfNodes,totalNumberOfFaces,numberOfRegions):
  with open(FileName, 'w') as f:
    f.write('# Part 1 - the node list.\n')
    f.write('# The model has %d nodes in 3d, no attributes, with boundary marker.\n' % totalNumberOfNodes)
    f.write('%d  %d  %d  %d\n' %(totalNumberOfNodes,3,0,1))
    f.write('# Skin point clouds\n')
    f.write('%d %f %f %f %d\n' % (29,12.0,2.6,3.5,2))
    f.write('# Left Radius points cloud\n')
    f.write('%d %f %f %f %d\n' % (29,12.0,2.6,3.5,3))
    f.write('# Left Humerus points cloud\n')
    f.write('%d %f %f %f %d\n' % (29,12.0,2.6,3.5,4))
    f.write('# Left Ulna points cloud\n')
    f.write('%d %f %f %f %d\n' % (29,12.0,2.6,3.5,5))
    f.write('# Part 2 - the facet list.\n')
    f.write('# %d facets with boundary markers.\n' % totalNumberOfFaces)
    f.write('%d  %d\n' %(totalNumberOfFaces,1))
    f.write('# Skin facets\n')
    f.write('%d	%d	%d	%d	%d	%d\n' %(4,0,1,2,3,2))
    f.write('# Left Radius facets\n')
    f.write('%d	%d	%d	%d	%d\n' %(3,0,1,2,3))
    f.write('# Left Humerus facets\n')
    f.write('%d	%d	%d	%d	%d\n' %(3,0,1,2,4))
    f.write('# Left Ulna facets\n')
    f.write('%d	%d	%d	%d	%d\n' %(3,0,1,2,5))
    f.write('# Part 3 - the hole list.\n')
    f.write('# There is no hole in regions.\n')
    f.write('%d\n' %0)
    f.write('# Part 4 - the region list.\n')
    f.write('# There are %d regions defined.\n' %numberOfRegions)
    f.write('%d\n' %numberOfRegions)
    f.write('  1 -206.152 -86.7753 978.752 -10 # muscle\n')
    f.write('  2 -251.338 -87.4435 922.511 -20 # bone\n')
    f.write('  3 -251.338 -87.4435 922.511 -20 # bone\n')
    f.write('  4 -251.338 -87.4435 922.511 -20 # bone\n')

RegionLabel = 2
offset = 0
FileName = 'fifth layer/DenseSkinSurf.ply'
numberOfLocalNodes = 3
ply2smesh(FileName,RegionLabel,numberOfLocalNodes,offset)


#TemplateSmesh("deleteIt.smesh",510,256,4)
