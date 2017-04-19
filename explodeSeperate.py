# explodeObjects.py


# getMeshData.py
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')



def explodeSeperate( objectList, scale, center = om.MVector(0,0,0)):

  for obj in objectList:

    pos = om.MVector(cmds.objectCenter(obj, gl=True))

    newPos = pos * scale

    cmds.xform(obj, translation=newPos, worldSpace=True)



explodeSeperate(cmds.ls(sl=1,fl=1), 3)