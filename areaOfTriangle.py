# pass three OpenMaya.Vectors
def areaOfTriangle(p0, p1, p2):
  return ((p2 - p1) ^ (p0 - p1)).length() * .5;