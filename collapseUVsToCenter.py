# collapseUVsToCenter.py


if 'includeScript' not in locals():
  def includeScript(path, cwd=''):
    exec (open(cwd + path, 'r').read(), globals())

# includes
includeScript('getMeshData.py', '/Users/laserstorm/MayaUsefulScripts/')


# cmds.polyEditUV( relative=False, uValue=0.556, vValue=0.56 )



selection = cmds.ls(sl=1, fl=1)


for m in selection:
  cmds.ConvertSelectionToFaces()

  for f in cmds.ls(sl=1, fl=1):
    fv = cmds.polyInfo(f, fv=1)[0].split('     ')[2:]
    print fv


cmds.select(selection, r=1)