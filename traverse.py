
def traverseDown( obj, callback ):
    
  children = cmds.listRelatives(obj, c=1)
  # children = getChildren( obj )
  
  if children != None:
    
    for i in children:
  
      traverseDown( i, callback )
      
  callback( obj )

  

def traverseUp( obj, callback ):

  p = cmds.listRelatives(obj, p=1)
  # p = getParent( obj )
  
  if p != None:
    
    traverseUp( p, callback )
    
  callback( obj )