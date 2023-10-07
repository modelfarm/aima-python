
#1.1 BUILDING YOUR WORLD
import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from agents import *


class MyFieldEnv(XYEnvironment):
    """The environment of [Ex. 2.12]. Agent perceives dirty or clean,
    and bump (into obstacle) or not; 2D discrete world of unknown size;
    performance measure is 100 for each dirt cleaned, and -1 for
    each turn taken."""
    def __init__(self,agent_program ,width=10, height=20):
        super().__init__(width, height)
        self.init_world(agent_program)

    def init_world(self, program):

        "WALLS AROUND"
        self.add_walls()

        listPosition=([3,12],[4,12],[5,12],[6,12],[7,12],[8,12],[5,13],[3,14],
             [1,16],[2,16],[3,16],[4,16],[5,16],[6,16],[5,17],[5,18],
             [3,18],[3,19])
        for l in listPosition:
            self.add_thing(Wall(), l)

        "Stones"
        for i in range(10):
            while True:
                w_x, w_y = self.random_location_inbounds(exclude=(1, 1))
                if  self.list_things_at(w_x, w_y)==None:
                    self.add_thing(Stone, (w_x, w_y))
                    break

        "Sand"
        for i in range(5):
            while True:
                w_x, w_y = self.random_location_inbounds(exclude=(1, 1))
                if  self.list_things_at(w_x, w_y)==None:
                    self.add_thing(Sand, (w_x, w_y))
                    break
        "water"
        listPos = ([2, 14], [3, 14], [1, 2],[2, 2])
        for l in listPos:
            self.add_thing(Water, l)

        #Convert all in Random
        "Hole"
        while True:
            w_x, w_y = self.random_location_inbounds(exclude=(1, 1))
            if  self.list_things_at(w_x, w_y)==None:
                self.add_thing(Hole, (w_x, w_y))
            break

        "Rope"
        while True:
            w_x, w_y = self.random_location_inbounds(exclude=(1, 1))
            if  self.list_things_at(w_x, w_y)==None:
                self.add_thing(Hole, (w_x, w_y))
            break

        "Treasure"       
        self.add_thing(Treasure, (1,19))

    def percept(self, agent):
        """location and things except None"""
        ThingList=self.list_things_at(agent.location)
        ThingList[agent.__class__] = None
        return agent.location, ThingList

    def execute_action(self, agent, action):
        """Modify the state of the environment based on the agent's actions.
        Performance score taken directly out of the book."""
      
        agent.bump = False
        #Movement Done
        if action == 'TurnRight':
            agent.direction += Direction.R
            agent.performance -= 1
        elif action == 'TurnLeft':
            agent.direction += Direction.L
            agent.performance -= 1
        elif action == 'MoveForward':
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
            agent.performance -= 1
        
        #Other Actions
        elif action == 'Wait':
            agent.idleturn-=1
            agent.performance -= 5
            print("Waiting Tiime")
        elif action=='TakeRope':
            things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing)]
            if things:    
                agent.holding.append(things[0])
                print("Take  ", things[0].__class__.__name__)
                self.delete_thing(things[0])
        elif action=='TreasureFound':
            agent.performance += 100
            print('Treasure Founded by ',agent.__class__.__name__)

#Classes
#Things

class SlowMotion(Thing):
    '''Agent can't move the next x movements'''
    pass

class Stone(Obstacle):
    pass

class Sand(SlowMotion):
    time=2
    pass

class Water(SlowMotion):
    times=5
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
def ModelBasedReflexAvExplorerAgent():
    
    idleTurn=0
    model = {(x, y): None for x in range(10) for y in range(20)} 

    def program(percept):
        location, things = percept
        choice=0
        #Model Condition, End actions
        for m in model.items():
            if m!='Visited' or m!='Obstacle':
                break
            else:
                return 'NoOp'            
        #Agent Actions
        model[tuple(location)] = 'Visited'
        for t in things:
            if isinstance(t, Obstacle):
                print('There is a Obstacle')
                model[tuple(location)] = 'Obstacle'
            elif isinstance(t, SlowMotion):
                print('there is ',t.__class__.__name__)
                if isinstance(t,Water):
                    idleTurn=2
                else:
                    idleTurn=5
                return 'Wait'
            #i am here
            elif isinstance(t,Rope):
                print('there is a Rope')
                idleTurn=5
                return 'Wait'
            
            elif isinstance(t, Bump):
                choice = random.choice(('L','R'))
            else:
                choice = random.choice(('L','R','MF'))
        if  choice !=0:
            if choice == 'L':
                return 'Left'
            elif choice == 'R':
                return 'Right'
            else:
                return 'MoveForward'
        return 'Move'+choice          
    return Agent(program)


MBRExplorer=ModelBasedReflexAvExplorerAgent()

#
MyField=MyFieldEnv()
MyField.add_thing(MBRExplorer)
MyField.step(15)
