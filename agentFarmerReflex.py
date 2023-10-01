from agents import *
import inspect
#from notebook import psource

class Farmer(Agent):
    location = 'loc_A'
    def move(self):
        if self.location == 'loc_A':
            self.location = 'loc_B'
        else:
            self.location = 'loc_A'
        print("Farmer moved to {}.".format(self.location))
        
    def can_grab(self, thing, tclass):
        # print(thing)
        # print(self)
        if isinstance(thing,(Fox,Chicken,Feed)) and self.location == 'loc_A':
            pass

class Fox(Thing):
    location = 'loc_A'
    def eatChicken(self):
        print('Fox eat a Chicken at location {}.'.format(self.location))
                
class Chicken(Thing):
    location = 'loc_A'
    def eatFeed(self, thing):
        print(self)
        print("Chicken eat at {}.".format(self.location))

class Feed(Thing):
    location = 'loc_A'
    pass

def status(self):
    return (isinstance(thing,(Fox,Chicken,Feed)) and agent.location)


class TrivialFarmEnv(Environment):

    def __init__(self):
        # super().__init__()
        # self.status = {loc_A: ['Farmer', 'Fox', 'Chicken','Feed'],
        #                loc_B: None}
        
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                loc_B: random.choice(['Clean', 'Dirty'])}

    def thing_classes(self):
        return [Farmer, Chicken, Fox, Feed, ReflexFarmerAgent]
    
    def percept(self, agent):
        '''return a list of things that are in our agent's location'''
        # things = self.list_things_at(agent.location)
        return (agent.location, self.status[agent.location])
    
    def execute_action(self, agent, action):
        # try to optimize grabbing by using only the method can_grab from Agent Class
        if action == 'Grab':
            agent.location = 'loc_A'
            # things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing,isinstance(thing,(Fox,Chicken,Feed)))]
            #for thing in self.list_things_at(agent.location):
            for thing in self.list_things_at('loc_A'):    
                if isinstance(thing,(Fox,Chicken,Feed)) and agent.location=='loc_A':
                    agent.holding.append(thing)
                    print("Grabbing ", thing.__class__.__name__)
                    self.delete_thing(thing)
                    if agent.holding:
                        agent.move()
                        dropped = agent.holding.pop()
                        print("Dropping ", dropped.__class__.__name__)
                        self.add_thing(dropped, location=agent.location)
                        agent.move()
            if not (isinstance(thing,(Fox,Chicken,Feed))) and agent.location=='loc_A':
                agent.location = 'loc_B'
    
    
    def is_done(self):
        '''By default, we're done when we can't find a live agent, 
        but to prevent killing our cute dog, we will stop before itself - when there is no more food or water'''
        no_edibles = False
        allThingsSameLocation = False
        
        for thing in self.things:
            no_things = not isinstance(thing, Farmer) \
                        and ((isinstance(thing, Feed) and isinstance(thing, Chicken) \
                        and Feed.location==Chicken.location) \
                        or (isinstance(thing, Fox) and isinstance(thing, Chicken) \
                        and Fox.location==Chicken.location))
        
        dead_agents = not any(agent.location=='loc_A' for agent in self.agents)
        
        #print(dead_agents)

        if (no_things or dead_agents):
                print('Game Over')     
        return False
        #dead_agents or no_things

    def score(self, agent):
        return agent.performance
      



def SimpleReflexAgentProgram():
    if any(agent.location=='loc_A' for agent in self.agents):
        return status
    
    if status == 'Agents in place':
        return True

    if bump == 'Bump':
        value = random.choice((1, 2))
    else:
        value = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward

    if value == 1:
        return 'TurnRight'
    elif value == 2:
        return 'TurnLeft'
    else:
        return 'Forward'


def ReflexFarmerAgent(SimpleReflexAgentProgram):
    def program(percept):
        location, status = percept
        if location != 'loc_B':
            return 'Grab'
        # elif location == loc_A:
        #     return 'Right'
        # elif location == loc_B:
        #     return 'Left'

    return Agent(program)

##########################################################################
# These are the two locations for the two-state environment
loc_A, loc_B = (0, 0), (1, 0)

# Initialize the two-state environment
farm = TrivialFarmEnv()

#farmerActions = ['Grab','Release','move']
newFarmer = ReflexFarmerAgent(SimpleReflexAgentProgram)
farmer = Farmer(newFarmer)

chicken = Chicken()
fox = Fox()
feed = Feed()

farm.add_thing(farmer,'loc_A')
farm.add_thing(chicken,'loc_A')
farm.add_thing(fox,'loc_A')
farm.add_thing(feed,'loc_A')

print(farm.list_things_at('loc_A'))
print(farm.list_things_at('loc_B'))
scoreBeforeRunFarmer = farm.score(farmer)
print(f'\n\nFarmer Score before run: {scoreBeforeRunFarmer} \n\n')
#farm.is_done()

#TraceAgent(farmer)

farm.run(8)


print(farm.list_things_at('loc_A'))
print(farm.list_things_at('loc_B'))
scoreAfterRun = farm.score(farmer)

print(f'\n\nFarmer Score after run: {scoreAfterRun}')
#print(farm.is_done())