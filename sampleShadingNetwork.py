# http://mayastation.typepad.com/maya-station/2011/03/how-to-sample-a-3d-texture.html

# getMeshData.py
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')


# example that samples a 3D marble texture at the location of a sphere
import maya.OpenMaya as OpenMaya
import maya.OpenMayaRender as OpenMayaRender

#
#
def sampleShadingNetworkAtPoints(nodeAttr, points):

  numSamples = len(points)
  pointArray = points;
  pointArray = OpenMaya.MFloatPointArray()
  pointArray.setLength(numSamples)

  refPoints = OpenMaya.MFloatPointArray()
  refPoints.setLength(numSamples)

  for i, point in enumerate(points):
    location = OpenMaya.MFloatPoint(point[0], point[1], point[2])
    pointArray.set(location, i)
    refPoints.set(location, i)

  # but we don't need these
  useShadowMap = False
  reuseMaps = False
  cameraMatrix= OpenMaya.MFloatMatrix()
  uCoords= None
  vCoords= None
  normals= None
  tangentUs= None
  tangentVs= None
  filterSizes= None

  # and the return arguments are empty....
  resultColors = OpenMaya.MFloatVectorArray()
  resultTransparencies = OpenMaya.MFloatVectorArray()

  # sample the node network
  OpenMayaRender.MRenderUtil.sampleShadingNetwork(
    nodeAttr,
    numSamples,
    useShadowMap,
    reuseMaps,
    cameraMatrix,
    pointArray,
    uCoords,
    vCoords,
    normals,
    refPoints,
    tangentUs,
    tangentVs,
    filterSizes,
    resultColors,
    resultTransparencies )

  # return formatted sampled colours
  return resultColors




def sampleShadingNetwork(nodeAttr, points):

  c = sampleShadingNetworkAtPoints(nodeAttr, points)

  return [om.MVector(c[i].x, c[i].y, c[i].z) for i in range(c.length())]
