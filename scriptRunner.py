# a useful reference for maya UI stuff: 
# http://tech-artists.org/forum/showthread.php?3292-maya-python-UI-acessing-controls-from-external-functions


if 'cmds' not in locals():
  import maya.cmds as cmds


class ScriptRunner():

  def __init__(self, filePath = None ):
    self.filePath = filePath
    self.currentField = None
    self.setupWindow()

  def getFileLocation( self ):
    return cmds.fileDialog2(fileMode = 1)[0]

  def scrollField(self, executeField=0):
    # John Scrollfield
    if self.currentField == None:
      self.currentField = cmds.cmdScrollFieldExecuter( t = self.readFile( self.filePath ), opc=1, sln=1, exa=executeField, sourceType="python") 

    else:
      cmds.cmdScrollFieldExecuter( self.currentField, e=True, t=self.readFile( self.filePath ), opc=1, sln=1, exa=executeField, sourceType="python") 


  def setFilePath( self ):
    self.filePath = self.getFileLocation()
    cmds.window( self.window, e=True, t=self.filePath.split('/').pop() )
    self.scrollField(0)

  def readFile( self, path ):
    t = open( path, "r")
    ouput = t.read()
    t.close();
    return ouput

  # MAYA UI buttons execute commands with *args [self, ... ]
  def setFilePathButton( *args ):
    args[0].setFilePath()
    
  def runPath( *args ):
    
    self = args[0]

    if self.filePath == None:
      self.setFilePath()

    self.scrollField(1)


  def setupWindow( self ):
      
    # create a window
    self.window = cmds.window( width=180, rtf = True , t = "scriptRunner" )
    cmds.columnLayout( adj = True )
    cmds.button( label='load script', height = 40, command = self.setFilePathButton )
    cmds.button( label='run script', height = 40, command = self.runPath )
    cmds.showWindow( self.window )

ScriptRunner()

