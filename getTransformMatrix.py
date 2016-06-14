def getTransformMatrix( transform ):
  return cmds.xform( transform, q=1, m=1, os=1, worldSpace=True )
