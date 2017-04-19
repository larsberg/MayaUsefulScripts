# randomParticlesOnMesh.py

'''

TODO:

- [ ] multiple uv sets

- [ ] bounding box

'''


def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('exportText.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getFileLocation.py', '/Users/laserstorm/MayaUsefulScripts/')

includeScript('getRandomPointsOnMesh.py', '/Users/laserstorm/MayaUsefulScripts/')


import maya.api.OpenMaya as om
import random
import json


# # get mesh
# def getDagPath(nodeName):
#   return om.MGlobal.getSelectionListByName(nodeName).getDagPath(0)


# def pointInTriangle(t0, t1, t2, u, v):

#   if ( u + v ) > 1:
#     u = 1.0 - u;
#     v = 1.0 - v;

#   return t0 * u + t1 * v + t2 * (1 - u - v);


# def areaOfTriangle(p0, p1, p2):
#   return ((p2 - p1) ^ (p0 - p1)).length() * .5;


# def getRandomPoints(nodeName, count = 100):

#   dagPath = getDagPath(nodeName)

#   mfnMesh = om.MFnMesh(dagPath)

#   numFaces = mfnMesh.numPolygons

#   point = om.MPoint(1,2,3)

#   triangles = mfnMesh.getTriangles()[1]

#   points = mfnMesh.getPoints(om.MSpace.kWorld)

#   numTriangles = len(triangles)

#   data = {
#     'position': []
#   }

#   p0 = om.MVector()
#   p1 = om.MVector()
#   p2 = om.MVector()

#   for i in range(0, count):

#     u = random.random()
#     v = random.random()

#     t = random.randint(0, numTriangles-3)

#     t0 = triangles[t];
#     t1 = triangles[t+1];
#     t2 = triangles[t+2];

#     p0 = om.MVector(points[t0])
#     p1 = om.MVector(points[t1])
#     p2 = om.MVector(points[t2])

#     p = pointInTriangle(p0, p1, p2, u, v)

#     data['position'].append(p)

#   return data

# def compareAreas(a, b):
#   if a['area'] < b['area']:
#     return 1
#   elif b['area'] == a['area']:
#     return 0
#   else:
#     return -1

# def getDistributedRandomPoints(nodeName, count):


#   data = {
#     'position': [],
#     'normal': [],
#     'uv': [],
#     'uvSets': {}
#   }

#   dagPath = getDagPath(nodeName)

#   mfnMesh = om.MFnMesh(dagPath)

#   points = [ om.MVector(p) for p in mfnMesh.getPoints(om.MSpace.kWorld) ]

#   # normals = [ om.MVector(n) for n in mfnMesh.getVertexNormals(True) ]

#   triIndices = mfnMesh.getTriangles()[1]

#   triangles = []

#   totalArea = 0

#   for i in range(0, len(triIndices), 3):

#     t0 = triIndices[i];
#     t1 = triIndices[i+1];
#     t2 = triIndices[i+2];

#     t = {
#       'p0': points[t0],
#       'p1': points[t1],
#       'p2': points[t2],
#       # 'n0': normals[t0],
#       # 'n1': normals[t1],
#       # 'n2': normals[t2],
#       'area': 0,
#       'start': 0
#     }

#     t['area'] = sqrt(areaOfTriangle(t['p0'], t['p1'], t['p2']))
#     totalArea += t['area']

#     triangles.append( t )

#   # sort by area
#   triangles.sort(compareAreas)


#   # which index do we start on
#   prog = 0
#   for t in triangles:
#     prog += t['area']
#     t['startIndex'] = count * prog / totalArea


#   # iterate through the triangles and makes some points
#   tIndex = 0
#   uvSetNames = mfnMesh.getUVSetNames()
#   for i in uvSetNames:
#     data['uvSets'][i] = []

#   for i in range(0, count):

#     u = random.random()
#     v = random.random()

#     if tIndex == len(triangles):
#       print 'breaking at :' + str(i)
#       break

#     t = triangles[tIndex]

#     if t['startIndex'] < i:
#       tIndex += 1

#     p = pointInTriangle(t['p0'],t['p1'],t['p2'], u, v)

#     data['position'].append(p)
#     # data['position'].extend([p[0],p[1],p[2]])

#   return data



def randomParticlesOnMesh(mesh, count = 100):

  data = getRandomPointsOnMesh(mesh, count)

  cmds.nParticle( p=data['position'] )


randomParticlesOnMesh(cmds.ls(sl=True, fl=True)[0], 500)