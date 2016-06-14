# exportText.py

def exportText( text, path ):
  t = open(path, "w")
  t.write( text )
  t.close()