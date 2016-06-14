# meshToArrays.py
# 

if 'cmds' not in locals():
  import maya.cmds as cmds


import json


import maya.OpenMaya as OpenMaya


# similar to obj format
def getDataArrays( mesh, prec=6 ):

  # get the dag path from the mesh name
  selection = OpenMaya.MSelectionList()
  selection.add( mesh )
  iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kGeometric)

  dagPath = OpenMaya.MDagPath()
  iterSel.getDagPath( dagPath )

  # our mesh function set
  meshFn = OpenMaya.MFnMesh(dagPath)


  # vertex data
  points = OpenMaya.MPointArray()
  normalArray = OpenMaya.MFloatVectorArray()
  uArray = OpenMaya.MFloatArray()
  vArray = OpenMaya.MFloatArray()

  # vertex face counts
  vertexCountMIntArray = OpenMaya.MIntArray()
  normalCountMIntArray = OpenMaya.MIntArray()
  uvCountMIntArray = OpenMaya.MIntArray()

  # face vertex index arrays
  vertexIndexArray = OpenMaya.MIntArray()
  normalIndexArray = OpenMaya.MIntArray()
  uvIdsMIntArray = OpenMaya.MIntArray()

  # get the vertex values
  meshFn.getPoints( points, OpenMaya.MSpace.kWorld )
  meshFn.getNormals( normalArray, OpenMaya.MSpace.kWorld )
  meshFn.getUVs( uArray, vArray )

  # get the face vertex indices
  meshFn.getVertices( vertexCountMIntArray, vertexIndexArray )
  meshFn.getNormalIds( normalCountMIntArray, normalIndexArray )
  meshFn.getAssignedUVs( uvCountMIntArray, uvIdsMIntArray )

  output = {
    'position' : [],    # [[x,y,z], ... ]
    'normal' : [],      # [[x,y,z], ... ]
    'uv' : [],          # [[u,v], ... ]
    'faceIndices' : []  # [[positionIndex,normalIndex,uvIndex], ... ]
  }

  for i in range(points.length()):
    output['position'].append( [round(points[i][0], prec), round(points[i][1], prec), round(points[i][2], prec)] )

  for i in range(normalArray.length()):
    output['normal'].append( [round(normalArray[i][0], prec), round(normalArray[i][1], prec), round(normalArray[i][2], prec)] )

  for i in range(uArray.length()):
    output['uv'].append( [round(uArray[i], prec), round(vArray[i], prec)] )

  for i in range(vertexIndexArray.length()):
    output['faceIndices'].append( [vertexIndexArray[i], normalIndexArray[i], uvIdsMIntArray[i] ] )

  return output


for mesh in cmds.ls(sl=1,fl=1):
  print getDataArrays(mesh)