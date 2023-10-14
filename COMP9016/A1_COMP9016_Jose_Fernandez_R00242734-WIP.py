import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from agents import *
import random

collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence 

random.seed(12345)

########################################
# Agent Class - Fire brigade - Model Agent
########################################
class ModelFiremanAgent(Agent):
    location = [1,1]           
    Name = 'ModelFiremanAgent'
      
  
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
    
    #TODO: model
    
    

########################################
# Agent Class - Fire brigade - Random Agent
########################################
class RandomFiremanAgent(Agent):
    location = [1,1]           
    Name = 'RandomFiremanAgent'
   
    def program(actions):
        return lambda percept: random.choice('Move Left','Move Right','Move Up','Move Down')


########################################
# Agent Class - Fire brigade - Reflex Agent
########################################
class ReflexFiremanAgent(Agent):

    def program(percept):
        location, things = percept





########################################
# AGENT PROGRAM
########################################
def programAgent(percept):
    
    # if not any(m != 'Visited' and m != 'Obstacle' for m in model.values()): return 'NoOp'
  
    location, things = percept


    for t in things[tuple(location)]:
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
   
    choice = random.choice(('Left','Right','Down','Up'))
    if  choice !=0:
        return 'Move ' + choice

    return programAgent

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

# Thing Class - Fire
class Wall(Obstacle):
    Name='Wall'
    pass

########################################
# ENVIRONMENT CLASS
########################################
# Forrest Class
class Forrest2D(GraphicEnvironment):
    # def percept(self, agent):
    #     listThings = []
    #     for things in self.list_things_at(agent.location):
    #         if things != agent:
    #             listThings.append(things)   
    #     """By default, agent perceives things within a default radius."""
    #     return agent.location, listThings
    
    
    def percept(self, agent):       
        # Check thigs in current location and the squares near
        x, y = agent.location
        listThings = {}
        listThings[(x,y)]=self.list_things_at(x, y)
        listThings['L']=self.list_things_at((x - 1, y))
        listThings['R']=self.list_things_at((x + 1, y))
        listThings['U']=self.list_things_at((x, y + 1))
        listThings['D']=self.list_things_at((x, y - 1))
        listThings.remove(Agent) if Agent in listThings else None
        return agent.location, listThings
    
       
    def thing_classes(self):
        return [Fire, Water, ModelFiremanAgent, Wall]

    def execute_action(self, agent, action):
        if action == 'Move Right':
            if agent.location[0] > 1 and agent.location[0]< 9:
                agent.location[0] += 1
            else:
                agent.location[0] = 2     
        elif action == 'Move Left':
            if agent.location[0] > 1 and agent.location[0] < 9:
                agent.location[0] -= 1
            else:
                agent.location[0] = 2        
        elif action == 'Move Up':
            if agent.location[1] > 1 and agent.location[1] < 9:
                agent.location[1] += 1
            else:
                agent.location[1] = 2            
        elif action == 'Move Down':
            if agent.location[1] > 1 and agent.location[1] < 9:
                agent.location[1] -= 1
            else:
                agent.location[1] = 2
        elif action == 'Take Water':
            items = self.list_things_at(agent.location, tclass=Water)
            for eachThing in items:
                if agent.takeWater(eachThing): 
                    agent.performance += 100
                    self.delete_thing(eachThing)
                    agent.isHoldingWater = True
                    print('Take Water')
        elif action == 'Estinguish Fire':
            items = self.list_things_at(agent.location, tclass=Fire)
            for eachThing in items:                  
                if agent.estinguishFire(eachThing):
                    agent.performance += 100
                    self.delete_thing(eachThing)
                    agent.isHoldingWater = False
                    print('Estinguish Fire')
                else:
                    agent.performance -= 100
                    print('Burning, no water')
        elif action == 'NoOp':
            agent.performance -= 100
            print('All good, enjoy the day!')
            
        print(agent.location)
        print(f'Fireman performance: {agent.performance}')

    def is_done(self):
        #TODO
        return False

def fillWord(env):
    "WALLS AROUND"
    env.add_walls()
    listPosition=([3,3],[3,2],[4,2])

    for l in listPosition:
        env.add_thing(Wall(), l)
    
########################################
# Start App - TODO main
########################################
model = {(x, y): None for x in range(10) for y in range(10)}
    
forrest = Forrest2D(9,9, color={'ModelFiremanAgent': (230, 115, 40), 'Water': (0, 200, 200), 'Fire': (200,0,0), 'Wall': (10,10,10)})
fillWord(forrest)

fireman = ModelFiremanAgent(programAgent)
fire = Fire()
water = Water()

forrest.add_thing(fireman, [3,4])
forrest.add_thing(water, [3,4])
forrest.add_thing(fire, [3,5])   

forrest.run(100,delay=0.1)

print(f'Fireman performance: {fireman.performance}')

print(model)
