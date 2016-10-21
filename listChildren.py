def listChildren(obj, type=None):
  if type:
    return cmds.listRelatives( obj, children=1, type=type, ni=True)
  else:
    return cmds.listRelatives( obj, children=1, ni=True)
