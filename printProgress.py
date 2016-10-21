
if 'printProgress' not in locals():
  def printProgress(index, total, message = '', increment = 1000):
    if index % increment == 0 or index == total - 1:
      print message + ' ' + str( 100 * index / (total-1) ) + "% complete"
      cmds.refresh()