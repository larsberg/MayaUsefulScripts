import json

if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes 
includeScript('getMeshData.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getSkinInfo.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('exportText.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getFileLocation.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('flattenArray.py', '/Users/laserstorm/MayaUsefulScripts/')


origSelect = cmds.ls(sl=1,fl=1)[0]

cmds.select("pCube1", r=1)

m = cmds.ls(sl=1,fl=1)[0]

# mesh data
meshData = getMeshData( m )

# skin weights
skinWeights = getSkinInfo( m )


def getBoundingBox(nodeName, objectSpace=True):
  return cmds.xform( nodeName, q=1, bb=1, os=objectSpace )

def getRigidBodies(nodeName):
  return cmds.listRelatives( nodeName, c=1, type="bulletRigidBodyShape") or cmds.listRelatives( nodeName, c=1, type="rigidBody") or []

def getRigidBodyShapeType(rb):
  
  shapeTypeMap = {
    1 : "box",
    2 : "sphere",
    3 : "capsule",
    4 : "hull",
    5 : "mesh",
    6 : "plane",
    7 : "cylinder",
  }

  return shapeTypeMap[cmds.getAttr(rb + '.colliderShapeType' )]

def getRigidBodyInfo(nodeName):
  
  bodyType = getRigidBodyShapeType(nodeName)
 
  return {
    "type" : bodyType,
    "static" : cmds.getAttr(nodeName + '.bodyType' ) == 0,
    "mass" : cmds.getAttr(nodeName + '.mass' ),
    "radius" : cmds.getAttr(nodeName + '.radius' ),
    "length" : cmds.getAttr(nodeName + '.length' ),
    "friction" : cmds.getAttr(nodeName + '.friction' ),
    "restitution" : cmds.getAttr(nodeName + '.restitution' ),
    "axis" : cmds.getAttr(nodeName + '.axis' ),
    "linearDamping" : cmds.getAttr(nodeName + '.linearDamping' ),
    "angularDamping" : cmds.getAttr(nodeName + '.angularDamping' ),
    "impulsePosition" : [i for i in cmds.getAttr(nodeName + '.impulsePosition' )[0]],
    "extents" : [i for i in cmds.getAttr(nodeName + '.extents' )[0]],
    "centerOfMass" : [i for i in cmds.getAttr(nodeName + '.centerOfMass' )[0]],
    "colliderOffset" : [i for i in cmds.getAttr(nodeName + '.colliderShapeOffset' )[0]],
    "constraints" : "TODO: get the constraints. try cmds.listConnections ?"
  }


# get the joint transforms
meshData["joints"] = {}
for i in skinWeights["jointNames"]:
  meshData["joints"][i] = cmds.xform( i, q=1, m=1, os=1, worldSpace=True )


for i in skinWeights:
  meshData[i] = skinWeights[i]


# get the joint heirarchy and constraints
meshData["jointData"] = {}
for i in skinWeights["jointNames"]:

  # get parent
  parent = cmds.listRelatives( i, p=1 )

  # get children
  children = cmds.listRelatives( i, c=1, type='joint' )
  
  # get constraints
  parentConstraints = [cmds.parentConstraint(c, q=1,targetList=1 )[0] for c in cmds.listRelatives(i, type="parentConstraint")]

  meshData["jointData"][i] = {
    "name" : i,
    "position" : cmds.xform(i, q=1, translation=1, worldSpace=True),
    "transform" : cmds.xform( i, q=1, m=1, worldSpace=True ),
    "parent" : parent,
    "children" : children,
    "parentConstraints" : parentConstraints,
    "rigidBodies" : [rb for p in parentConstraints for rb in getRigidBodies(p)]
  }



# each mesh will get a rigid body
# things we'll need from that rigid body are:
# - constraints
rigidBodies = {}

for i in meshData["jointData"]:

  for rb in meshData["jointData"][i]["rigidBodies"]:
    
    rigidBodies[rb] = getRigidBodyInfo(rb)


meshData["rigidBodies"] = rigidBodies





  
# rigidBodies = {}
# for i in meshData["jointData"]:
  
#   bodies = meshData["jointData"][i]["parentConstraints"]

#   for b in bodies:

#     rigidBodies[b] = {
#       "bound" : getBoundingBox(b),
#       "transform" : cmds.xform( b, q=1, m=1, worldSpace=True )
#     }
    
# print rigidBodies

# for i in rigidBodies:
#   print cmds.listRelatives(i, c=1)
#   print "connections",cmds.listConnections(i, type="constraint")
#   for j in cmds.listRelatives(i, c=1):
#     print "connections",cmds.listConnections(j, type="constraint")

#   # for c in cmds.listRelatives( i, c=1, type="bulletRigidBodyShape") or cmds.listRelatives( i, c=1, type="rigidBody") or []:
#   #   print cmds.listConnections(c)


print meshData["jointData"]

# write a json file
# exportText(json.dumps(meshData, indent=4), getFileLocation(0, '.json'))
json.dumps(meshData, indent=4)


cmds.select(origSelect, r=1)