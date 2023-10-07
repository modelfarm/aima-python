import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from agents import *

########################################
# AGENT CLASSES
########################################
# Agent Class - Fire brigade Agent - Model
def ModelBasedReflexFireman():
    location = [0,0]
    isVisited = False
    model = {}
    for x in range(5):
        for y in range(5):
            model[x,y] = None
     
    def program(percept):
        location, things = percept
        choice=0
        
        #Model Condition, End actions
        for m in model.items():
            if m!=None:
                break
            else:
                return 'NoOp'
            
        #Agent Actions
        for t in things:
            if isinstance(t, Fire):
                print('there is a fire')
                return 'Extinguish'
                model[tuple(location)] = t  # Update the model here
            elif isinstance(t, Water):
                print('there is a Water')
                return 'TakeWater'       
                model[tuple(location)] = t  # Update the model here
            else:
                choice = random.choice(('L','R','D','U'))
            if  choice !=0:
                if choice == 'L':
                    if location[0]==0:
                        location[0]=1
                elif choice == 'R':
                    pass
                elif choice == 'D':
                    pass
                elif choice == 'U':
                    pass
            return 'Move'+choice          
    return Agent(program)

def ModelBasedFiremanAgent():

    # model = {loc_A: None, loc_B: None}
    model = {(x, y): None for x in range(10) for y in range(20)} 

    def program(percept):
        """Same as ReflexVacuumAgent, except if everything is clean, do NoOp."""
        location, things = percept
        model[tuple(location)] = things  # Update the model here
        
        for eachLoc in model.items():
            if eachLoc !='Visited' or eachLoc !='Obstacle':
                if eachLoc == 'NoOp':
                    return 'NoOp'
                elif things == 'Fire':
                    return 'Suck'
                elif location == loc_A:
                    return 'Right'
                elif location == loc_B:
                    return 'Left' 
            else:
                return 'NoOp'
            
            model[tuple(location)] = 'Visited'  
            
    return Agent(program)


def ReflexFireman():
    location = [0,0]
    isHoldingWater = True
    map = {}
    for x in range(5):
        for y in range(5):
            map[x,y] = None
     
    def program(percept):
        location, things = percept
        choice=0
        for t in things:
            if isinstance(t, Fire):
                print('there is a fire')
                return 'Extinguish'
                map[tuple(location)] = t  # Update the model here
            elif isinstance(t, Water):
                print('there is a Water')
                return 'TakeWater'       
                map[tuple(location)] = t  # Update the model here
            else:
                Print('Move')
                choice = random.choice(('L','R','D','U'))
        if  choice !=0:
            if choice == 'L':
                pass
            elif choice == 'R':
                pass
            elif choice == 'D':
                pass
            elif choice == 'U':
                pass          
    return Agent(program)
########################################
# THING CLASSES
########################################
# Thing Class - Water
class Water(Thing):
    Name='Water'
    pass

# Thing Class - Fire
class Fire(Thing):
    pass


########################################
# ENVIRONMENT CLASS
########################################
# Forrest Class
class Forrest(XYEnvironment):
    # def percept(self, agent):
    #     '''return a list of things that are in our agent's location'''
    #     things = self.list_things_at(agent.location)
    #     return things
    
    def _init__():
        map = {}
        for x in range(5):
            for y in range(5):
                map[x,y] = None
    
    def percept(self, agent):
        """By default, agent perceives things within a default radius."""
        return agent.location, self.list_things_at(agent.location)
    
    # def thing_classes(self):
    #     return [Fire, Water, ModelFireman]

    def execute_action(self, agent, action):
        #print('here there is a fire')
        # try to optimize grabbing by using only the method can_grab from Agent Class
        #agent.program('Extinguish')
        # if action == 'Extenguish':
        print('here there is not a fire')
            

# def RandomFiremanProgram(actions):
#     return lambda percept: random.choice(actions)

# firemanActions = ['Extenguish','Move']
# percept = ['Fire', 'Tree', 'Axes']              

# newFiremanProgram = RandomFiremanProgram(firemanActions)

fireman = ModelBasedFiremanAgent()
fire = Fire()
water = Water()

forrest = Forrest()
forrest.add_thing(fireman,[0,0])
forrest.add_thing(water,(0,0))

forrest.run()
        
