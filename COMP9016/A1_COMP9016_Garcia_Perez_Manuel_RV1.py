
#1.1 BUILDING YOUR WORLD
import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from agents import Agent,collections,Thing,GraphicEnvironment,Wall,Obstacle
from ipythonblocks import BlockGrid
import random
collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence


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

#Agents

#Aventure Explorer Random Agent
def RandomAvExplorerAgent(Agent):
    """Randomly choose one of the actions from the vacuum environment.
    """
    idleTurn=0
    def program(actions):
        return lambda percept: random.choice('Left','Right','Up','Down')
        # idleTurn
    return Agent(program)

#Aventure Explorer Reflex Agent
def ReflexAvExplorerAgent():

    idleTurn=0
    def program(percept):
        location, things = percept
        choice=0
      
        #Agent Actions
        # for t in things:
        #     if isinstance(t, Rope):
        #         print('Rope Founded')
        #         model[tuple(location)] = 'Visited'
        #         return 'TakeRope'
                
        #     elif isinstance(t, SlowMotion):
        #         print('Wait in this possition')
        #         return 'Wait'       
        #     else:
        #         choice = random.choice(('L','R','D','U'))
        # if  choice !=0:
        #     if choice == 'L':  

        #     elif choice == 'R':
        #         pass
        #     elif choice == 'D':
        #         pass
        #     elif choice == 'U':
        #         pass
        # return 'Move'+choice          
    return Agent(program)

#Aventure Explorer Model Based Reflex Agent
class ModelBasedReflexAvExplorerAgent(Agent):
    #Features
    Possition = [0,0]      
    idleTurn=0
    
    #Movement Methods
    def MoveRight(Self):
        Self.location[0]+=1
    
    def MoveLeft(Self):
        Self.location[0]-=1

    def MoveDown(Self):
        Self.location[1]+=1
    
    def MoveUp(Self):
        Self.location[1]-=1
    


def ReflexAgentprogram(percept):

    model = {(x, y): None for x in range(10) for y in range(20)} 
    location, ThingsDic = percept
    choice=0
    MoveOptions=[]

    #Model Condition, End actions
    if not any(m != 'Visited' and m != 'Obstacle' for m in model.values()): return 'NoOp'

    #Delete
    # for m in model.items():
    #     if m!='Visited' or m!='Obstacle':
    #         break
    #     else:
    #         return 'NoOp'  
                  
    #Agent Actions
    model[tuple(location)] = 'Visited'
    for t in ThingsDic[tuple(location)]:
        # elif isinstance(t, SlowMotion):
        #     if Agent.idleTurn==0:
        #         print('there is ',t.__class__.__name__)
        #         if isinstance(t,Water):
        #             Agent.idleTurn=2
        #         else:
        #             Agent.idleTurn=5            
        #     return 'Wait'       
        if any(t): 
            if isinstance(t[0], Rope):
                print('There is a Rope')
                return 'TakeRope'
    for t in ThingsDic:
        if any(ThingsDic[t]):
            if not isinstance(ThingsDic[t][0],Obstacle): MoveOptions.append(t)
        else:
            MoveOptions.append(t)
            

    if any(MoveOptions): choice = random.choice(MoveOptions) 
    if  choice !=0:
        if choice == 'L':
            return 'Left'
        elif choice == 'R':
            return 'Right'
        elif choice == 'D':
            return 'Down'
        elif choice == 'U':
            return 'Up'        

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

MyField=MyFieldEnv(10,20,color=color1)
FillWorld(MyField)
MBRExplorer=ModelBasedReflexAvExplorerAgent(ReflexAgentprogram)
MyField.add_thing(MBRExplorer,[2,13])
MyField.add_thing(Wall(),[0,0])
MyField.run(80,delay=0.1)
