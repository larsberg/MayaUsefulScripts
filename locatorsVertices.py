
def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('distanceBetweenPoints.py', '/Users/laserstorm/MayaUsefulScripts/')

import maya.api.OpenMaya as om




# get mesh
def getDagPath(nodeName):
  return om.MGlobal.getSelectionListByName(nodeName).getDagPath(0)

def putLocatorsAtVertices(nodeName):

  g = cmds.group(name="locs", em=True)

  dagPath = getDagPath(nodeName)

  mfnMesh = om.MFnMesh(dagPath) 

  points = [ om.MVector(p) for p in mfnMesh.getPoints() ]


  cmds.constructionHistory( tgl=False )
  # cmds.curve( p=points, degree=1 )
  j=1
  for i in range(0, len(points)):

    if j < len(points):
      if distanceBetweenPoints(points[i], points[j]) < 0.15:
        cmds.curve( p=[points[i], points[j]], degree=1 )
    j += 1


  cmds.constructionHistory( tgl=True )





putLocatorsAtVertices(cmds.ls(sl=1,fl=1)[0])