
if 'om' not in locals():
  import maya.api.OpenMaya as om

if 'oma' not in locals():
  import maya.api.OpenMayaAnim as oma


def getMObjectForNode(nodeName):
    sel = om.MSelectionList();
    sel.add(nodeName)
    return sel.getDependNode(0)


def getDagPathForNode(nodeName):
    sel = om.MSelectionList();
    sel.add(nodeName)
    result = om.MDagPath()
    result = sel.getDagPath(0)

    if not result.isValid():
        raise MessageException("node %s does not exist" % nodeName) 
    return result