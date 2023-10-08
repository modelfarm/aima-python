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
class ModelFireman(Agent):
    location = [0,0]           
    Name = 'ModelFireman'
    Agent.isHoldingWater = False
    
    def takeWater(self, thing):
        '''returns True upon success or False otherwise'''
        if isinstance(thing, Water):
            return True
        return False
    
    def estinguishFire(self, thing):
        '''returns True upon success or False otherwise'''
        if isinstance(thing, Fire):
            return True
        return False

########################################
# AGENT PROGRAM
########################################
def programAgent(percept):
    location, things = percept
    for t in things:
        #if model[tuple(location)] not in['Visited']:
        if isinstance(t, Fire):
            model[tuple(location)] = 'Fire'
            print('There is Fire')
            return 'Estinguish Fire'
        elif isinstance(t, Water):
            model[tuple(location)] = 'Water'
            print('There is Water')
            return 'Take Water'     
        model[tuple(location)] = t  # Update the model here

    if not isinstance(model[tuple(location)],(Water,Fire)):
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
    return 'Move' + choice

    #return programAgent#, model

########################################
# THING CLASSES
########################################
# Thing Class - Water
class Water(Thing):
    Name='Water'
    pass

# Thing Class - Fire
class Fire(Thing):
    Name='Fire'
    pass


########################################
# ENVIRONMENT CLASS
########################################
# Forrest Class
class Forrest2D(GraphicEnvironment):
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
        if action == 'MoveR':
            if agent.location[0]>=0 and agent.location[0]< 5:
                agent.location[0]+=1
                agent.performance -= 1
                #print('R here we go')       
        elif action == 'MoveL':
            if agent.location[0]>0 and agent.location[0]<=5:
                agent.location[0]-=1
                agent.performance -= 1
                #print('L here we go')         
        elif action == 'MoveU':
            if agent.location[1]>=0 and agent.location[1]<5:
                agent.location[1]+=1
                agent.performance -= 1
                #print('U here we go')               
        elif action == 'MoveD':
            if agent.location[1]>0 and agent.location[1]<=5:
                agent.location[1]-=1
                agent.performance -= 1             
                #print('D here we go') 
        elif action == 'Take Water':
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.takeWater(items[0]): 
                    agent.performance += 100
                    self.delete_thing(items[0])
                    agent.isHoldingWater = True
                    print('Take Water')
        elif action == 'Estinguish Fire':
            items = self.list_things_at(agent.location, tclass=Fire)
            if len(items) != 0:                  
                if agent.estinguishFire(items[0]) and agent.isHoldingWater:
                    agent.performance += 100
                    self.delete_thing(items[0])
                    agent.isHoldingWater = False
                    print('Estinguish Fire')
                else:
                    agent.performance -= 100
                    print('Burning, no water')
                    
        if model[tuple(agent.location)] == 'Visited':
            agent.performance -= 10
            
        print(model[tuple(agent.location)])
        print(agent.location)
        print(f'Fireman performance: {agent.performance} and is holding water: {agent.isHoldingWater}')

    def is_done(self):
        
        return False
    
collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence   
 
   
model = {(x, y): None for x in range(6) for y in range(6)}
forrest = Forrest2D(6,6, color={'ModelFireman': (230, 115, 40), 'Water': (0, 200, 200), 'Fire': (200,0,0)})

fireman = ModelFireman(programAgent)
fire = Fire()
water = Water()

forrest.add_thing(fireman, [3,3])
forrest.add_thing(water, [3,4])
forrest.add_thing(fire, [3,5])   

forrest.run(30,delay=0.1)

print(f'Fireman perfrmance: {fireman.performance} and is holding water: {fireman.isHoldingWater}')

print(model)
