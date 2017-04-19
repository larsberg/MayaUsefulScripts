# SpaceLocAtAveragePoint.py


# getMeshData.py
if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes
includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')

selected = cmds.ls(sl=1, fl=1)

p = om.MVector()


for i in selected:
  pos = cmds.pointPosition(i)

  p.x += pos[0]
  p.y += pos[1]
  p.z += pos[2]

p /= len(cmds.ls(sl=1, fl=1))



cmds.spaceLocator(p=p)

cmds.select(selected, r=1)

