# getMeshData.py
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')

import random

# def GetDagPath(nodeName):
#   sel = om.MSelectionList()
#   om.MGlobal.getSelectionListByName(nodeName, sel)

#   dp = om.MDagPath()

#   sel.getDagPath(0,dp)
#   return dp


def UvCoordToWorld(meshFn, u, v, space = om.MSpace.kWorld, uvSet=''):

  numFaces = meshFn.numPolygons

  WSpoint = om.MPoint(0.0,0.0,0.0)

  # util2 = om.MScriptUtil()
  # util2.createFromList ((U, V),2)
  # float2ParamUV = util2.asFloat2Ptr()

  for i in range(numFaces):
    try:
      #point is in this poly
      return meshFn.getPointAtUV(i, u, v, space, uvSet)
      break
    except:
      continue #point not found!

  return None


# print UvCoordToWorld(om.MFnMesh(getDagPathForNode(cmds.ls(sl=1, fl=1)[0])), random.random(), random.random())