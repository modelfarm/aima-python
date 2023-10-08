# working

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
class Fireman(Agent):
    location = [0,0]           
    Name = 'Fireman'
    isHoldingWater = False
    
    def can_grab(self, thing):
        """Fireman can only grab water"""
        return thing.__class__ == Water
    
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

def randomMotions():
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
    #print('Move' + choice)
    return ('Move' + choice)


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

class Obstacle(Thing):
    """Something that can cause a bump, preventing an agent from
    moving into the same square it's in."""
    pass

class Wall(Obstacle):
    pass

########################################
# ENVIRONMENT CLASS
########################################
# Forrest Class
#class Forrest2D(XYEnvironment):
class Forrest2D(GraphicEnvironment):
    
    def percept(self, agent):
        listThings = []
        for things in self.list_things_at(agent.location):
            if things != agent:
                listThings.append(things)   
        """By default, agent perceives things within a default radius."""
        return agent.location, listThings
     
    
    def thing_classes(self):
        return [Fire, Water, Fireman, Wall]
    
    
    def execute_action(self, agent, action):

        if action == 'Take Water':
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
                if agent.estinguishFire(items[0]):
                    agent.performance += 100 if Water in agent.holding else -100
                    self.delete_thing(items[0])
                    agent.isHoldingWater = False
                    print('Estinguish Fire')
                else:
                    agent.performance -= 100
                    print('Burning, no water')
                    
        if model[tuple(agent.location)] == 'Visited':
            #self.colors = (50,50,50)
            agent.performance -= 10
        
        #print(self.colors[self.default_location])
                  
        motions = randomMotions()       
        if motions == 'MoveR':
            if agent.location[0]>=0 and agent.location[0]< 5:
                agent.location[0]+=1
                agent.performance -= 1
                print('Move Right')       
        elif motions == 'MoveL':
            if agent.location[0]>0 and agent.location[0]<=5:
                agent.location[0]-=1
                agent.performance -= 1
                print('Move Left')         
        elif motions == 'MoveU':
            if agent.location[1]>=0 and agent.location[1]<5:
                agent.location[1]+=1
                agent.performance -= 1
                print('Move UP')               
        elif motions == 'MoveD':
            if agent.location[1]>0 and agent.location[1]<=5:
                agent.location[1]-=1
                agent.performance -= 1        
                print('Move Down') 

            
        print(model[tuple(agent.location)])
        print(agent.location)
        print(f'Fireman performance: {agent.performance} and is holding water: {agent.isHoldingWater}')

    def is_done(self):
        
        return False
    
collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence   
 
   
model = {(x, y): None for x in range(6) for y in range(6)}
forrest = Forrest2D(6,6, color={'Fireman': (230, 115, 40), 'Water': (0, 200, 200), 'Fire': (200,0,0), 'Visited': (50,50,50), 'Walls': (50,50,50)})

fireman = Fireman(programAgent)
fire = Fire()
water = Water()




forrest.add_thing(fireman, [2,1])
forrest.add_thing(water, [3,4])
#forrest.add_thing(Water(), forrest.random_location_inbounds(exclude=(3, 4)))
forrest.add_thing(fire, [1,5])
#forrest.add_thing(Fire(), forrest.random_location_inbounds(exclude=(1, 5)))

forrest.run(100,delay=0.05)

print(f'Fireman performance: {fireman.performance} and is holding water: {fireman.isHoldingWater}')

print(model)
