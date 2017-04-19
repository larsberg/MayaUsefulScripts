# setTranslationToPivot.py

def setTranslationToPivotPosition( node ):

  pivotPos = cmds.xform(node, q=1, ws=1, rp=1)

  cmds.xform( node, t=[ -i for i in pivotPos ], ws=True)

  cmds.makeIdentity(node, t=True, apply=True)

  cmds.xform( node, t=pivotPos, ws=True )


for node in cmds.ls(sl=1, fl=1):
  setTranslationToPivotPosition(node)