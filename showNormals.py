# showNormals.py


for o in cmds.ls(sl=1, fl=1):

  cmds.setAttr( o + '.displayNormal', 1)
  cmds.setAttr( o + '.normalSize', 10)