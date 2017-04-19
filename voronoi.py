# voronoi.py
import random


# getMeshData.py
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('flattenArray.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('distanceBetweenPoints.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('printProgress.py', '/Users/laserstorm/MayaUsefulScripts/')


import time


# TODO:
#   use bounding box for each point
#   as points are trimmed their bounding boxes shrink
#   compare boxes before trimming



def getParticlePositions( particles ):
  points = []

  for i in range(cmds.nParticle( inputs['nParticle'], q=1, ct=1)):
    p = om.MVector( cmds.nParticle( at='position', q=1, id=i  ) )
    points.append(p)

  return points



def getType(nodeName):
  return cmds.objectType( cmds.listRelatives( nodeName, s=1)[0] )


def setBoundsFromMesh(bounds, mesh):

  bb = cmds.polyEvaluate(mesh, boundingBox=1)

  bounds.clear()
  bounds.expand(om.MPoint(bb[0][0],bb[1][0],bb[2][0]))
  bounds.expand(om.MPoint(bb[0][1],bb[1][1],bb[2][1]))



def setTranslationToPivotPosition( node ):

  pivotPos = cmds.xform(node, q=1, ws=1, rp=1)

  cmds.xform( node, t=[ -i for i in pivotPos ], ws=True)

  cmds.makeIdentity(node, t=True, apply=True)

  cmds.xform( node, t=pivotPos, ws=True )


def cutMesh(m, mid, delta, up):

  q = up.rotateTo(delta)

  euler = q.asEulerRotation()

  rot = [degrees(euler.x), degrees(euler.y), degrees(euler.z)]

  cmds.polyCut(m, ch=0, pc=mid, ro=rot, df=1)
  cmds.polyCloseBorder(m, ch=0)
  cmds.delete(m, ch=True)

  return m



def setTranslationToPivotPosition( node ):

  pivotPos = cmds.xform(node, q=1, ws=1, rp=1)

  cmds.xform( node, t=[ -i for i in pivotPos ], ws=True)

  cmds.makeIdentity(node, t=True, apply=True)

  cmds.xform( node, t=pivotPos, ws=True )




def voronoiFromnPoints(points, boundaryOffset = 1):

  # randomizing speeds things up a bit the bounding boxes trim faster/stronger
  random.shuffle(points)

  # get the particle bounding box
  bounds = om.MBoundingBox()
  for p in points:
    bounds.expand(om.MPoint(p))


  boundMesh = cmds.polyCube(
    name='VoronoiBoundMesh',
    ch=0,
    w=bounds.width + boundaryOffset,
    h=bounds.height + boundaryOffset,
    d=bounds.depth + boundaryOffset)

  cmds.xform(boundMesh, t=[bounds.center.x, bounds.center.y, bounds.center.z] )
  cmds.hide(boundMesh)

  # per point bounds
  pointBounds = []
  boundMeshes = []
  group = cmds.group( em=True, name='voronoi' )

  for i, p in enumerate(points):

    pointBounds.append( om.MBoundingBox(bounds))

    m = cmds.duplicate(boundMesh)

    cmds.hide(m)

    # print m
    cmds.parent(m[0], group)
    boundMeshes.append(m)


  # for larger point counts I've had to turn off the  undo cache for (crashes), you may need to adjust this
  if len(points) > 30:
    print 'Turning off undo... lots of points'
    cmds.undoInfo( state=False )

  isCount = 0

  for i, p in enumerate(points):

    diameter = distanceBetweenPoints(pointBounds[i].min, pointBounds[i].max)

    for j, p1 in enumerate(points):

      if j > i:

        if pointBounds[i].intersects( pointBounds[j] ) :

          mid = (p+p1) * 0.5

          delta = p - p1

          cutMesh(boundMeshes[i], mid, (p - p1).normalize(), om.MVector(0,0,1))
          setBoundsFromMesh(pointBounds[i], boundMeshes[i])

          cutMesh(boundMeshes[j], mid, (p1 - p).normalize(), om.MVector(0,0,1))
          setBoundsFromMesh(pointBounds[j], boundMeshes[j])


    cmds.showHidden(boundMeshes[i])
    setTranslationToPivotPosition(boundMeshes[i])
    if i%3 is 0:
      # printProgress(i, len(points), 'voronoi progress:')
      cmds.refresh()

  cmds.delete(boundMesh)
  cmds.undoInfo( state=True )
  cmds.select(group, r=1)




# # use boundaryMesh as a boolean op on the remaining
# if 'mesh' in inputs:

#   cells = cmds.listRelatives(group, children=1)

#   for c in cells:

#     dup = cmds.duplicate(boundaryMesh, rc=True)

#     trimmed = cmds.polyBoolOp( dup[0], c, op=3, ch=False )

#     cmds.delete(trimmed, ch=True)
#     cmds.delete(dup[0])
#     cmds.parent(trimmed, group)

#     cmds.refresh()
#     time.sleep(0.01)



# cmds.constructionHistory( tgl=True )






# get bounding box mesh, we'll use this to make carving mesh
selected = cmds.ls(sl=1,fl=1)

# CH = cmds.constructionHistory( q=True, tgl=True )

# cmds.constructionHistory( tgl=False )


inputs = {}
for i in selected:
  inputs[getType(i)] = i # getDagPathForNode(i);

print inputs


# get the particle positions
points = getParticlePositions(inputs['nParticle'])

voronoiFromnPoints(points, 20)

cmds.select(selected, r=1)