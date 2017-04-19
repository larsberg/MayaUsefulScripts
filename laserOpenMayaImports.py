
if 'om' not in locals():
  import maya.api.OpenMaya as om

# TODO: remove this one...
if 'OpenMaya' not in locals():
    import maya.api.OpenMaya as OpenMaya

if 'oma' not in locals():
  import maya.api.OpenMayaAnim as oma

if 'omr' not in locals():
    import maya.OpenMayaRender as omr


# get mesh
def getDagPath(nodeName):
  return om.MGlobal.getSelectionListByName(nodeName).getDagPath(0)

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