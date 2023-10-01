from agents import *
import inspect
#from notebook import psource

class Farmer(Agent):
    
    def move(self):    
        if self.location == 'loc_A':
            self.location = 'loc_B'
        else:
            self.location = 'loc_A'
        #print(" Farmer moved to {}.".format(self.location))
        
    def can_grab(self, thing, tclass):
        # print(thing)
        # print(self)
        if isinstance(thing,(Fox,Chicken,Feed)) and self.location == 'loc_A':
            pass
            #self.move()
            #thing.location = self.location
            #print('{} grabbed {} at location {}.'.format(self.__class__.__name__, thing.__class__.__name__, self.location))

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


class Farm(Environment):   
    def percept(self, agent):
        '''return a list of things that are in our agent's location'''
        things = self.list_things_at(agent.location)
        return things
    
    def execute_action(self, agent, action):
        if action == "eatChicken":
            items = self.list_things_at(agent.location, tclass=Fox)
            #print(str(agent.eatChicken))
            if len(items) != 0:
                if str(items[0])[1:-1] != str(agent)[1:-1]:
                    print('{} eat {} from location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.agent.eatChicken()
                    #self.agent.performance -= 10
                   
        if action == "eatFeed":
            items = self.list_things_at(agent.location, tclass=Chicken)
            #print(str(agent.eatChicken))
            if len(items) != 0:
                if str(items[0])[1:-1] != str(agent)[1:-1]:
                    print('{} eat {} from location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.agent.eatFeed()
                    #self.agent.performance -= 10

        # try to optimize grabbing by using only the method can_grab from Agent Class
        elif action == 'Grab':
            #agent.location = 'loc_A'
            # things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing,isinstance(thing,(Fox,Chicken,Feed)))]
            #for thing in self.list_things_at(agent.location):
            
            for thing in self.list_things_at('loc_A'):
                agent.location = 'loc_A'
                if isinstance(thing,(Fox,Chicken,Feed)): # and thing.location == 'loc_A':
                    agent.holding.append(thing)
                    #agent.location = 'loc_A'
                    print("{} grabbing a {} at location {}".format(agent.__class__.__name__, thing.__class__.__name__, agent.location))
                    self.delete_thing(thing)
                    if agent.holding:
                        agent.location = 'loc_B'
                        #agent.move()
                        dropped = agent.holding.pop()
                        print(" {} dropped a {} at location {}".format(agent.__class__.__name__, dropped.__class__.__name__, agent.location))
                        self.add_thing(dropped, location=agent.location)
                elif isinstance(agent,Farmer):
                    agent.move()
                           

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
        
        dead_agents = not any(agent.is_alive() for agent in self.agents for agent in self.agents)
        
        #print(dead_agents)

        if (no_things or dead_agents):
                print('Game Over')
        return False
        #dead_agents or no_things

    def score(self, agent):
        return agent.performance

def RandomFarmerProgram(actions):
    return lambda percept: random.choice(actions)


farmerActions = ['Grab','Release','move']
newFarmerProgram = RandomFarmerProgram(farmerActions)
farmer = Farmer(newFarmerProgram)

chicken = Chicken()
fox = Fox()
feed = Feed()

farm = Farm()
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

farm.run()


print(farm.list_things_at('loc_A'))
print(farm.list_things_at('loc_B'))
scoreAfterRun = farm.score(farmer)

print(f'\n\nFarmer Score after run: {scoreAfterRun}')
print(farm.is_done())