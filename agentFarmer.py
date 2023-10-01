from agents import *
#from notebook import psource

class Farmer(Agent):
    location = 1
    def move(self):
        if self.location == 1:
            self.location = 2
        else:
            self.location = 1
        print("Farmer moved to {}.".format(self.location))           
    def grabChicken(self, thing):
        if isinstance(thing, Chicken):
            print("Farmer grab a chicken {}.".format( self.location))
            return True
        return False       
    def grabFox(self, thing):
        if isinstance(thing, Fox):
            print("Farmer grab a fox {}.".format( self.location))
            return True
        return False      
    def grabFeed(self, thing):
        if isinstance(thing, Feed):
            print("Farmer grab the feed {}.".format( self.location))
            return True
        return False
    def eat(self, thing):
        print("Farmer wanted to eat at {}.".format(self.location))
        
   
class Chicken(Agent):
    location = 1
    def move(self):
        if self.location == 1:
            self.location = 2
        else:
            self.location = 1
        print("Chicken moved to location {}.".format(self.location))
    def eat(self, thing):
        print("Chicken eat at {}.".format(self.location))


class Fox(Agent):
    location = 1
    def move(self):
        if self.location == 1:
            self.location = 2
        else:
            self.location = 1
        print("Fox moved to location {}.".format(self.location))
    def eat(self, thing):
        print("Fox eat at {}.".format(self.location))


class Feed(Thing):
    location = 1
    pass


class Farm(Environment):
    def percept(self, agent):
        '''return a list of things that are in our agent's location'''
        things = self.list_things_at(agent.location)
        return things
    
    def execute_action(self, agent, action):
        '''changes the state of the environment based on what the agent does.'''
        # if action == "move":
        #     print('{} decided to {} from location: {}'.format(str(agent)[1:-1], action, agent.location))
        #     agent.move()
        #     agent.performance += 1
        # elif action == "grabChicken":
        #     items = self.list_things_at(agent.location)
        #     if len(items) != 0:
        #         if agent.grabChicken(items[0]):
        #             print('{} grabbed {} from location: {}'
        #                   .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
        #             agent.grabChicken()
        #             agent.move()
        #             agent.performance += 1
        ItemMoveA=list(self.state[Loc_A])
        ItemMoveB=list(self.state[Loc_B])
        ItemToMove=action.split()[-1]
        if action == "Right with " + ItemToMove:
            agemt.location = loc_A
            ItemMoveA.remove(ItemToMove)
            ItemMoveB.append(ItemToMove)
        if action == "eat":
            items = self.list_things_at(agent.location)
            if len(items) != 0:
            #if agent.eat(items[0]):
                #print(f'  This is items[0]: {items[0]}')
                print('{} eat {} from location: {}'
                      .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                #self.delete_thing((items[0])[1:-1])
                # print(f'  This is str(agent)[1:-1]: {str(agent)[1:-1]}')
                # print(f'  This is str(items[0])[1:-1]: {str(items[0])[1:-1]}')
                # print(f'  This is str(items[0]): {str(items[0])}')
                #self.agent.eat()
                agent.performance += 1
        # elif action == "eatChicken":
        #     items = self.list_things_at(agent.location, tclass=Fox)
        #     if len(items) != 0:
        #         if agent.eatChicken(items[0]):
        #             print('{} eat {} from location: {}'
        #                   .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
        #             self.delete_thing(things[0])
        #             self.agent.eatChicken()
        #             self.agent.performance -= 10
        # elif action == "eatFeed":
        #     items = self.list_things_at(agent.location, tclass=Chicken)
        #     if len(items) != 0:
        #         if agent.eatFeed(items[0]):
        #             print('{} eat {} from location: {}'
        #                   .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
        #             self.delete_thing(things[0])
        #             agent.eatFeed()
        #             agent.move()
        #             agent.performance -= 10
                    
        #elif action != 'NoOp':
            
         #   agent.performance -= 0
        #             agent.location = 2
        #             #self.delete_thing(items[0]) #Delete it from the Farm after.
        # elif action == "grabFox":
        #     items = self.list_things_at(agent.location, tclass=Fox)
        #     if len(items) != 0:
        #         if agent.grabFox(items[0]): 
        #             print('{} grabbed {} from location: {}'
        #                   .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
        #             agent.location = 2
        #             #self.delete_thing(items[0]) #Delete it from the Farm after.
        # elif action == "grabFeed":
        #     items = self.list_things_at(agent.location, tclass=Feed)
        #     if len(items) != 0:
        #         if agent.grabFeed(items[0]):
        #             print('{} grabbed {} from location: {}'
        #                   .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
        #             agent.location = 2
        # else:
        #     print('No valid actions available')
                    #self.delete_thing(items[0]) #Delete it from the Farm after.
# try to optimize grabbing by using only the method can_grab from Agent Class
        # elif action == 'Grab':
        #     things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing)]
        #     if things:    
        #         agent.holding.append(things[0])
        #         print("Grabbing ", things[0].__class__.__name__)
        #         self.delete_thing(things[0])
        # elif action == 'Release':
        #     if agent.holding:
        #         dropped = agent.holding.pop()
        #         print("Dropping ", dropped.__class__.__name__)
        #         self.add_thing(dropped, location=agent.location)




    def is_done(self):
        '''By default, we're done when we can't find a live agent, 
        but to prevent killing our cute dog, we will stop before itself - when there is no more food or water'''
        no_edibles=False
        for thing in self.things:
            no_edibles =  not isinstance(thing, Farmer) \
            and ((isinstance(thing, Feed) and isinstance(thing, Chicken) \
                 and Feed.location==Chicken.location) \
                 or (isinstance(thing, Fox) and isinstance(thing, Chicken) \
                 and Fox.location==Chicken.location))
        
        dead_agents = not any(agent.is_alive() for agent in self.agents)
        #Fail Game
        if no_edibles:
                print('Fail Game')
        
        return False
        #dead_agents or no_edibles

    def score(self, agent):

        return agent.performance
# class TrivialFarmerEnvironment(Environment):
#     """This environment has two locations, A and B. Each can have Chicken
#     Feed and Fox. The agent perceives its location and the location's
#     status."""

#     def __init__(self):
#         super().__init__()
#         print(self.status)
#         self.status = {loc_A: ['Chicken', 'Fox', 'Feed'],
#                        loc_B: 'Empty'}

#     def thing_classes(self):
#         return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent, TableDrivenVacuumAgent, ModelBasedVacuumAgent]

#     def percept(self, agent):
#         """Returns the agent's location, and the location status."""
#         return agent.location, self.status[agent.location]

#     def execute_action(self, agent, action):
#         if action == 'grabChicken':
#             agent.location = loc_B
#             agent.performance -= 1
#         elif action == 'grabFox':
#             agent.location = loc_A
#             agent.performance -= 1
#         # elif action == 'move':
#         #     if self.status[agent.location] == 'empty':
#         #         agent.performance += 10
#         #     self.status[agent.location] = 'Clean'

#     def default_location(self, thing):
#         """Agents start location A."""
#         return loc_A


loc_A, loc_B = 1, 2


farmerActions = ['grabChicken', 'grabFox', 'grabFeed', 'move']#, 'eat']
chickenActions = ['eat', 'move']
foxActions = ['eat', 'move']
#list = ['grabChicken']
#lambda percept: random.choice(list)
#test = random.choice(list)
#print(test)

newFarmerProgram = RandomAgentProgram(farmerActions)
foxProgram = RandomAgentProgram(foxActions)
chickenProgram = RandomAgentProgram(chickenActions)

farmer = Farmer(newFarmerProgram)
chicken = Chicken(chickenProgram)
fox = Fox(foxProgram)
feed = Feed()

farm = Farm()

farm.add_thing(farmer,1)
farm.add_thing(chicken,1)
farm.add_thing(fox,1)
farm.add_thing(feed,1)

items1 = farm.list_things_at(1)
items2 = farm.list_things_at(2)
scoreBeforeRunFarmer = farm.score(farmer)

print(f'\n\nFarmer Score before run: {scoreBeforeRunFarmer} \n\n')
#farm.is_done()

#chicken.grabFox(fox)
#print(farm.things)
farm.run(20)

items0 = farm.list_things_at(0)
items1 = farm.list_things_at(1)
items2 = farm.list_things_at(2)
scoreAfterRun = farm.score(farmer)
scoreAfterRunFox = farm.score(fox)
scoreAfterRunChicken = farm.score(chicken)
print(f'\n\nFarmer Score after run: {scoreAfterRun}')
print(f'Chicken Score after run: {scoreAfterRunChicken}')
print(f'Fox Score after run: {scoreAfterRunFox} \n')
print(farm.is_done())
# farm.delete_thing()


    # >>> list = ['Right', 'Left', 'Suck', 'NoOp']
    # >>> program = RandomAgentProgram(list)
    # >>> agent = Agent(program)
    # >>> environment = TrivialVacuumEnvironment()
    # >>> environment.add_thing(agent)
    # >>> environment.run()


def TableDrivenVacuumAgent():
    """Tabular approach towards vacuum world as mentioned in [Figure 2.3]
    >>> agent = TableDrivenVacuumAgent()
    >>> environment = TrivialVacuumEnvironment()
    >>> environment.add_thing(agent)
    >>> environment.run()
    >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    table = {((loc_A, 'Chicken','Fox','Feed'),): 'Right with Chicken',
              ((loc_A, 'Dirty'),): 'Suck',
              ((loc_B, 'Clean'),): 'Left',
              ((loc_B, 'Dirty'),): 'Suck',
              ((loc_A, 'Dirty'), (loc_A, 'Clean')): 'Right',
              ((loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
              ((loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck',
              ((loc_B, 'Dirty'), (loc_B, 'Clean')): 'Left',
              ((loc_A, 'Dirty'), (loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
              ((loc_B, 'Dirty'), (loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck'}
    return Agent(TableDrivenAgentProgram(table))
