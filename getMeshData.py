# getMeshData.py
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes 
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('flattenArray.py', '/Users/laserstorm/MayaUsefulScripts/')


def getUVs(meshFn):

  uvs = {}

  for i in meshFn.getUVSetNames():
    uv = meshFn.getUVs(i)
    uvs[i] = [[pair[0], pair[1]] for pair in zip(uv[0], uv[1])]
    # uvs[i] = [val for pair in zip(uv[0], uv[1]) for val in pair]

  return uvs


def getTangents(meshFn, coordSpace):

  tangents = {}

  for i in meshFn.getUVSetNames():
    tangents[i] = meshFn.getTangents(coordSpace, i)

  return tangents

def getFaces(meshDag):

  polyIter = om.MItMeshPolygon(meshDag)

  faces = []
  
  for p in range(polyIter.count()):

    polyIter.setIndex(p)

    fv = [i for i in polyIter.getVertices()]
    fn = []
    fuv = []

    # TODO: handle multiple uv sets
    for i, vIndex in enumerate(fv):
      fn.append( polyIter.normalIndex(i) )
      fuv.append( polyIter.getUVIndex(i) )

    faces.append([fv,fn,fuv])

  return faces


def getMeshData(nodeName, coordSpace = om.MSpace.kWorld ):

  meshObj = getMObjectForNode(nodeName)
  
  meshDag = getDagPathForNode(nodeName)

  meshFn = om.MFnMesh(meshDag)

  uvs = getUVs(meshFn)

  faces = getFaces(meshDag)

  positions = [[p for p in i ] for i in meshFn.getFloatPoints(coordSpace)] 

  normals = [[n for n in i ] for i in meshFn.getNormals(coordSpace)] 

  print uvs

  return {
    "position" : positions,
    "normal" : normals,
    "uv" : uvs,
    "faces" : faces
    # "binormals" : meshFn.getBinormals(coordSpace),
    # "tangents" : getTangents(meshFn, coordSpace),
  }


