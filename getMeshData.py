# getMeshData.py
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes 
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('printProgress.py', '/Users/laserstorm/MayaUsefulScripts/')



def getUVs(meshFn):

  uvs = {}

  for i in meshFn.getUVSetNames():
    uv = meshFn.getUVs(i)
    uvs[i] = [val for pair in zip(uv[0], uv[1]) for val in pair]

  return uvs



def flattenArray(forest, maxIndex = 3):
  return [leaf for tree in forest for index, leaf in enumerate(tree) if index < maxIndex]


def getMeshData(nodeName, coordSpace = om.MSpace.kWorld ):

  meshObj = getMObjectForNode(nodeName)
  
  meshDag = getDagPathForNode(nodeName)

  meshFn = om.MFnMesh(meshDag)

  uvs = getUVs(meshFn)

  for i in uvs:
    print len(uvs[i])
  #   uvs[i] = flattenArray[uvs[i]]

  return {
    "position" : flattenArray(meshFn.getFloatPoints(coordSpace)),
    "normal" : flattenArray(meshFn.getNormals(coordSpace)),
    "uvs" : uvs,
    "faces" : None
  }


