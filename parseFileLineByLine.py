# parseFileLineByLine.py

def includeScript(path, cwd=''):
  # print script
  exec (open(cwd + path, 'r').read(), globals())


includeScript('laserMayaImports.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('getFileLocation.py', '/Users/laserstorm/MayaUsefulScripts/')
includeScript('exportText.py', '/Users/laserstorm/MayaUsefulScripts/')


loc = "/Users/laserstorm/Tool_Lexus/model.csv" # getFileLocation()

print loc

count = 0
output = []
with open(loc) as f:
  for line in f:
    count += 1

    if count > 1:
      l = eval("[" + line.replace('\n', '') + "]")
      output.append( "v " + l[2].replace(', ', ' '))

exportText('\n'.join(output), getFileLocation());