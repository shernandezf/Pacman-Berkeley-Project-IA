from game import Directions
from game import Agent
from game import Actions
from util import manhattanDistance
import random
import numpy as np
from dijkstra import Dijkstra
import tensorflow as tf
from tensorflow import keras

import heapq
class ce811OneStepLookaheadManhattanAgent(Agent):
 

  def getAction(self, gameState):
 
    legalMoves = gameState.getLegalActions()
    legalMoves = [i for i in legalMoves if i != "Stop"]
   
    scores = [self.evaluateBoardState(gameState.generatePacmanSuccessor(action)) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) 
    return legalMoves[chosenIndex]
  def eval_food(self,food_amount):
    return 100/food_amount
  def eval_food_distance(self,food_distance):
    random_multiplier=random.randint(1, 3)
    return (10000/food_distance)*random_multiplier
  def eval_ghost_distance(self,ghost_dist):
    eval=0
    for i in ghost_dist:
      if i<3:
        eval+=(100000000/i)
    return (-1*eval)
  def eval_ghost_distance_scared(self,ghost_dist):
    return 1000/ghost_dist
  
  def evaluateBoardState(self,gameState):
  
    pacman_pos = gameState.getPacmanPosition()
    food_positions = gameState.getFood().asList()
    ghost_states = gameState.getGhostStates()
    ghost_positions = gameState.getGhostPositions()
    ghost_movement_directions = [ghostState.getDirection() for ghostState in ghost_states]
    ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    capsule_positions = gameState.getCapsules()
    capsule_distances=[manhattanDistance(pacman_pos, capsule_pos) for capsule_pos in capsule_positions]
    food_distances = [manhattanDistance(pacman_pos, food_pos) for food_pos in food_positions]
    min_food_distance = min(food_distances) if len(food_distances)>0 else 0
    num_food_left=len(food_distances)

    ghost_distances_dangerous = [manhattanDistance(pacman_pos, ghost_pos) for ghost_pos,time in zip(ghost_positions,ghost_scared_times) if time<=1]
    ghost_distances_scared = [manhattanDistance(pacman_pos, ghost_pos) for ghost_pos,time in zip(ghost_positions,ghost_scared_times) if time>1]

    evaluation=0
    if num_food_left>0:
      evaluation+=self.eval_food(num_food_left)
      evaluation+=self.eval_food_distance(min_food_distance)
    if len(ghost_distances_dangerous)>0:
      if min(ghost_distances_dangerous)>0:
        evaluation+=self.eval_ghost_distance(ghost_distances_dangerous)
    if len(ghost_distances_scared)>0:
      if min(ghost_distances_scared)<2 and min(ghost_distances_scared)>0:
        evaluation+=self.eval_ghost_distance_scared(min(ghost_distances_scared))
    
    
    return evaluation 

class ce811OneStepLookaheadDijkstraAgent(Agent):

  def getAction(self, gameState):
    """  
    Just like in the tutorial, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()
    legalMoves = [i for i in legalMoves if i != "Stop"]
    # Choose one of the best actions
    scores = [self.evaluateBoardState(gameState.generatePacmanSuccessor(action)) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    return legalMoves[bestIndices[0]]
  def eval_future_food(self,pacman_pos,food_positions):
    evaluation=0
    pacman_pos_x,pacman_pos_y=pacman_pos
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    for (dx,dy) in directions:
      neighbour_food_y=pacman_pos_x+dy
      neighbour_food_x=pacman_pos_x+dx
      if (neighbour_food_x,neighbour_food_y) in food_positions:
        evaluation+= 50000
      else:
        evaluation+= 0
      return evaluation
  def eval_food(self,food_amount):
  
    return 1000000000/food_amount
  def eval_food_distance(self,food_distance):
    return 1000/food_distance
  def eval_ghost_distance(self,ghost_dist):
    evaluation=0
    for i in ghost_dist:
      if i<3:
        evaluation+=(100000000/i)
    return (-1*evaluation)
  def eval_ghost_distance_scared(self,ghost_dist):
    evaluation=0
    for i in ghost_dist:
      if i<2:
        evaluation+=(1000000/i)
    return evaluation

  def evaluateBoardState(self,gameState):
    
    dijkstra=Dijkstra()
    pacman_pos = gameState.getPacmanPosition()
    #list of tuples (x,y)
    food_positions = gameState.getFood().asList()
    #object ghost
    ghost_states = gameState.getGhostStates()
    #list of tuples [(6.0, 6.5), (7.5, 9.0)]
    ghost_positions = gameState.getGhostPositions()
    # list of two direction ["North","West"]
    maze=gameState.getWalls()
  
    array_gScores, parent_nodes=dijkstra.calculate_gscores(maze,pacman_pos)
    ghost_movement_directions = [ghostState.getDirection() for ghostState in ghost_states]
    # list of two scared times [0,0]
    ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    # list of tuples [(1, 1), (18, 9)]
    capsule_positions = gameState.getCapsules()
    capsule_distances=[array_gScores[capsule_pos_y][capsule_pos_x] for capsule_pos_x,capsule_pos_y in capsule_positions]
    #list of numbers with the distance [3, 4, 5]
    food_distances = [array_gScores[food_pos_y][food_pos_x] for food_pos_x,food_pos_y in food_positions]
    min_food_distance = min(food_distances) if len(food_distances)>0 else 0
    num_food_left=len(food_distances)
    ghost_distances_dangerous = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time<=1]
    ghost_distances_scared = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time>2]
    
    evaluation=gameState.getScore() # Encourage actually scoring points.  This is immediate and useful.  
    #evaluation=0
    # Also including game score stops pacman getting trapped becuase by eating one isolated food item, the closest food appears to move further away (which is bad).  
    if num_food_left>0:
      evaluation+=self.eval_future_food(pacman_pos,food_positions)
      evaluation+=self.eval_food(num_food_left)
      evaluation+=self.eval_food_distance(min_food_distance)
    elif num_food_left==0:
      evaluation+=100000000000
    if len(ghost_distances_dangerous)>0:
      if min(ghost_distances_dangerous)>0:
        evaluation+=self.eval_ghost_distance(ghost_distances_dangerous)
    if len(ghost_distances_scared)>0:
      evaluation+=self.eval_ghost_distance_scared(ghost_distances_scared)

    
    return evaluation 



class ce811MyBestAgent(Agent):
  def eval_future_food(self,pacman_pos,food_positions):
    evaluation=0
    pacman_pos_x,pacman_pos_y=pacman_pos
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    for (dx,dy) in directions:
      neighbour_food_y=pacman_pos_x+dy
      neighbour_food_x=pacman_pos_x+dx
      if (neighbour_food_x,neighbour_food_y) in food_positions:
        evaluation+= 50000
      else:
        evaluation+= 0
      return evaluation
  def eval_food(self,food_amount):
  
    return 1000000000/food_amount
  def eval_food_distance(self,food_distance):
    return 1000/food_distance
  def eval_ghost_distance(self,ghost_dist):
    evaluation=0
    for i in ghost_dist:
      if i<3:
        evaluation+=(100000000/i)
    return (-1*evaluation)
  def eval_ghost_distance_scared(self,ghost_dist):
    evaluation=0
    for i in ghost_dist:
      if i<2:
        evaluation+=(1000000/i)
    return evaluation
  
  def getAction(self, gameState):
    #INITIAL INFO
    legal_moves = gameState.getLegalActions()
    dijkstra=Dijkstra()
    pacman_pos = gameState.getPacmanPosition()
    food_location = gameState.getFood().asList()
    ghost_states = gameState.getGhostStates()
    ghost_positions = gameState.getGhostPositions()
    maze=gameState.getWalls()
    array_gScores, parent_nodes=dijkstra.calculate_gscores(maze,pacman_pos)

    #GHOST INFO
    ghost_movement_directions = [ghostState.getDirection() for ghostState in ghost_states]
    ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    ghost_distances_dangerous = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time<=1]
    ghost_distances_scared = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time>2]
    closest_ghost=min(ghost_distances_dangerous) if len(ghost_distances_dangerous)>0 else 0
    if len(ghost_distances_dangerous)>0:
      closest_ghost_location=ghost_positions[ghost_distances_dangerous.index(min(ghost_distances_dangerous))]
      ghost_x,ghost_y=closest_ghost_location
      path_to_ghost=dijkstra.calc_path_to_point(pacman_pos,(int(ghost_x),int(ghost_y)),parent_nodes)

    #CAPSULE INFO
    capsule_positions = gameState.getCapsules()
    capsule_distances=[array_gScores[capsule_pos_y][capsule_pos_x] for capsule_pos_x,capsule_pos_y in capsule_positions]
    
    #FOOD INFO
    food_distances = [array_gScores[food_pos_y][food_pos_x] for food_pos_x,food_pos_y in food_location]
    min_food_distance = min(food_distances) if len(food_distances)>0 else 0
    num_food_left=len(food_distances)
    closest_food_location=food_location[food_distances.index(min(food_distances))]
    path_to_food=dijkstra.calc_path_to_point(pacman_pos,closest_food_location,parent_nodes)


    good_moves=legal_moves
    good_moves.remove(Directions.STOP)

    if len(ghost_distances_dangerous)>0 and closest_ghost<=5:
          if path_to_ghost[0] in good_moves:
            good_moves.remove(path_to_ghost[0])
    else:
      if path_to_food[0] in good_moves:
          return path_to_food[0]
    

    if len(good_moves)>0:
      scores = [self.evaluateBoardState(gameState.generatePacmanSuccessor(action)) for action in good_moves]
      bestScore = max(scores)
      bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
      chosenIndex = random.choice(bestIndices) # Pick randomly among the best
      return good_moves[bestIndices[0]]
    else:
      return Directions.STOP
  def evaluateBoardState(self,gameState):
    dijkstra=Dijkstra()
    pacman_pos = gameState.getPacmanPosition()
    #list of tuples (x,y)
    food_positions = gameState.getFood().asList()
    #object ghost
    ghost_states = gameState.getGhostStates()
    #list of tuples [(6.0, 6.5), (7.5, 9.0)]
    ghost_positions = gameState.getGhostPositions()
    # list of two direction ["North","West"]
    maze=gameState.getWalls()
  
    array_gScores, parent_nodes=dijkstra.calculate_gscores(maze,pacman_pos)
    ghost_movement_directions = [ghostState.getDirection() for ghostState in ghost_states]
    # list of two scared times [0,0]
    ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    # list of tuples [(1, 1), (18, 9)]
    capsule_positions = gameState.getCapsules()
    capsule_distances=[array_gScores[capsule_pos_y][capsule_pos_x] for capsule_pos_x,capsule_pos_y in capsule_positions]
    #list of numbers with the distance [3, 4, 5]
    food_distances = [array_gScores[food_pos_y][food_pos_x] for food_pos_x,food_pos_y in food_positions]
    min_food_distance = min(food_distances) if len(food_distances)>0 else 0
    num_food_left=len(food_distances)
    ghost_distances_dangerous = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time<=1]
    ghost_distances_scared = [array_gScores[int(ghost_pos_y)][int(ghost_pos_x)] for (ghost_pos_x,ghost_pos_y),time in zip(ghost_positions,ghost_scared_times) if time>2]
    
    evaluation=gameState.getScore()
    if num_food_left>0:
      evaluation+=self.eval_future_food(pacman_pos,food_positions)
      evaluation+=self.eval_food(num_food_left)
      evaluation+=self.eval_food_distance(min_food_distance)
    elif num_food_left==0:
      evaluation+=100000000000
    if len(ghost_distances_dangerous)>0:
      if min(ghost_distances_dangerous)>0:
        evaluation+=self.eval_ghost_distance(ghost_distances_dangerous)
    if len(ghost_distances_scared)>0:
      evaluation+=self.eval_ghost_distance_scared(ghost_distances_scared)
    return evaluation 
class ce811NeuralBestAgent(Agent):
    
  def get_smallest_elements(self,input_list):
    if len(input_list) <= 4:
        return input_list
    smallest_elements = heapq.nsmallest(4, input_list)
    return smallest_elements
  def getAction(self, gameState):
    model_filename="./best_agent.h5"
    model = keras.models.load_model(model_filename)
    trw=[w.numpy() for w in model.trainable_weights]
    dijkstra=Dijkstra()
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
    
    input_vector=[pacman_pos[0],pacman_pos[1],ghost_positions[0][0],ghost_positions[0][1],ghost_distances_dangerous[0],
    ghost_positions[1][0],ghost_positions[1][1],ghost_distances_dangerous[1],ghost_distances_scared[0],ghost_distances_scared[1],
    closest_4th_food_location[0][0],closest_4th_food_location[0][1],
    capsule_positions[0][0],capsule_positions[0][1],capsule_distances[0],capsule_positions[1][0],capsule_positions[1][1],capsule_distances[1],gameState.getScore()]
    input_array = np.array(input_vector).reshape(1, 19)
    output_probabilities_directions = model.predict(input_array)
    output_probabilities_directions=output_probabilities_directions[0].tolist()
    map_probabilities = {0:Directions.EAST,1:Directions.NORTH,2:Directions.SOUTH,3:Directions.STOP,4:Directions.WEST}
    
    for i in range(5):
      best_move_probability=max(output_probabilities_directions)
      print(output_probabilities_directions)
      index_best_move=output_probabilities_directions.index(best_move_probability)
      #index_best_move=np.where(output_probabilities_directions == best_move_probability)
      move=map_probabilities[index_best_move]
      if move in legal_moves:
        print(move)
        return move
      else:
        output_probabilities_directions[index_best_move]=-10

    

    #return Directions.STOP
    
