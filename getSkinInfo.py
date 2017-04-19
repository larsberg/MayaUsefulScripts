
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())


# includes 
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('printProgress.py', '/Users/laserstorm/MayaUsefulScripts/')



def getJoints( mesh ):
  return cmds.skinCluster( mesh, query=True, inf=True )

def getMeshSkin( mesh ):

  joint = getJoints( mesh )[0]
  skin = cmds.listConnections( joint, t='skinCluster' )

  return skin.pop()



def flattenArray(forest, maxIndex = 3):
  return [leaf for tree in forest for index, leaf in enumerate(tree) if index < maxIndex]


def getSkinWeights(skinFn, meshDag):

  # get the per vertex joint weights
  jointWeights = []
  jointIndices = []
  vertIter = om.MItMeshVertex(meshDag)

  numWeightsPerVertex = 0

  for i in range(vertIter.count()):

    vertIter.setIndex(i)

    # get the skin weights
    vertexWeights = skinFn.getWeights(meshDag, vertIter.currentItem())[0]

    # trim the empty weights and get the joint index
    vertexJointData = [ (index, w) for index, w in enumerate(vertexWeights) if w > 0.0]

    numWeightsPerVertex = max(len(vertexJointData), numWeightsPerVertex);

    jointIndices.append( [ w[0] for w in vertexJointData] )
    jointWeights.append( [ w[1] for w in vertexJointData] )
  
    printProgress(i, vertIter.count(), 'getSkinWeights:')

  # make sure they all have the right number of weights
  for i in jointWeights:
    if len(i) < numWeightsPerVertex:
      
      print "numWeightsPerVertex: " + str(len(i))
      
      for j in range(len(i), numWeightsPerVertex):
        i.append( (0,0) )

  return (jointWeights, jointIndices, numWeightsPerVertex)



def getSkinInfo(nodeName):

  meshDag = getDagPathForNode(nodeName)

  skinClusterName = getMeshSkin(m)

  skinFn = oma.MFnSkinCluster(getMObjectForNode(skinClusterName))

  weights = getSkinWeights(skinFn, meshDag)

  print [ j.partialPathName() for j in skinFn.influenceObjects()]

  return {
    'vertexJointWeights' : weights[0],
    'vertexJointIndices' : weights[1],
    "numWeightsPerVertex" : weights[2],
    'jointNames' : [ j.partialPathName() for j in skinFn.influenceObjects()] # skinFn.influenceObjects()
  }
