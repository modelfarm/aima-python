import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from agents import *
import random

########################################
# AGENT CLASSES
########################################
# Agent Class - Fire brigade Agent - Model
def ModelFireman():
    location = [0,0]
    width = 6
    height = 6
    model = {(x, y): None for x in range(width) for y in range(height)}     

    def program(percept):
        location, things = percept
        print(model[tuple(location)])
        # print(things)
        
        for t in things:
            if model[tuple(location)] not in['Visited']:
                if isinstance(t, Fire):
                    print('there is a fire')
                elif isinstance(t, Water):
                    model[tuple(location)] = 'Water'
                    print('there is a Water')
                    return 'Extinguish'
                model[tuple(location)] = t  # Update the model here
        
        if not isinstance(things,(Water,Fire)):
            model[tuple(location)] = 'Visited'
        
                        
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
        return 'Move'+ choice
         
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
    
    def __init__(self, width=5, height=5):
        super().__init__(width, height)
        model = {}
        for x in range(width):
            for y in range(height):
                model[x,y] = None
            
            
    def percept(self, agent):
        listThings = []
        for things in self.list_things_at(agent.location):
            if things != agent:
                listThings.append(things)   
        """By default, agent perceives things within a default radius."""
        return agent.location, listThings
    
    def thing_classes(self):
        return [Fire, Water, ModelFireman]

    def execute_action(self, agent, action):
        #print('here there is a fire')
        # try to optimize grabbing by using only the method can_grab from Agent Class
        #agent.program('Extinguish')
        if action == 'MoveR':
            if agent.location[0]>=0 and agent.location[0]< 5:
                agent.location[0]+=1
                agent.performance -= 1
                print('R here we go')       
        elif action == 'MoveL':
            if agent.location[0]>0 and agent.location[0]<=5:
                agent.location[0]-=1
                agent.performance -= 1
                print('L here we go')         
        elif action == 'MoveU':
            if agent.location[1]>=0 and agent.location[1]<5:
                agent.location[1]+=1
                agent.performance -= 1
                print('U here we go')               
        elif action == 'MoveD':
            if agent.location[1]>0 and agent.location[1]<=5:
                agent.location[1]-=1
                agent.performance -= 1             
                print('D here we go')   
        elif action == 'Extinguish':
            #agent.location=(0,0)
            self.delete_thing(agent)
            if agent.location[0]>=0 and agent.location[0]< 5:
                agent.location[0]+=1
                agent.performance += 100
            else:
                agent.location[0]-=1
                agent.performance += 100        
            print('Extinguish here we go')
        
        print(agent.location)
            

    def is_done(self):
        
        return False



# def RandomFiremanProgram(actions):
#     return lambda percept: random.choice(actions)

# firemanActions = ['Extenguish','Move']
# percept = ['Fire', 'Tree', 'Axes']              

# newFiremanProgram = RandomFiremanProgram(firemanActions)

fireman = ModelFireman()
fire = Fire()
water = Water()

forrest = Forrest()
forrest.add_thing(fireman,[0,0])
forrest.add_thing(water,(2,1))

forrest.run()

print(f'Fireman performance: {fireman.performance}')
