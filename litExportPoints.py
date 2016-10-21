

def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('exportText.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getFileLocation.py', '/Users/laserstorm/MayaUsefulScripts/')


import maya.api.OpenMaya as om
import json



doNormals = True

normalMeshName = 'resampledOcclusion1:normalSample'
uvMeshName = 'resampledOcclusion1:uvSample'


# our output object
data = {
  'position': [],
  'normal': [],
  'uvSets': {}
}


# get mesh
def getDagPath(nodeName):
  return om.MGlobal.getSelectionListByName(nodeName).getDagPath(0)



# the mesh we'll sample from
normalMesh = om.MFnMesh(getDagPath(normalMeshName))
uvMesh = om.MFnMesh(getDagPath(uvMeshName)) 

# list of MPoints to sample with
points = []

# open point file and parse through vertices to create an array of mPoints
loc = "/Users/laserstorm/Tool_Lexus/LED-model-uvmap-10-11-v5-POINTS.obj" # getFileLocation()
count = 0

with open(loc) as f:
  for line in f:

    if line[:2] == "v ":
      v = line[2:].split(' ')
      p = om.MPoint(float(v[0]),float(v[1]),float(v[2]))
      points.append(p)
      data['position'].extend([float(v[0]),float(v[1]),float(v[2])])

    count += 1

print "positions done"
cmds.refresh()

print "count: " + str(count)

# sample the UVs
count = 0
for i in uvMesh.getUVSetNames():
  
  data['uvSets'][i] = []

  for p in points:
    uv = uvMesh.getUVAtPoint(p, om.MSpace.kObject, i)
    data['uvSets'][i].extend(uv[0:2])

    count += 1
    if count % 1000 == 0:
      print i + " count == " + str(count)
      cmds.refresh()

print "UVs done"
cmds.refresh()

if doNormals: 
  # sample the normals
  count = 0

  for p in points:
    n = normalMesh.getClosestNormal(p, om.MSpace.kObject)[0]
    data['normal'].extend(n)
    
    count += 1
    if count % 1000 == 0:
      print "normal count == " + str(count)
      cmds.refresh()

# write a json file
exportText(json.dumps( data ), getFileLocation(0, '.json'))

