from agents import *
#from notebook import psource

class Farmer(Agent):
    
    def move(self):    
        if self.location == 'loc_A':
            self.location = 'loc_B'
        else:
            self.location = 'loc_A'
            
class Chicken(Thing):
    #location = 'loc_A'
    #print("Chicken moved to location {}.".format(location))
    pass

class Fox(Thing):
    #location = 'loc_A'
    #print("Fox moved to location {}.".format(location))
    pass

class Feed(Thing):
    #location = 'loc_A'
    pass

class Farm(Environment):
    def percept(self, agent):
        '''return a list of things that are in our agent's location'''
        things = self.list_things_at(agent.location)
        return things
    
    def execute_action(self, agent, action):
        if action == 'Move':
            agent.move()
        elif action == 'Grab':
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
            
        '''changes the state of the environment based on what the agent does.'''
        #print(f'{ agent } percives { self } to { action }')

    def is_done(self):        
        return False

    def score(self, agent):
        return agent.performance

def RandomFarmerProgram(actions):
    return lambda percept: random.choice(actions)

farmerActions = ['Grab', 'Move']
newFarmerProgram = RandomFarmerProgram(farmerActions)

farmer = Farmer(newFarmerProgram)
chicken = Chicken()
fox = Fox()
feed = Feed()

farm = Farm()

farm.add_thing(farmer,'loc_A')
farm.add_thing(chicken,'loc_A')
farm.add_thing(fox,1)
farm.add_thing(feed,1)

# items1 = farm.list_things_at(1)
# items2 = farm.list_things_at(2)
# scoreBeforeRunFarmer = farm.score(farmer)

# print(f'\n\nFarmer Score before run: {scoreBeforeRunFarmer} \n\n')

farm.run()

# items1 = farm.list_things_at('loc_A')
# items2 = farm.list_things_at('loc_B')
# scoreAfterRun = farm.score(farmer)
# scoreAfterRunFox = farm.score(fox)
# scoreAfterRunChicken = farm.score(chicken)
# print(f'\n\nFarmer Score after run: {scoreAfterRun}')
# print(f'Chicken Score after run: {scoreAfterRunChicken}')
# print(f'Fox Score after run: {scoreAfterRunFox} \n')
# print(farm.is_done())
