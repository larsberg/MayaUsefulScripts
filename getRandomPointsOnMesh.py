# randomPointsOnMesh.py

def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('normalFromThreePoints.py', '/Users/laserstorm/MayaUsefulScripts/')

import random

import maya.api.OpenMaya as om


# get mesh
def getDagPath(nodeName):
  return om.MGlobal.getSelectionListByName(nodeName).getDagPath(0)


def pointInTriangle(t0, t1, t2, u, v):

  if ( u + v ) > 1:
    u = 1.0 - u;
    v = 1.0 - v;

  return t0 * u + t1 * v + t2 * (1 - u - v);



def areaOfTriangle(p0, p1, p2):
  return ((p2 - p1) ^ (p0 - p1)).length() * .5



def getRandomPointsOnMesh(nodeName, count = 100):

  # print nodeName, "wtf"

  meshDag = getDagPathForNode(nodeName)

  meshFn = om.MFnMesh(meshDag)

  triangles = meshFn.getTriangles()[1]

  points = meshFn.getPoints(om.MSpace.kWorld)

  numTriangles = len(triangles) / 3

  data = {
    'position': [],
    'normal': []
  }

  for i in range(0, count):

    t0 = random.randint(0, numTriangles-1) * 3
    t1 = t0 + 1
    t2 = t0 + 2

    p0 = om.MVector( points[ triangles[t0] ] )
    p1 = om.MVector( points[ triangles[t1] ] )
    p2 = om.MVector( points[ triangles[t2] ] )

    u = random.random()
    v = random.random()

    p = pointInTriangle(p0, p1, p2, u, v)
    n = normalFromThreePoints(p0, p1, p2)

    data['position'].append(p)
    data['normal'].append(n)

  return data

# print getRandomPointsOnMesh(cmds.ls(sl=True, fl=True)[0], 1000)