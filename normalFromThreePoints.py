# normalFromPoints.py

def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('laserOpenMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')


def normalFromThreePoints( a, b, c ):

  cb = (c - b).normalize()

  ab = (a - b).normalize()

  return cb ^ ab
