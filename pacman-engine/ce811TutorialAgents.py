# ce811TutorialAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
#
# Adapted for CE811 by M. Fairbank
# Put your agents for the CE811 pacman tutorial in here.

from util import manhattanDistance
from game import Directions
import random, util
from dijkstra import Dijkstra
from game import Agent

from dataCollector import DataCollector
import heapq

class ce811GoWestAgent(Agent):

  def getAction(self, gameState):
    #legalMoves = gameState.getLegalActions()
    return Directions.WEST
    #return random.choice(legalMoves) 



class ce811GoSouthWestAgent(Agent):
  def getAction(self, gameState):
    legalMoves = gameState.getLegalActions()
    if Directions.SOUTH in legalMoves:
      return Directions.SOUTH
    else:
      return Directions.WEST


class ce811ManhattanFoodSeekerAgent(Agent):

  def getAction(self, gameState):
    legal_moves = gameState.getLegalActions()
    pacman_pos = gameState.getPacmanPosition()
    #print("pacman_pos",pacman_pos) # useful for debugging
    food_locations=gameState.getFood().asList()
    assert len(food_locations)==1,"For this exercise, we should always run this crossMaze with the commnadline option: -d 1"
    food_location=food_locations[0] #gets the first value of the list (there's only one food item in this board!)
    #print("food_location",food_location) # useful for debugging
    # Note that pacman_pos and food_location are both tuples of the form (x,y).
    # The origin is such that (0,0) is the top-left of the game board
    # Hence if the food's y coordinate is higher than pacman's y coordiante then we know the food is below us.
    # Similarly, if the food's x coordinate is higher than pacman's x coordiante then we know the food is to the east of us.
    food_x,food_y=food_location # unpack the tuple (x,y) into some more conventient variable names
    pacman_x,pacman_y=pacman_pos # unpack the tuple (x,y) into some more conventient variable names
    if food_y>pacman_y:
        return Directions.SOUTH 
    elif food_y<pacman_y:
        return Directions.NORTH
    elif food_x>pacman_x:
        return Directions.EAST 
    elif food_x<pacman_x:
        return Directions.WEST 
    # Should never get here!
    raise Exception("Should never get here")


class ce811ManhattanGhostDodgerAgent(Agent):
  

  def getAction(self, gameState):
    
    legal_moves = gameState.getLegalActions()
    pacman_pos = gameState.getPacmanPosition()
    food_locations=gameState.getFood().asList()
    food_location=food_locations[0]
    food_x,food_y=food_location
    pacman_x,pacman_y=pacman_pos # unpack the tuple (x,y) into some more conventient variable names
    ghost_positions = gameState.getGhostPositions()
    ghost_x,ghost_y=ghost_positions[0]
    ghost_states = gameState.getGhostStates()
    ghost_movement_directions = [ghostState.getDirection() for ghostState in ghost_states]
    good_moves=legal_moves

    good_moves.remove(Directions.STOP)
    if ghost_movement_directions[0]=="South" and  Directions.NORTH in good_moves:
        return Directions.NORTH
    if ghost_movement_directions[0]=="North" and  Directions.SOUTH in good_moves:
        return Directions.SOUTH
    if Directions.WEST in good_moves:
      return Directions.WEST
    if Directions.EAST in good_moves:
      return Directions.EAST
    
    return Directions.STOP


class ce811ManhattanGhostDodgerHunterAgent(Agent):
  def getAction(self, gameState):
    # Collect legal moves and successor states
    legal_moves = gameState.getLegalActions()
    # locate pacman
    pacman_pos = gameState.getPacmanPosition()
    #locate ghosts:
    pacman_x,pacman_y=pacman_pos 
    ghost_states = gameState.getGhostStates()
    ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    ghost_movement_directions = [ghostState.getDirection() for ghostState in ghost_states]
    ghost_positions = gameState.getGhostPositions()
    ghost_x,ghost_y=ghost_positions[0]
    ghost_positions=[manhattanDistance(pacman_pos, ghost_pos) for ghost_pos in ghost_positions]
    ghost_distances_scared = [ghost_dist for ghost_dist,time in zip(ghost_positions,ghost_scared_times) if time>1]
    ghost_distances_dangerous = [ghost_dist for ghost_dist,time in zip(ghost_positions,ghost_scared_times) if time<=1]
    
    #locate closest food dot:
    food_locations=gameState.getFood().asList()
    food_distances = [manhattanDistance(pacman_pos, food_pos) for food_pos in food_locations]
    closest_food_location=food_locations[food_distances.index(min(food_distances))]
    food_x,food_y=closest_food_location
    distance_closest_food_loc=manhattanDistance(pacman_pos, closest_food_location)
    good_moves=legal_moves
    if ghost_movement_directions[0]=="South" and  Directions.NORTH in good_moves and ghost_x!=pacman_x:
        return Directions.NORTH
    if ghost_movement_directions[0]=="North" and  Directions.SOUTH in good_moves and ghost_x!=pacman_x:
        return Directions.SOUTH
    if ghost_movement_directions[0]=="East" and Directions.WEST in good_moves and ghost_y!=pacman_y:
      return Directions.WEST
    if ghost_movement_directions[0]=="West" and Directions.EAST in good_moves and ghost_y!=pacman_y:
      return Directions.EAST

    if ghost_movement_directions[0]=="South" and  Directions.SOUTH in good_moves and ghost_x==pacman_x:
        return Directions.SOUTH
    if ghost_movement_directions[0]=="North" and  Directions.NORTH in good_moves and ghost_x==pacman_x:
        return Directions.NORTH
    if ghost_movement_directions[0]=="West" and Directions.WEST in good_moves and ghost_y==pacman_y:
      return Directions.WEST
    if ghost_movement_directions[0]=="East" and Directions.EAST in good_moves and ghost_y==pacman_y:
      return Directions.EAST

    if ghost_positions[0]>distance_closest_food_loc:
      if food_y>pacman_y and Directions.SOUTH in good_moves:
        return Directions.SOUTH 
      elif food_y<pacman_y and Directions.NORTH in good_moves:
        return Directions.NORTH
      elif food_x>pacman_x and Directions.EAST in good_moves:
        return Directions.EAST 
      elif food_x<pacman_x and Directions.WEST in good_moves:
        return Directions.WEST

    return Directions.STOP

class ce811DijkstraRuleAgent(Agent):
  def get_smallest_elements(self,input_list):
    if len(input_list) <= 4:
        return input_list
    smallest_elements = heapq.nsmallest(4, input_list)
    return smallest_elements
  def getAction(self, gameState):
    dijkstra=Dijkstra()
    data_collector=DataCollector()
    # Collect legal moves and successor states
    legal_moves = gameState.getLegalActions()
    # locate pacman
    pacman_pos = gameState.getPacmanPosition()
    #locate ghosts:
    maze=gameState.getWalls()
    array_gScores, parent_nodes=dijkstra.calculate_gscores(maze,pacman_pos)

    ghost_states = gameState.getGhostStates()
    ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    ghost_positions = gameState.getGhostPositions()
   
    ghost_distances_dangerous = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time<=1]
    ghost_distances_scared = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time>2]
    closest_ghost=min(ghost_distances_dangerous) if len(ghost_distances_dangerous)>0 else 0
    if len(ghost_distances_dangerous)>0:
      closest_ghost_location=ghost_positions[ghost_distances_dangerous.index(min(ghost_distances_dangerous))]
      ghost_x,ghost_y=closest_ghost_location
      path_to_ghost=dijkstra.calc_path_to_point(pacman_pos,(int(ghost_x),int(ghost_y)),parent_nodes)
    capsule_positions = gameState.getCapsules()
    capsule_distances=[array_gScores[capsule_pos_y][capsule_pos_x] for capsule_pos_x,capsule_pos_y in capsule_positions]
    
    #locate closest food dot:
    food_locations=gameState.getFood().asList()
    food_distances = [array_gScores[food_pos_y][food_pos_x] for food_pos_x,food_pos_y in food_locations]
    min_food_distance = min(food_distances) if len(food_distances)>0 else 0
    closest_food_location=food_locations[food_distances.index(min(food_distances))]
    path_to_food=dijkstra.calc_path_to_point(pacman_pos,closest_food_location,parent_nodes)

    good_moves=legal_moves
    good_moves.remove(Directions.STOP)
    value_return=None
    if len(ghost_distances_dangerous)>0 and closest_ghost<=5:
          if path_to_ghost[0] in good_moves:
            good_moves.remove(path_to_ghost[0])
    if path_to_food[0] in good_moves:
          value_return=path_to_food[0]
          #return path_to_food[0]
    else:
      if len(good_moves)>0:
        indices=range(len(good_moves))
        chosen_index=random.choice(indices)
        value_return= good_moves[chosen_index]
      else:
        value_return= Directions.STOP
    
    #Ensure there is always information, in case there is not, it is filled with -1
    if len(ghost_distances_dangerous) < 2:
      ghost_distances_dangerous.extend([-1] * (2 - len(ghost_distances_dangerous)))
    if len(ghost_distances_scared) < 2:
      ghost_distances_scared.extend([-1] * (2 - len(ghost_distances_scared)))
    if len(capsule_distances) < 2:
      capsule_distances.extend([-1] * (2 - len(capsule_distances)))
    if len(ghost_positions) < 2:
      ghost_positions.extend([(-1,-1)] * (2 - len(ghost_positions)))
    if len(capsule_positions) < 2:
      capsule_positions.extend([(-1,-1)] * (2 - len(capsule_positions)))
    closest_4th_food_location=[]
    smallest_4th_distances=self.get_smallest_elements(food_distances)
    for i in range(len(smallest_4th_distances)):
      closest_4th_food_location.append(food_locations[food_distances.index(smallest_4th_distances[i])])
      
    if len(closest_4th_food_location) < 4:
      closest_4th_food_location.extend([(-1,-1)] * (4 - len(closest_4th_food_location)))

    data_collector.writeLine(pacman_pos[0],pacman_pos[1],ghost_positions[0][0],ghost_positions[0][1],ghost_distances_dangerous[0],
    ghost_positions[1][0],ghost_positions[1][1],ghost_distances_dangerous[1],ghost_distances_scared[0],ghost_distances_scared[1],
    closest_4th_food_location[0][0],closest_4th_food_location[0][1],
    capsule_positions[0][0],capsule_positions[0][1],capsule_distances[0],capsule_positions[1][0],capsule_positions[1][1],capsule_distances[1],gameState.getScore(),value_return)



    return value_return