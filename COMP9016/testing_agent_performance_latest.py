import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import random
from agents import *
from search import *
from scipy.spatial import distance

# random.seed(242734)
random.seed(0)
collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence 

################################################################
# Define the Fireman agent
################################################################
class Fireman(Agent):
    direction = Direction("down")

    def perceive(self, environment):
        """
        Return a list of things that the agent can perceive in its current location.
        """
        things = environment.list_things_at(self.location)
        return things

    def __init__(self, program=None):
        super().__init__(program)
        self.holding_water = False
        self.num_wildfires_extinguished = 0
        self.water_taken = 0
        self.path_length = 0

    def take_water(self, thing):
        if isinstance(thing, Water):
            self.holding_water = True
            return True
        elif isinstance(thing, Wildfire) and not agent.holding_water:
            return not thing.is_extinguished()

    def extinguish_fire(self, percept):
        for p in percept:
            if isinstance(p, Wildfire) and self.holding_water:
                self.num_wildfires_extinguished += 10
                return 'Extinguish'
        return None

    def turn_left(self):
        self.direction = self.direction + Direction.L  # Change direction left

    def turn_right(self):
        self.direction = self.direction + Direction.R  # Change direction right

    def bump(self, location):
        for thing in self.perceive(self):
            if isinstance(thing, Obstacle) and location == self.location:
                return True
        return False

    def move_forward(self, success=True):
        new_location = self.direction.move_forward(self.location)
        if self.bump(new_location):
            success = False
        return super().move(success)

class Water(Thing):
    pass

class Wildfire(Thing):
    def __init__(self, size):
#        super().__init()
        self.size = size

    def is_extinguished(self):
        return self.size == 0

class Wall(Obstacle):
    pass

class Path(Thing):
    pass

class ForrestEnvironment(GraphicEnvironment):

    def __init__(self, width, height, colors=None):
        super().__init__(width, height)
        self.add_walls()
        self.colors = colors

    def is_bump(self, location):
        for thing in self.list_things_at(location):
            if isinstance(thing, Obstacle):
                return True
        return False

    def execute_action(self, agent, action):
        agent.bump = False
        if action == 'Forward':
            new_location = agent.direction.move_forward(agent.location)
            agent.bump = self.move_to(agent, new_location)
            # Check if the agent bumped into an obstacle
            if not agent.bump:
                agent.location = new_location  # Update the agent's location
                agent.path_length += 1  # Increase path_length

        elif action == 'TurnLeft':
            agent.turn_left()

        elif action == 'TurnRight':
            agent.turn_right()

        elif action == 'Take Water':
            things = [thing for thing in self.list_things_at(agent.location) if agent.take_water(thing)]
            if things:
                agent.holding_water = True
                agent.water_taken += 1
                self.delete_thing(things[0])

        elif action == 'Extinguish':
            percept = agent.perceive(self)
            for p in percept:
                if isinstance(p, Wildfire) and agent.holding_water:
                    agent.holding_water = False
                    agent.num_wildfires_extinguished += 1
                    agent.delete_thing(p)             
    def step(self):
        if self.is_done():
            return
        for agent in self.agents:
            action = agent.program(self.percept(agent))
            self.execute_action(agent, action)
        self.update()

    def update(self, delay=0.01):
        sleep(delay)
        self.reveal()

    def draw(self, force=False):
        if not self.isVisible or not (self.width or self.height):
            return
        if force or self.step == 0 or self.step % self.display_frequency == 0:
            self.window.clear()
            for x in range(self.width):
                for y in range(self.height):
                    if self.inbounds((x, y)):
                        for thing in self.list_things_at((x, y)):
                            self.draw_thing(thing, (x, y))
            self.window.refresh()

# Reflex Agent program
def reflex_agent_program(percept, agent):
    for p in percept:
        if isinstance(p, Wildfire) and agent.holding_water:
            return 'Extinguish'
        elif isinstance(p, Water):
            return 'Take Water'
    if agent.holding_water:
        return random.choice(['Forward', 'TurnLeft', 'TurnRight'])
    else:
        return random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Take Water'])

# Random Agent program
def random_agent_program(percept, agent):
    if agent.holding_water:
        if random.random() < 0.5:
            return 'Extinguish'
        else:
            return 'Release'
    else:
        return random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Take Water'])

# Table based Agent program
def table_based_agent_program(percept, agent):
    holding_water = agent.holding_water
    wildfire_present = any(isinstance(p, Wildfire) for p in percept)
    state = (wildfire_present, holding_water)

    if state == (False, False):
        # If no wildfires are present and the agent is not holding water, choose random action.
        return random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Take Water'])
    elif state == (False, True):
        # If no wildfires are present but the agent is holding water, move forward.
        return 'Forward'
    elif state == (True, False):
        # If wildfires are present but the agent is not holding water, take water if available.
        if any(isinstance(p, Water) for p in percept):
            return 'Take Water'
        else:
            # If water is not available, choose a random action.
            return random.choice(['Forward', 'TurnLeft', 'TurnRight'])
    elif state == (True, True):
        # If wildfires are present and the agent is holding water, extinguish wildfires.
        return 'Extinguish'


# Create the firefighting environment
colors = {
    'Fireman':  (230, 115, 40),
    'Water':    (0, 200, 200),
    'Wildfire': (200, 0, 0),
    'Wall':     (50, 50, 50),
    'Visited':  (70, 110, 70),
    'Path':     (70, 110, 70)
}

# Define obstacles
obstacles = [(2, 2), (5, 4), (1, 4), (3, 7), (3, 5), (6, 1), (7, 3), (5, 7)]

# Create instances of the agents
reflex_agent = Fireman(program=lambda percept: reflex_agent_program(percept, reflex_agent))
random_agent = Fireman(program=lambda percept: random_agent_program(percept, random_agent))
table_based_agent = Fireman(program=lambda percept: table_based_agent_program(percept, table_based_agent))

agents = [reflex_agent, random_agent, table_based_agent]
# agents = [ table_based_agent]
agent_names = ['Reflex Agent', 'Random Agent', 'Table-Based Agent']

# Environment size
width = 10
height = 10

# Initialize the environment
env = ForrestEnvironment(width, height, colors=colors)

# Add obstacles to the environment
for obstacle in obstacles:
    x, y = obstacle
    env.add_thing(Wall(), (x, y))

# Add water and wildfires
env.add_thing(Water(), (6, 6))
env.add_thing(Water(), (2, 7))
env.add_thing(Wildfire(1), (5, 6))

# Create an empty dictionary to store performance metrics
# Create an empty dictionary to store performance metrics
performance_metrics = {
    'num_wildfires_extinguished': {},
    'water_taken': {},
    'path_length': {},
}

# Loop through agents one at a time and run the environment
agent_location = (6, 2)

for agent, agent_name in zip(agents, agent_names):
    # Initialize the environment
    env = ForrestEnvironment(width, height, colors=colors)

    # Add obstacles to the environment
    for obstacle in obstacles:
        x, y = obstacle
        env.add_thing(Wall(), (x, y))

    # Add water and wildfires
    env.add_thing(Water(), (6, 3))
    env.add_thing(Water(), (2, 3))
    env.add_thing(Wildfire(1), (7, 2))

    # Add the agent to the environment at the specified location
    env.add_thing(agent, location=agent_location)

    # Run the environment for a fixed number of steps
    env.run(400, delay=0.001)

    # Collect performance metrics for the current agent
    performance_metrics['num_wildfires_extinguished'][agent_name] = agent.num_wildfires_extinguished
    performance_metrics['water_taken'][agent_name] = agent.water_taken
    performance_metrics['path_length'][agent_name] = agent.path_length

    # Remove the agent from the environment for the next iteration
    env.delete_thing(agent)

# Print performance metrics for each agent
for agent_name, metrics in performance_metrics.items():
    print(f'Performance Metrics for {agent_name}:')
    for metric_name, metric_value in metrics.items():
        print(f'{metric_name}: {metric_value}')
    print('-' * 40)
