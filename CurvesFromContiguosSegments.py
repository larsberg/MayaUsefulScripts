# CurvesFromContiguosSegments.py

def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('distanceBetweenPoints.py', '/Users/laserstorm/MayaUsefulScripts/')

import maya.api.OpenMaya as om


# get mesh
def getDagPath(nodeName):
  return om.MGlobal.getSelectionListByName(nodeName).getDagPath(0)


selection = cmds.ls(sl=1,fl=1)

segments = []

for segment in selection:
  nc = om.MFnNurbsCurve(getDagPath(segment));
  segments.extend( [nc.cvPositions()] )



def doSegmentsTouch(s0, s1, threshold=0.01):
  if s0[0].distanceTo(s1[0]) < threshold :
    return True
  elif s0[-1].distanceTo(s1[0]) < threshold :
    return True
  elif s0[0].distanceTo(s1[-1]) < threshold :
    return True
  elif s0[-1].distanceTo(s1[-1]) < threshold :
    return True
  else:
    return False

currentCurve = []
curves = [currentCurve]

lastSegment = 0


for s in segments:

  if lastSegment != 0:

    if doSegmentsTouch(s, lastSegment):
      currentCurve.append(s)

    else:
      currentCurve = []
      currentCurve.append(s)
      curves.append(currentCurve)
  
  else:
    currentCurve.append(s)

  lastSegment = s

  

outCurves = []
for curve in curves:
  cp = []
  for s in curve:
    if s[0] not in cp:
      cp.append(s[0])

    if s[1] not in cp:
      cp.append(s[1])


  points = []
  for p in cp:
    points.append((p[0],p[1],p[2]))
  
  outCurves.append(cmds.curve( p=points, degree=1 ))
  cmds.refresh()

cmds.select(outCurves, r=1)
cmds.group(name="NEW_CURVES")

cmds.select(selection, r=1)