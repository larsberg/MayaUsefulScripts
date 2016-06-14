
def getFileLocation(filemode=0, fileType="All Files (*.*)"):
  return cmds.fileDialog2(fileMode=filemode, ff=fileType)[0]