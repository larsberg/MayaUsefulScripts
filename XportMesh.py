# XportMesh.py

import json

if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes
includeScript('getMeshData.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('exportText.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getFileLocation.py', '/Users/laserstorm/MayaUsefulScripts/')


def exportJson(dic, pretty=False):
  if pretty:
    exportText(json.dumps(dic, indent=2), getFileLocation(0, '.json'))
  else:
    exportText(json.dumps(dic), getFileLocation(0, '.json'))


def meshToData(m):

  # mesh data
  meshData = getMeshData( m )

  # add the transform
  meshData['transform'] = cmds.xform(m, q=1, m=1, worldSpace=True )

  # # flatten arrays
  # meshData['position'] = [ p[i] for p in meshData['position'] for i in range(3) ]
  # meshData['normal']   = [ n[i] for n in meshData['normal'] for i in range(3) ]
  # meshData['uv']       = [ u[i] for u in meshData['uv'] for i in range(2) ]

  # meshData['itemSize'] = {
  #   'position' : 3,
  #   'normal' : 3,
  #   'uv' : 2
  # }

  return meshData


selected = cmds.ls(sl=1, fl=1)


scene = {
  'mesh' : []
}


for i in selected:

  # print i
  scene['mesh'].append( meshToData(i) )



exportJson(scene, True)





cmds.select(selected, r=1)