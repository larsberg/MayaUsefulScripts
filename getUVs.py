'''

TODO:

- [ ] multiple uv sets

- [ ] normals

- [ ] bounding box

'''


def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('exportText.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getFileLocation.py', '/Users/laserstorm/MayaUsefulScripts/')


import maya.api.OpenMaya as om
import random
import json


# get mesh
def getDagPath(nodeName):
  return om.MGlobal.getSelectionListByName(nodeName).getDagPath(0)

def getUVs(mesh):

  uvs = {}

  for i in mesh.getUVSetNames():
    uvs[i] = mesh.getUVs(i)

  return uvs


m = om.MFnMesh(getDagPath(cmds.ls(sl=1,fl=1)[0]))


print getUVs(m).keys()
