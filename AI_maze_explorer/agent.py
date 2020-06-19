#-------------------------------------------------------------------------------
#TEAM NAME : SEEKERS

#MEMBERS:
    #ANKITA RATHOD(VY49170)
    #BETOUL ALSABAGH (SL48175)
    #SOPHIA KENNEDY(WL78890)
    #NITU CHOUDHARY (KJ96491)

#-------------------------------------------------------------------------------

import numpy as np
from utils import Directions
import util_functions as uf
from utils import MapTiles
import utils


class BaseAgent(object):
    def __init__(self, height, width, initial_strength, name='base_agent'):
        """
        Base class for a game agent

        Parameters
        ----------
        height: int
            Height of the game map
        width: int
            Width of the game map
        initial_strength: int
            Initial strength of the agent
        name: str
            Name of the agent
        """
        self.height = height
        self.width = width
        self.initial_strength = initial_strength
        self.name = name

    def step(self, location, strength, game_map, map_objects):
        """

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far


        Returns
        -------
        direction: Directions
            Which direction to move
        """
        pass


class RandomAgent(BaseAgent):
    """
    A random agent that moves in each direction randomly

    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='random_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of a random agent that at each step randomly moves in
        one of the four directions

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        return np.random.choice(list(Directions))


class HumanAgent(BaseAgent):
    """
    A human agent that that can be controlled by the user. At each time step
    the agent will prompt for an input from the user.

    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='human_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of an agent that at each step asks the user
        what to do

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        dir_dict = {'N': Directions.NORTH,
                    'S': Directions.SOUTH,
                    'W': Directions.WEST,
                    'E': Directions.EAST}

        dirchar = ''
        while not dirchar in ['N', 'S', 'W', 'E']:
            dirchar = input("Please enter a direction (N/S/E/W): ").upper()

        return dir_dict[dirchar]

class Node():
    """
        Node class for bookkeeping of children nodes for SeekerAgent
    """
    def __init__(self, position=None):
        self.position = position  #The x,y co-ordinates of the cell
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position

class SeekerAgent(BaseAgent):
    def __init__(self, height, width, initial_strength, name='seeker_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)
        
    visited_list=[]     #To store already visited locations
    
    def step(self, location, strength, game_map, map_objects):
        
        SeekerAgent.visited_list.append(location)

        direction = {(-1, 0): "N", (1, 0): "S", (0, -1): "W", (0, 1): "E"}
        dir_dict = {'N': Directions.NORTH,
                    'S': Directions.SOUTH,
                    'W': Directions.WEST,
                    'E': Directions.EAST}
        
        children = []
        children_same_h =[]
        child_max_index= -1
        p = []
        direc = ''
        max1 = 0
        (x, y) = location
        d = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        #Function to calculate the path cost
        def cal_cost(position, game_map):
            if (game_map[position[0]][position[1]] == MapTiles.PATH):
                    return 1 
            elif (game_map[position[0]][position[1]] == MapTiles.SAND):
                    return 3
            elif (game_map[position[0]][position[1]] == MapTiles.MOUNTAIN):
                    return 10
            elif (game_map[position[0]][position[1]] == MapTiles.WALL):
                    return -1
                
        #Function to calculate heuristic
        def cal_h(position, game_map):
            s1=0    #To store the delta value for the map_objects
            pos_list=[] #To store the list of positions
            
            #To calculate path cost
            h = cal_cost(position, game_map)
            
            #If h=-1 then the cell is a wall and -1 is returned as the heuristic value for that cell
            if h==-1:
                return -1
            
            #Nearby Map_objects are checked for the child node(i.e given position) and the position itself is checked for any map_objects
            #And the delta values are calculated
            if(direction[tuple(np.subtract(position, location))] == "N" or direction[tuple(np.subtract(position, location))] == "S"):
                
                pos_list.append(position)
                position1 = tuple(np.add(position,(0,-1)))
                pos_list.append(position1)
                position2 = tuple(np.add(position,(0, 1)))
                pos_list.append(position2)
                
                for k in pos_list:
                    #To validate if position is within range
                    if (k[0] > (self.height - 1) or k[0] < 0 or k[1] < 0 or k[1] > (self.width - 1)):
                        continue
        
                    if k in map_objects:
                        if k!=position:
                            h1 = h+cal_cost(k, game_map)
                        else:
                            h1 = h
                            
                        if isinstance(map_objects[k], utils.PowerUp):
                            #Will choose to go in that direction only if it has the strength to reach there
                            if ((strength-h1)>0):
                                s1 = map_objects[k].delta
                            else: 
                                s1 = -(h1)+h

                        elif isinstance(map_objects[k], utils.Boss):
                            #Calculation of win chance to decide to fight against the Boss
                            wc = (strength-h1)/((strength-h1) + map_objects[k].strength)
                            #Comparison of win chance with a lower threshold value of 0.3 so that the agent chooses to fight everytime when win chance is greater than or equal to the threshold value.
                            if ((strength-h1) > 0 and wc >= 0.3):
                                s1 = map_objects[k].strength
                            else:
                                s1 = map_objects[k].delta-h1+h
                                
                        elif isinstance(map_objects[k], utils.StaticMonster):
                            #Calculation of win chance to decide to fight the Static Monster
                            wc = (strength-h1)/((strength-h1) + map_objects[k].strength)
                            #Comparison of win chance with a lower threshol value of 0.3 so that the agent chooses to fight everytime when win chance is greater than or equal to the threshold value.
                            if ((strength-h1) > 0 and wc >= 0.3):
                                s1 = map_objects[k].strength
                            else:
                                s1 = map_objects[k].delta-h1+h
                                
                        #To fight other agent
                        elif isinstance(map_objects[k], BaseAgent):
                            #Decision to fight depending on the strength of both the agents.
                            #It chooses to fight only if its strength is greater than the other agent's strength.
                            #(Strength-h1) need to be greater than zero so that the agent has some energy to fight and doesn't lose all its energy just in reaching there.
                            if ((strength-h1) > 0 and strength > map_objects[k].strength):
                                s1 = map_objects[k].strength-h1+h
                            else:
                                s1 = -(map_objects[k].strength)-h1+h
                                
                pos_list.clear()

                #Penalty points to get the agent to move towards the unexplored region
                if(position[0]>=self.height/2):
                    h = h+0
                else:
                    h = h+10
    
            elif(direction[tuple(np.subtract( position, location))] == "E" or direction[tuple(np.subtract( position, location))] == "W"):
                
                pos_list.append(position)
                position1 = tuple(np.add(position,(-1,0)))
                pos_list.append(position1)
                position2 = tuple(np.add(position,(1,0)))
                pos_list.append(position2)

                for k in pos_list:
                    #To validate if position is within range
                    if (k[0] > (self.height - 1) or k[0] < 0 or k[1] < 0 or k[1] > (self.width - 1)):
                        continue
                    if k in map_objects:
                        if k!=position:
                            h1 = h+cal_cost(k, game_map)
                        else:
                            h1 = h
                            
                        if isinstance(map_objects[k], utils.PowerUp):
                            #Will choose to go in that direction only if it has the strength to reach there
                            if ((strength-h1) > 0):
                                s1 = map_objects[k].delta
                            else:
                                s1 = -(h1)+h

                        elif isinstance(map_objects[k], utils.Boss):
                            wc = (strength-h1)/((strength-h1) + map_objects[k].strength)
                            #Comparison of win chance with a lower threshold value of 0.3 so that the agent chooses to fight everytime when win chance is greater than or equal to the threshold value.
                            if ((strength-h1) > 0 and wc >= 0.3):
                                s1 = map_objects[k].strength
                            else:
                                s1 = map_objects[k].delta-h1+h
                                
                        elif isinstance(map_objects[k], utils.StaticMonster):
                            wc = (strength-h1)/((strength-h1) + map_objects[k].strength)
                            #Comparison of win chance with a lower threshold value of 0.3 so that the agent chooses to fight everytime when win chance is greater than or equal to the threshold value.
                            if ((strength-h1) > 0 and wc >= 0.3):
                                s1 = map_objects[k].strength
                            else:
                                s1 = map_objects[k].delta-h1+h
                        
                        elif isinstance(map_objects[k], BaseAgent):
                            #To fight other agent in the map
                            if ((strength-h1) > 0 and strength > map_objects[k].strength):
                                s1 = map_objects[k].strength-h1+h
                            else:
                                s1 = -(map_objects[k].strength)-h1+h

                pos_list.clear()
                
                #Penalty points to get the agent to move towards the unexplored region
                if(position[1]<=self.width/2):
                    h =h+0
                else:
                    h =h+10

           #Returns heuristic value considering the delta for the map_objects,cell cost, penalties and the strength of the agent
            return strength-h+s1     


        #Generating Children 
        for new_pos in d:
            node_position = tuple(np.add(location, new_pos))
            #To validate if position is within range
            if (node_position[0] > (self.height - 1) or node_position[0] < 0 or node_position[1] < 0 or node_position[
                1] > (self.width - 1)):
                continue

            #Create a new node
            new_node = Node(node_position)
            new_node.h = cal_h(node_position, game_map)

            #Wall cell is not added to the children list.
            if new_node.h != -1:
                children.append(new_node)
                
        p.clear()
        
        #To remove the already visited node from children list.
        for k,c in enumerate(children):
            for v in SeekerAgent.visited_list:
                if(c.position==v):
                    #Store the indices of the already visited nodes
                    p.append(k)
                    break
                    

        if len(p)!= 0 and len(children)!=0:
            for j in range(0, len(p)):
                # Loop to remove the nodes from the children list which is already present in the visited_list.
                children.pop(p[j] - j)
              
        #To find maximum heuristic value
        #Basically the new strength of the agent after all the penalties and the gain of energy after winning fights is considered as the heuristic
        #Higher the heuristic after considering the delta values of map_objects, cell cost, penalties and the strength of the agent, higher is the chance of taking that action(i.e choosing the node)
        #Node with highest heuristic value is chosen
        for i,c in enumerate(children):
            if c.h >= max1 and c.h!=-1:
                max1 = c.h
                child_max_index = i
                
        #If children list is empty after removing nodes leading to the wall cell and the nodes already visited.
        if(len(children)==0):
            return np.random.choice(list(Directions))
        else:
            child = children.pop(child_max_index)

        #The children nodes with same heuristic value(i.e the max value) are appended in children_same_h list.
        for c in children:
            if not c==child:
                if c.h == child.h:
                    children_same_h.append(c)
                    
        #If there are more possibilities with same heuristic value choose one node randomly.
        if(len(children_same_h)!=0):
            child = np.random.choice(children_same_h)

        #To find the direction
        direc = direction[tuple(np.subtract( child.position, location))]
        
        #Return the direction for one step
        return dir_dict[direc]
