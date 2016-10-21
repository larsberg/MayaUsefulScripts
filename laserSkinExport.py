import json

if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes 
includeScript('getMeshData.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getSkinInfo.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('exportText.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getFileLocation.py', '/Users/laserstorm/MayaUsefulScripts/')


cmds.select('mesh', r=1)

m = cmds.ls(sl=1,fl=1)[0]

# mesh data
meshData = getMeshData( m )

# skin weights
skinWeights = getSkinInfo( m )
# skinWeights["numJointWeightsPerVertex"] = (skinWeights["weights"][0])


# get the joint transforms
jointNames = skinWeights["joints"]

print jointNames


for i in skinWeights:
  meshData[i] = skinWeights[i]


for i in meshData:
  print i



# write a json file
exportText(json.dumps(meshData, indent=4), getFileLocation(0, '.json'))