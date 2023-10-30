import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

#from agents import *


from agents import Agent, Thing, Obstacle, Direction, GraphicEnvironment, collections
# from time import sleep
# from IPython.display import clear_output, HTML
import random

collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence 

################################################################
# Define the Fireman agent
################################################################
class Fireman(Agent):
    direction = Direction("right")

    def __init__(self, program=None):
        super().__init__(program)
        self.holding_water = None
        self.num_wildfires_extinguished = 0
        self.water_used = 0
        self.num_collisions = 0
        self.path_length = 0  # Added to track the path length
        self.visited_locations = set()  # Initialize an empty set for visited locations

    def perceive(self, environment):
        """
        Gather perceptual information from the environment.
        """
        # For example, you can gather things in the agent's location
        return environment.list_things_at(self.location)
    

    def can_grab(self, thing):
        if isinstance(thing, Water):
            return isinstance(thing, Water) and self.holding_water is None
        elif isinstance(thing, Wildfire):
            return isinstance(thing, Wildfire)
                       
    def release(self):
        if self.holding_water:
            water = Water()
            water.location = self.location
            self.holding_water = None
            #self.delete_thing(water)
            return water

    def extinguish_fire(self, percept):
        for p in percept:
            if isinstance(p, Wildfire) and self.holding_water:
                #self.delete_thing(p)
                self.num_wildfires_extinguished += 1
                self.water_used += 1
                return 'Extinguish'
        return None
    
    def turn_left(self):
        self.direction = self.direction.turn_left()

    def turn_right(self):
        self.direction = self.direction.turn_right()
       
    def bump(self, location):
        for thing in self.list_things_at(location):
            if isinstance(thing, Obstacle):
                self.num_collisions += 1
                return True
        return False

    def move(self, success=True):
        new_location = self.direction.move(self.location)
        if self.bump(new_location):
            self.num_collisions += 1
            success = False
        if success:
            self.visited_locations.add(self.location)
            self.path_length += 1
        return super().move(success)

################################################################
# Define the Water class
################################################################
class Water(Thing):
    pass

################################################################
# Define the Wildfire class
################################################################
class Wildfire(Thing):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def is_extinguished(self):
        return self.size == 0

################################################################
# Define the Obstacle class
################################################################
class Wall(Obstacle):
    pass

################################################################
# Define the FirefightingEnvironment class
################################################################
class FirefightingEnvironment(GraphicEnvironment):
    def __init__(self, width=9, height=9, colors=None):
        super().__init__(width, height)
        self.add_walls()
        self.colors = colors #if colors is not None else {}

    def add_thing(self, thing, location=None, exclude_duplicate_class_items=False):
        #if location is None:
        #    super().add_thing(thing)
        #el
        if self.is_inbounds(location):
            if (exclude_duplicate_class_items and
                    any(isinstance(t, thing.__class__) for t in self.list_things_at(location))):
                return
            super().add_thing(thing, location)

    def add_wildfires(self, num_wildfires):
        for _ in range(num_wildfires):
            x, y = self.random_location_inbounds()
            size = random.randint(1, 3)
            self.add_thing(Wildfire(size), (x, y))

    def add_water(self, num_water):
        for _ in range(num_water):
            x, y = self.random_location_inbounds()
            self.add_thing(Water(), (x, y))

    def add_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            x, y = self.random_location_inbounds()
            self.add_thing(Wall(), (x, y))
    
    def bump(self, location):
        """
        Check if bumping into a wall or obstacle.
        """
        for thing in self.things:
            if isinstance(thing, Obstacle) and location == thing.location:
                return True
        return False


    def execute_action(self, agent, action):
        if action == 'Forward':
            new_location = agent.direction.move_forward(agent.location)
            if self.is_inbounds(new_location) and not self.bump(new_location):
                self.move_to(agent, new_location)
            if action == 'TurnLeft':
                agent.turn_left()
            elif action == 'TurnRight':
                agent.turn_right()  # For turning right
        elif action == 'Grab':
            things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing)]
            if things:
                agent.holding_water = things[0]
                self.delete_thing(things[0])
        elif action == 'Release':
            if agent.holding_water:
                water = Water()
                water.location = agent.location
                agent.holding_water = None
                self.add_thing(water, location=agent.location)
        elif action == 'Extinguish':
            percept = agent.perceive(self)
            for p in percept:
                if isinstance(p, Wildfire) and agent.holding_water:
                    agent.delete_thing(p)
         
    def step(self):
        if self.is_done():
            return
        for agent in self.agents:
            action = agent.program(self.percept(agent))
            self.execute_action(agent, action)
        self.update()

    
    """
    The Fireman class keeps track of visited locations in the visited_locations set,
    and the FirefightingEnvironment class displays these visited locations 
    as 'Visited'. This will help you visualize which locations the agent 
    has visited during its actions.
    """        
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
                    if (x, y) in self.visited_locations:
                        self.draw_cell('Visited', (x, y))  # Display visited locations
            self.window.refresh()

################################################################
# Define the reflex agent program
################################################################
def reflex_agent_program(percept, agent):
    for p in percept:
        if isinstance(p, Wildfire) and agent.holding_water:
            agent.delete_thing(p)
            return 'Extinguish'
        elif isinstance(p, Wildfire) and not agent.holding_water:
            agent.delete_thing(p)
            return 'Extinguish'
    
    if agent.holding_water:
        return random.choice(['Forward', 'TurnLeft', 'TurnRight'])
    else:
        return random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Grab'])

################################################################
# Define the random agent program
################################################################
def random_agent_program(percept, agent):
    if agent.holding_water:
        if random.random() < 0.5:  # Probability of extinguishing fire
            return 'Extinguish'
        else:
            return 'Release'
    else:
        return random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Grab'])

################################################################
# Define a lookup table where states are represented as 
# tuples (wildfire_present, holding_water)
# and actions are strings ('Extinguish', 'Grab', etc.)
################################################################
lookup_table = {
    (True, True): 'Extinguish',
    (True, False): 'Grab',
    (False, True): random.choice(['Forward', 'TurnLeft', 'TurnRight']),
    (False, False): random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Grab']),
}

def table_based_agent_program(percept, agent):
    wildfire_present = any(isinstance(p, Wildfire) for p in percept)
    state = (wildfire_present, agent.holding_water)
    
    # Look up the action based on the current state
    action = lookup_table.get(state)
    
    if not action:
        action = random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Grab'])
    return action

################################################################
# Create the firefighting environment
################################################################

colors = {
    'Fireman':  (230, 115, 40),
    'Water':    (0, 200, 200),
    'Wildfire': (200, 0, 0),
    'Wall':     (50, 50, 50),
    'Visited':  (70,110,70)
}
env = FirefightingEnvironment(width=10, height=10, colors=colors)

# Create instances of the agents
# reflex_agent = Fireman(program=lambda percept: reflex_agent_program(percept, reflex_agent))
# random_agent = Fireman(program=lambda percept: random_agent_program(percept, random_agent))
table_based_agent = Fireman(program=lambda percept: table_based_agent_program(percept, table_based_agent))

# Add agents to the environment
# env.add_thing(reflex_agent, location=(1, 1))
# env.add_thing(random_agent, location=(1, 2))
env.add_thing(table_based_agent, location=(1, 3))

# Add wildfires, water, and obstacles to the environment
env.add_wildfires(3)
env.add_water(3)
env.add_obstacles(6)

# Run the environment
env.run(100, delay=0.01)


# def run_agent(agent, agent_name, num_episodes=10):
#     total_metrics = {
#         'num_wildfires_extinguished': 0,
#         'water_used': 0,
#         'num_collisions': 0,
#         'path_length': 0,
#     }

#     for _ in range(num_episodes):
#         env = FirefightingEnvironment(width=10, height=10, colors=colors)
#         env.add_thing(agent, location=(1, 1))
#         env.add_wildfires(3)
#         env.add_water(3)
#         env.add_obstacles(6)

#         env.run(50, delay=0.01)

#         total_metrics['num_wildfires_extinguished'] += agent.num_wildfires_extinguished
#         total_metrics['water_used'] += agent.water_used
#         total_metrics['num_collisions'] += agent.num_collisions
#         total_metrics['path_length'] += agent.path_length

#         # Reset the agent's internal performance metrics
#         agent.num_wildfires_extinguished = 0
#         agent.water_used = 0
#         agent.num_collisions = 0
#         agent.path_length = 0

#     # Calculate the average performance metrics
#     num_episodes_float = float(num_episodes)
#     average_metrics = {
#         key: value / num_episodes_float for key, value in total_metrics.items()
#     }

#     return average_metrics



# Create instances of the agents
# reflex_agent = Fireman(program=lambda percept: reflex_agent_program(percept, reflex_agent))
# random_agent = Fireman(program=lambda percept: random_agent_program(percept, random_agent))
# table_based_agent = Fireman(program=lambda percept: table_based_agent_program(percept, table_based_agent))

# # Run each agent and collect their performance metrics
# num_episodes = 1
# reflex_agent_metrics = run_agent(reflex_agent, 'Reflex Agent', num_episodes)
# random_agent_metrics = run_agent(random_agent, 'Random Agent', num_episodes)
# table_based_agent_metrics = run_agent(table_based_agent, 'Table-Based Agent', num_episodes)

# # Print the performance metrics for each agent
# print('Performance of Reflex Agent:')
# print(reflex_agent_metrics)
# print('-' * 40)

# print('Performance of Random Agent:')
# print(random_agent_metrics)
# print('-' * 40)

# print('Performance of Table-Based Agent:')
# print(table_based_agent_metrics)
# print('-' * 40)
