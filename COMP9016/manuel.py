import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import *
from search import *
from ipythonblocks import BlockGrid

# Define custom agent class
class MyAgent(Agent):
    def execute_action(self, action):
        if action == 'Right':
            self.location = (self.location[0] + 1, self.location[1])
        elif action == 'Left':
            self.location = (self.location[0] - 1, self.location[1])
        elif action == 'Down':
            self.location = (self.location[0], self.location[1] + 1)
        elif action == 'Up':
            self.location = (self.location[0], self.location[1] - 1)
        elif action == 'TakeRope':
            things = [thing for thing in self.location.things if self.can_grab(thing)]
            if things:
                self.holding.append(things[0])
                self.location.remove(things[0])

class MyFieldEnv(GraphicEnvironment):
    def __init__(self, width, height, color=None):
        super().__init__(width, height, color=color)
        self.grid = BlockGrid(width, height, fill=(255, 255, 255))
        self.agent = None

    """2D World"""

    def percept(self, agent):
        """Location and things except None and Agent"""
        x, y = agent.location
        ThingDict = {}
        ThingDict[(x, y)] = self.list_things_at(x, y)
        ThingDict['L'] = self.list_things_at((x - 1, y))
        ThingDict['R'] = self.list_things_at((x + 1, y))
        ThingDict['U'] = self.list_things_at((x, y - 1))
        ThingDict['D'] = self.list_things_at((x, y + 1))
        ThingDict[(x, y)] = [thing for thing in ThingDict[(x, y)] if not isinstance(thing, Agent)]
        return agent.location, ThingDict

    def execute_action(self, agent, action):
        # Movement
        if action == 'Right':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveRight()
        elif action == 'Left':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveLeft()
        elif action == 'Down':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveDown()
        elif action == 'Up':
            print('Agent decided to Move {} from location: {}'.format(action, agent.location))
            agent.MoveUp()
        elif action == 'TakeRope':
            things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing)]
            if things:
                agent.holding.append(things[0])
                print("Take ", things[0].__class__.__name__)
                self.delete_thing(things[0])

# Define custom things and environment setup
class SlowMotion(Thing):
    pass

class Stone(Obstacle):
    pass

class Sand(SlowMotion):
    pass

class Water(SlowMotion):
    pass

class Treasure(Thing):
    pass

class Hole(Thing):
    pass

class Rope(Thing):
    pass

def FillWorld(Env):
    "WALLS AROUND"
    listPosition = [(3, 11), (4, 11), (5, 11)]
    for l in listPosition:
        Env.add_thing(Wall(), l)

    "Stones"
    for i in range(5):
        while True:
            w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
            if not any(Env.list_things_at(w_x, w_y)):
                Env.add_thing(Stone(), (w_x, w_y), True)
                break

    "Sand"
    for i in range(5):
        while True:
            w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
            if not any(Env.list_things_at(w_x, w_y)):
                Env.add_thing(Sand(), (w_x, w_y), True)
                break
    "Water"
    listPos = [(2, 13), (3, 13), (1, 2), (2, 2)]
    for l in listPos:
        Env.add_thing(Water(), l)

    "Hole"
    while True:
        w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
        if not any(Env.list_things_at(w_x, w_y)):
            Env.add_thing(Hole(), (w_x, w_y), True)
            break

    "Rope"
    while True:
        w_x, w_y = Env.random_location_inbounds(exclude=(1, 1))
        if not any(Env.list_things_at(w_x, w_y)):
            Env.add_thing(Rope(), (w_x, w_y), True)
            break

    "Treasure"
    Env.add_thing(Treasure(), (1, 18))

    # Remove the obstacles near the goal location
    for w_x in range(4, 7):
        for w_y in range(17, 19):
            obstacles_at_location = Env.list_things_at((w_x, w_y), tclass=Wall)
            for obstacle in obstacles_at_location:
                Env.delete_thing(obstacle)

    # Add the goal location
    goal_location = (5, 5)
    Env.add_thing(Treasure(), goal_location)

    agentManuel = MyAgent()
    Env.add_thing(agentManuel, (1, 1))

# Create the environment
MyField = MyFieldEnv(10, 20)
PosUsedMyMap = FillWorld(MyField)

# Define the problem by specifying the start and goal locations
initial_location = (1, 1)
goal_location = (5, 5)

# Define actions, result, and goal test functions
def actions(state):
    x, y = state
    possible_actions = []
    if x < 5:
        possible_actions.append('Right')
    if y < 5:
        possible_actions.append('Down')
    return possible_actions

def result(state, action):
    x, y = state
    if action == 'Right':
        return (x + 1, y)
    elif action == 'Down':
        return (x, y + 1)

def goal_test(state):
    return state == goal_location

# Define the initial_location (start state)
initial_location = (1, 1)  # Start at position (1, 1)

# Define the list of possible actions
actions = ['Right', 'Left', 'Down', 'Up', 'TakeRope']

# Define the result function
def result(state, action):
    x, y = state  # Extract the current location (state)

    if action == 'Right':
        # Move right (increment x coordinate)
        new_state = (x + 1, y)
    elif action == 'Left':
        # Move left (decrement x coordinate)
        new_state = (x - 1, y)
    elif action == 'Down':
        # Move down (increment y coordinate)
        new_state = (x, y + 1)
    elif action == 'Up':
        # Move up (decrement y coordinate)
        new_state = (x, y - 1)
    elif action == 'TakeRope':
        # Define logic for taking a rope (if applicable)
        # For example, check if there's a rope at the current location

        # You should implement the logic for taking a rope here
        # For simplicity, I'll assume the agent can always take a rope
        new_state = state  # No change in state

    # Return the new state after the action
    return new_state

# Define the goal_test function
def goal_test(state):
    # Define the condition for reaching the goal state
    return state == (5, 5)  # Agent reaches position (5, 5)

# Create the problem instance
AgentToTreasure = GraphProblem(initial_location, goal_test, actions, result)

from search import breadth_first_search

# Search for a solution using BFS
searcher = breadth_first_search(AgentToTreasure)

# Get the result of the search
result = searcher(AgentToTreasure)

# Check if a solution was found
if result:
    # Extract the list of actions to reach the goal
    solution_actions = result.solution()

    # Print the solution
    print("Solution found using BFS:")
    print("Actions:", solution_actions)
    print("Number of actions:", len(solution_actions))
else:
    print("No solution found using BFS.")


