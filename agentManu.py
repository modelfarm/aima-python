from agents import *
from notebook import psource

def TableDrivenFarmerAgent():
    """Tabular approach towards vacuum world as mentioned in [Figure 2.3]
    >>> agent = TableDrivenFarmerAgent()
    >>> environment = TrivialVacuumEnvironment()
    >>> environment.add_thing(agent)
    >>> environment.run()
    >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    # table = {((loc_A, ['Chicken', 'Fox', 'Feed'])): 'Right with Chicken',
    #          ((loc_A, ['Fox','Feed'])): 'Right with Fox',
    #          ((loc_A, ['Chicken','Feed'])): 'Right with Feed',
    #          ((loc_A, ['Chicken'])): 'Right with Chicken',
    #          ((loc_B, ['Chicken'])): 'Left Alone',
    #          ((loc_B, ['Chicken','Fox'])): 'Left with Chicken',
    #          ((loc_B, ['Fox','Feed'])): 'Left Alone',}
    # table = {((loc_A, 'Chicken', 'Fox', 'Feed')): 'Right with Chicken',
    #     ((loc_A, 'Fox','Feed')): 'Right with Fox',
    #     ((loc_A, 'Chicken','Feed')): 'Right with Feed',
    #     ((loc_A, 'Chicken')): 'Right with Chicken',
    #     ((loc_B, 'Chicken')): 'Left Alone',
    #     ((loc_B, 'Chicken','Fox')): 'Left with Chicken',
    #     ((loc_B, 'Fox','Feed')): 'Left Alone',}
    table = {((loc_A, ('Chicken', 'Fox', 'Feed')),): 'Right with Chicken',
        ((loc_A, ('Fox','Feed')),): 'Right with Fox',
        ((loc_A, ('Chicken','Feed')),): 'Right with Feed',
        ((loc_A, ('Chicken')),): 'Right with Chicken',
        ((loc_B, ('Chicken')),): 'Left Alone',
        ((loc_B, ('Chicken','Fox')),): 'Left with Chicken',
        ((loc_B, ('Fox','Feed')),): 'Left Alone',}
    return Agent(TableDrivenAgentProgram(table))


class TrivialFarmerEnvironment(Environment):
    """This environment has two locations, A and B. Each can have Chicken
    Feed and Fox. The agent perceives its location and the location's
    status."""

    def __init__(self):
        super().__init__()
        self.status = {loc_A:('Chicken', 'Fox', 'Feed'),
                       loc_B: ''}

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent, TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """Returns the agent's location, and the location status."""
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        NewStatusA=list(self.status[loc_A])
        NewStatusB=list(self.status[loc_B])
        #Take the las word = element to move
        if action is not None:
            ElemntToMove= action.split()[-1]
            #Actions
            if action == 'Right with ' + ElemntToMove:
                agent.location = loc_B
                #agent.performance -= 1
                if ElemntToMove in self.status[loc_A]:
                    NewStatusA.remove(ElemntToMove)
                    NewStatusB.append(ElemntToMove)
            if action == 'Left with ' + ElemntToMove:
                agent.location = loc_A
                #agent.performance += 1
                if ElemntToMove in self.status[loc_B]:
                    NewStatusB.remove(ElemntToMove)
                    NewStatusA.append(ElemntToMove)
            if action == 'Right Alone ':
                agent.location = loc_B
            if action == 'Left Alone ':
                agent.location = loc_A
        self.status[loc_A]=tuple(NewStatusA)
        self.status[loc_B]=tuple(NewStatusB)
                    
    def default_location(self, thing):
        """Agents start location A."""
        return loc_A


# #Instances
Farmer = TableDrivenFarmerAgent()
River = TrivialFarmerEnvironment()
River.add_thing(Farmer)
River.run(20)
print(River.status)
#River.status == {(1,0):['Chicken', 'Fox', 'Feed'] , (0,0) : 'Clean'}

# agent1 = TableDrivenVacuumAgent()
# environment1 = TrivialVacuumEnvironment()
# environment1.add_thing(agent1)
# environment1.run(20)
# environment1.status == {(1,0):'Clean' , (0,0) : 'Clean'}