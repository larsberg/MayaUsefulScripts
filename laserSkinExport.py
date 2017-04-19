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


m = cmds.ls(sl=1,fl=1)[0]

# mesh data
meshData = getMeshData( m )

# skin weights
skinWeights = getSkinInfo( m )

def getBoundingBox(nodeName, objectSpace=True):
  return cmds.xform( nodeName, q=1, bb=1, os=objectSpace )


def getRigidBodies(nodeName):
  return cmds.listRelatives( nodeName, c=1, type="bulletRigidBodyShape") or cmds.listRelatives( nodeName, c=1, type="rigidBody") or []


def getRigidBodyConstraints(nodeName):

  constraints = []

  for c in [i for i in cmds.listConnections(nodeName)]:
    
    for s in cmds.listRelatives( c, s=1) or []:
      
      if cmds.objectType(s) == 'bulletRigidBodyConstraintShape':
      
        constraints.append(c)

  return constraints




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

  parent = cmds.listRelatives(nodeName, p=1)
 
  return {
    "parent" : parent,
    "position" : cmds.xform(parent, q=1, translation=1, worldSpace=True),
    "scale" : cmds.xform(parent, q=1, scale=1, worldSpace=True),
    "rotation" : cmds.xform(parent, q=1, rotation=1, worldSpace=True),
    "transform" : cmds.xform(parent, q=1, m=1, worldSpace=True ),
    "type" : bodyType,
    "static" : cmds.getAttr(nodeName + '.bodyType' ) == 0,
    "mass" : cmds.getAttr(nodeName + '.mass' ),
    "radius" : cmds.getAttr(nodeName + '.radius' ),
    "length" : cmds.getAttr(nodeName + '.length' ),
    "friction" : cmds.getAttr(nodeName + '.friction' ),
    "restitution" : cmds.getAttr(nodeName + '.restitution' ),
    "axis" : {0: 'X', 1: 'Y', 2: 'Z'}[cmds.getAttr(nodeName + '.axis' )],
    "linearDamping" : cmds.getAttr(nodeName + '.linearDamping' ),
    "angularDamping" : cmds.getAttr(nodeName + '.angularDamping' ),
    "impulsePosition" : [i for i in cmds.getAttr(nodeName + '.impulsePosition' )[0]],
    "extents" : [i for i in cmds.getAttr(nodeName + '.extents' )[0]],
    "centerOfMass" : [i for i in cmds.getAttr(nodeName + '.centerOfMass' )[0]],
    "colliderOffset" : [i for i in cmds.getAttr(nodeName + '.colliderShapeOffset' )[0]],
    "constraints" : getRigidBodyConstraints(nodeName)
  }


def getConstraintData(nodeName):

  shape = cmds.listRelatives(nodeName, s=1)[0]

  return {
    'rigidBodyA' : cmds.listConnections(shape + '.rigidBodyA', sh=1)[0],
    'rigidBodyB' : cmds.listConnections(shape + '.rigidBodyB', sh=1)[0],
    "type" : {0: "point",1: "hinge",2: "slider",3: "coneTwist",4: "sixDof"}[cmds.getAttr(nodeName + '.constraintType' )],
    "translate" : [i for i in cmds.getAttr(nodeName + '.translate' )[0]],
    "linearConstraintMin" : [i for i in cmds.getAttr(nodeName + '.linearConstraintMin' )[0]],
    "linearConstraintMax" : [i for i in cmds.getAttr(nodeName + '.linearConstraintMax' )[0]],
    "angularConstraintMin" : [i for i in cmds.getAttr(nodeName + '.angularConstraintMin' )[0]],
    "angularConstraintMax" : [i for i in cmds.getAttr(nodeName + '.angularConstraintMax' )[0]],
    "linearSpringDamping" : [i for i in cmds.getAttr(nodeName + '.linearSpringDamping' )[0]],
    "linearSpringStiffness" : [i for i in cmds.getAttr(nodeName + '.linearSpringStiffness' )[0]],
    "angularSpringDamping" : [i for i in cmds.getAttr(nodeName + '.angularSpringDamping' )[0]],
    "angularSpringStiffness" : [i for i in cmds.getAttr(nodeName + '.angularSpringStiffness' )[0]]
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

  print i
  # get parent
  parent = cmds.listRelatives( i, p=1 )

  # get children
  children = cmds.listRelatives( i, c=1, type='joint' )
  
  # get constraints
  parentConstraints = [cmds.parentConstraint(c, q=1,targetList=1 )[0] for c in cmds.listRelatives(i, type="parentConstraint")]

  print parentConstraints

  meshData["jointData"][i] = {
    "name" : i,
    "position" : cmds.xform(i, q=1, translation=1, worldSpace=True),
    "scale" : cmds.xform(i, q=1, scale=1, worldSpace=True),
    "rotation" : cmds.xform(i, q=1, rotation=1, worldSpace=True),
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

  print i

  for rb in meshData["jointData"][i]["rigidBodies"]:
    print rb
    rigidBodies[rb] = getRigidBodyInfo(rb)


meshData["rigidBodies"] = rigidBodies


# get the names for each constraint
meshData['constraints'] = {}
for i in meshData["rigidBodies"]:

  for c in meshData["rigidBodies"][i]["constraints"]:
    meshData['constraints'][c] = getConstraintData(c)


# populate the constraint data
for i in meshData['constraints']:
  print i, meshData['constraints'][i]



print meshData["jointData"]

# write a json file
exportText(json.dumps(meshData, indent=4), getFileLocation(0, '.json'))
# json.dumps(meshData, indent=4)


cmds.select(origSelect, r=1)