if 'cmds' not in locals():
	import maya.cmds as cmds
import math


def spherify(radius=10):

    def distance(p1,p2):
        return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2)+((p1[2]-p2[2])**2))
    def normalize(v):
        length = math.sqrt(v[0]**2 +v[1]**2 +v[2]**2) 
        return [v[0]/length, v[1]/length, v[2]/length ]

    selected = cmds.ls(sl=1,fl=1)
    #get some vertices to work with
    cmds.ConvertSelectionToVertices()
    vertices = cmds.ls(sl=1,fl=1)



    #find centroid
    centroid = [0,0,0]
    for i in range(0,len(vertices)):
    	p = vertices[i]
    	pos = cmds.pointPosition( vertices[i] )
    	centroid[0] += pos[0]
    	centroid[1] += pos[1]
    	centroid[2] += pos[2]
    centroid[0] /= len(vertices)
    centroid[1] /= len(vertices)
    centroid[2] /= len(vertices)

    #move the vertices 
    for v in vertices:
        pos = cmds.pointPosition( v )
        diff = normalize( [pos[0] - centroid[0], pos[1] - centroid[1], pos[2] - centroid[2] ] )
        dist = distance( centroid, pos )
        pos = [ centroid[0]+diff[0]*radius,  centroid[1]+diff[1]*radius,  centroid[2]+diff[2]*radius ]
        cmds.select( v, r=1)
        cmds.move( pos[0], pos[1], pos[2] )

    cmds.select(selected, r=1)
spherify(10)