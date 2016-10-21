
def traverseDown( obj, callback ):
    
  children = getChildren( obj )
  
  if children != None:
    
    for i in children:
  
      traverseDown( i, callback )
      
  callback( obj )

  

def traverseUp( obj, callback ):

  p = getParent( obj )
  
  if p != None:
    
    traverseUp( p, callback )
    
  callback( obj )