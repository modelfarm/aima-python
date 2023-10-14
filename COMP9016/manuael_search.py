import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from agents import *
from search import *
#from agents import Agent,collections,Thing,GraphicEnvironment,Wall,Obstacle
from ipythonblocks import BlockGrid
import random
collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence

#from search import Problem, Node, astar_search, UndirectedGraph, DicMapCreation
import numpy as np
from scipy.spatial import distance


class MyFieldEnv(GraphicEnvironment):
    """2D World"""
    def percept(self, agent):

        """location and things except None and Agent"""
        #Check thigs in current location and the squares near
        x, y = agent.location
        ThingDict = {}
        ThingDict[(x,y)]=self.list_things_at(x,y)
        ThingDict['L']=self.list_things_at((x - 1, y))
        ThingDict['R']=self.list_things_at((x + 1, y))
        ThingDict['U']=self.list_things_at((x, y - 1))
        ThingDict['D']=self.list_things_at((x, y + 1))
        ThingDict.remove(Agent) if Agent in ThingDict else None
        return agent.location, ThingDict

    def execute_action(self, agent, action):
        """Modify the state of the environment based on the agent's actions.
        Performance score taken directly out of the book."""

        #Movement
        if action == 'Right':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveRight()
        elif action == 'Left':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveLeft()
        elif action == 'Down':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveDown()
        elif action == 'Up':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveUp()
        elif action=='TakeRope':
            things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing)]
            if things:    
                agent.holding.append(things[0])
                print("Take  ", things[0].__class__.__name__)
                self.delete_thing(things[0])
        #Other Actions
        # elif action == 'Wait':
        #     agent.idleTurn-=1
        #     agent.performance -= 5
        #     print("Waiting Tiime")
        # elif action=='TreasureFound':
        #     agent.performance += 100
        #     print('Treasure Founded by ',agent.__class__.__name__)

#Classes
#Things
class SlowMotion(Thing):
    pass

class Stone(Obstacle):
    pass

class Sand(SlowMotion):
    pass

class Water(SlowMotion):
    pass

class Treasure(Thing):
    pass

class Hole(Thing):
    pass

class Rope(Thing):
    pass

###Search problem
def DicMapCreation(width,height,BlockPos):
    rows = height-1
    columns = width-1

    # Lista de posiciones bloqueadas
    GameMap = {}
    def is_inside_grid(x, y):
        return 0 < x <= columns and 0 < y <= rows

    # Generar las posibilidades de movimiento y sus costos, excluyendo las posiciones bloqueadas
    for x in range(1, columns + 1):
        for y in range(1, rows + 1):
            CurrPos = (x, y)
            
            # Verificar si la posición actual está bloqueada
            if CurrPos not in BlockPos:
                transitions = {}
                
                # Movimiento hacia arriba
                if is_inside_grid(x - 1,y) and (x - 1,y) not in BlockPos:
                    transitions[str((x - 1,y))] = 1
                # Movimiento hacia abajo
                if is_inside_grid(x + 1,y) and (x + 1,y) not in BlockPos:
                    
                    transitions[str((x + 1,y))] = 1
                # Movimiento hacia la izquierda
                if is_inside_grid(x,y - 1) and (x,y - 1) not in BlockPos:
                    transitions[str((x,y - 1))] = 1
                # Movimiento hacia la derecha
                if is_inside_grid(x,y + 1) and (x,y + 1) not in BlockPos:
                    transitions[str((x,y + 1))] = 1
                
                if transitions:
                    GameMap[str(CurrPos)] = transitions

    # Prnint dictionary
    for location, transitions in GameMap.items():
        print(f'From {location}: {transitions}')
    return GameMap 


def FillWorld(Env):

    "WALLS AROUND"
    Env.add_walls()

    listPosition=([3,11],[4,11],[5,11],[6,11],[7,11],[8,11],[5,12],[3,1],
            [1,15],[2,15],[3,15],[4,15],[5,15],[6,15],[5,16],[5,17],
            [3,17],[3,18])
    for l in listPosition:
        Env.add_thing(Wall(), l)

    "Stones"
    for i in range(5):
        while True:
            w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
            if  not any(Env.list_things_at(w_x, w_y)):
                Env.add_thing(Stone(), (w_x, w_y),True)
                break

    "Sand"
    for i in range(5):
        while True:
            w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
            if  not any(Env.list_things_at(w_x, w_y)):
                Env.add_thing(Sand(), (w_x, w_y),True)
                break
    "water"
    listPos = ([2, 13], [3, 13], [1, 2],[2, 2])
    for l in listPos:
        Env.add_thing(Water(), l)

    #Convert all in Random
    "Hole"
    while True:
        w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
        if  not any(Env.list_things_at(w_x, w_y)):
            Env.add_thing(Hole(), (w_x, w_y),True)
        break

    "Rope"
    while True:
        w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
        if  not any(Env.list_things_at(w_x, w_y)):
            Env.add_thing(Rope(), (w_x, w_y),True)
        break

    "Treasure"       
    Env.add_thing(Treasure(), (1,18))

#execution
color1 = {"Stone": (128, 128, 128),
        "Sand": (255,253,85),
        "Water": (50, 130, 246),
        "Rope": (120, 67, 21),
        "Treasure": (255, 215, 0),
        "ModelBasedReflexAvExplorerAgent": (117, 250, 97),
        "Wall": (44, 53, 57),
        "Hole": (255, 255, 255),     
        }
#

# MyField=MyFieldEnv(10,20,color=color1)
# FillWorld(MyField)
# MBRExplorer=ModelBasedReflexAvExplorerAgent(ReflexAgentprogram)
# MyField.add_thing(MBRExplorer,[2,13])
# MyField.add_thing(Wall(),[0,0])
# MyField.run(80,delay=0.1)



MyField=MyFieldEnv(10,20,color=color1)
PosUsedMyMap=FillWorld(MyField)
DicMyField=UndirectedGraph(DicMapCreation(MyField.width,MyField.height,PosUsedMyMap))

AgentToTreasure = GraphProblem('(1, 1)', '(1, 18)', DicMyField)

def compare_graph_searchers(uninformed_searchers):
    """Prints a table of search results."""
    outputString = 'Actions/Goal Tests/States/Goal\n'
    print(outputString)
    compare_searchers(problems=[AgentToTreasure], header=['Searcher', 'Game_Map((1,1)), (1,18)))'], searchers=uninformed_searchers)

searchers=[breadth_first_graph_search]
        #   breadth_first_tree_search
        #    depth_first_tree_search,
        #    breadth_first_graph_search,
        #    depth_first_graph_search,
        #    iterative_deepening_search,
        #    depth_limited_search

compare_graph_searchers(searchers)

