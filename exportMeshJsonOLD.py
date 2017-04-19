# exportMeshJson.py


if 'cmds' not in locals():
  import maya.cmds as cmds


import json


import maya.OpenMaya as OpenMaya



def exportText( text, path ):
  t = open(path, "w")
  t.write( text )
  t.close()


def getFileLocation(filemode=0, fileType="json"):
  return cmds.fileDialog2(fileMode=filemode, ff=fileType)[0]


# similar to obj format
def exportVertexArrays( mesh, prec=6 ):

  if mesh is None:
    return

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


  faces = []


  for i in range(vertexIndexArray.length()):
    faces.append( [vertexIndexArray[i], normalIndexArray[i], uvIdsMIntArray[i] ] )


  output = {
    'position' : [],    # [[x,y,z], ... ]
    'normal' : [],      # [[x,y,z], ... ]
    'uv' : [],          # [[u,v], ... ]
  }


  for f in faces:
    # print f

    p = points[f[0]]
    n = normalArray[f[1]]
    u = uArray[f[2]]
    v = vArray[f[2]]

    output['position'].extend( [round(x, prec) for x in [p[0],p[1],p[2]]] )

    output['normal'].extend( [round(x,prec) for x in [n[0],n[1],n[2]]] )
    
    output['uv'].extend( [round(x,prec) for x in [u,v]] )


  # export the arrays as a json
  exportText(json.dumps( output ), getFileLocation())

  return output



exportVertexArrays(cmds.ls(sl=1,fl=1)[0])

print 'this is old!!!'