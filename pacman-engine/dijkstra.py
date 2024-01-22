import numpy as np
import layout
from game import Directions
class Dijkstra:
    def calc_path_A_to_B(self,start_node, end_node, maze_walls):
        # This function is just a wrapper for calc_path_to_point below
        # This function is written for you - no need to change anything in this short function.
        gScores,parent_nodes=self.calculate_gscores(maze_walls, start_node)
        return self.calc_path_to_point(start_node,end_node, parent_nodes)

    def calc_path_to_point(self,start_node,end_node, parent_nodes): 
        path=[]    
        while start_node!=end_node:
            parent_node=parent_nodes[end_node]
            end_node_x,end_node_y=end_node
            parent_node_x,parent_node_y=parent_node
            if end_node_x==parent_node_x:
                if end_node_y>parent_node_y:
                    path.insert(0,Directions.SOUTH)
                else:
                    path.insert(0,Directions.NORTH)
            elif end_node_y==parent_node_y:
                if end_node_x<parent_node_x:
                    path.insert(0,Directions.WEST)
                else:
                    path.insert(0,Directions.EAST)
            end_node=parent_node
        return path 
    def calculate_neighbouring_nodes(self,node, maze):
        maze_height=maze.height
        maze_width=maze.width
        directions=[(1,0),(-1,0),(0,1),(0,-1)]
        (x,y)=node
        result_neigbours={}
        for (dx,dy) in directions:
            neighbour_y=y+dy
            neighbour_x=x+dx
            # check if this potential neighbour goes off the edges of the maze:
            if neighbour_y>=0 and neighbour_y<maze_height and neighbour_x>=0 and neighbour_x<maze_width:
                # check if this potential neighbour is not a wall:
                if maze[neighbour_x][neighbour_y]==False:
                    # we have found a valid neighbouring node that is not a wall
                    result_neigbours[(neighbour_x,neighbour_y)]=1 # this says the distance to this neighbour is 1
                    # Note that all neighbours in this problem are distance 1 away!
        return result_neigbours


    def calculate_gscores(self,maze, start_node):
        assert str(type(maze))=="<class 'game.Grid'>"
        maze_height=maze.height
        maze_width=maze.width
        end_node=(maze_height-1,maze_width-1)
        assert maze[start_node[0]][start_node[1]]==False,"start_node error "+str(start_node) # start node must point to a False in the maze array
        
        array_gScores, parent_nodes=self.dijkstra_algorithm(maze, start_node, end_node)
        return [array_gScores, parent_nodes]


    def dijkstra_algorithm(self,maze, start_node, end_node):
        # on entry, maze is a nested list (2d-array) of 1s and 0s indicating maze walls and corridors respectively.
        maze_height=maze.height
        maze_width=maze.width
        assert maze[start_node[0]][start_node[1]]==False, "Start node must point to a zero of the maze array"

        # Identify all nodes of the graph.  A node is a tuple object (x,y) corresponding to the location of the node in the maze.
        nodes=[(x,y) for x in range(maze_width) for y in range(maze_height) if maze[x][y]==False] 
        # store all of each node's immediate neighbours in a dictionary for speedy reference:                
        neighbouring_nodes={node:self.calculate_neighbouring_nodes(node, maze) for node in nodes} 
        # The above line builds our "graph" of nodes and connections.  
        # Each connection is length 1 - which is rather inefficient.  Maybe we 
        # could skip lots of nodes which form a long corridor? 
        # See https://www.youtube.com/watch?v=rop0W4QDOUI for a discussion of one way to do that.
                                

        # Now implement Dijkstra's algorithm
        open_nodes=[start_node] # seed the flood-fill search to expand from here.
        parentNodes={start_node: None} # These hold which node precedes this one on the best route.
        nodeGValues={start_node: 0} # These hold the distance of each node from the start node.
        closed_list = [] # List of nodes that are completely finished
        for i in nodes:
            if i!=start_node:
                nodeGValues[i]=999999999

        while len(open_nodes)>0:
            sorted_list_of_open_nodes_nodes=sorted(open_nodes, key = lambda n: nodeGValues[n]) # this sorts the open_nodes nodes list by gValues first.
            current_node = sorted_list_of_open_nodes_nodes[0] # this pulls off the first (i.e. shortest-distance) open_nodes item.
            current_distance=nodeGValues[current_node]
            closed_list.append(current_node)
            open_nodes.remove(current_node)

            #consider all of the neighbours of the current node:
            for neighbour_node, neighbour_distance in neighbouring_nodes[current_node].items():
                if neighbour_node not in closed_list:
                    if neighbour_node not in open_nodes:
                        open_nodes.append(neighbour_node)
                    temp_distance=neighbour_distance+current_distance
                    if temp_distance<nodeGValues[neighbour_node]:
                        nodeGValues[neighbour_node]=temp_distance
                        parentNodes[neighbour_node]=current_node
        
        array_gScores=np.zeros((maze_height, maze_width),dtype=int)
        for n in nodes:
            (x,y)=n
            if n not in nodeGValues:
                raise Exception("Not a fully connected maze!")
            array_gScores[y,x]=nodeGValues[n]
        return[array_gScores,parentNodes]