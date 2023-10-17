import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import random
from agents import *
from search import *
from scipy.spatial import distance

random.seed(242734)

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
        self.holding_water = None
        self.num_wildfires_extinguished = 0
        self.water_used = 0
        self.num_collisions = 0
        self.path_length = 0
        self.visited_locations = set()

    def can_take_water(self, thing):
        if isinstance(thing, Water):
            self.water_used += 1
            return self.holding_water is True
        elif isinstance(thing, Wildfire) and not agent.holding_water:
            self.num_collisions += 5
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
                self.num_collisions += 1
                return True
        return False

    def move_forward(self, success=True):
        new_location = self.direction.move_forward(self.location)
        if self.bump(new_location):
            self.num_collisions += 1
            success = False
        if success:
            self.visited_locations.add(self.location)
            self.path_length += 1
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
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))       
        elif action == 'TurnLeft':
            agent.turn_left()
        elif action == 'TurnRight':
            agent.turn_right()
        elif action == 'Take Water':
            things = [thing for thing in self.list_things_at(agent.location) if agent.can_take_water(thing)]
            if things:
                agent.holding_water = things[0]
                self.delete_thing(things[0])
        elif action == 'Extinguish':
            percept = agent.perceive(self)
            for p in percept:
                if isinstance(p, Wildfire) and agent.holding_water:
                    agent.holding_water = False
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
                    if (x, y) in self.visited_locations:
                        self.draw_cell('Visited', (x, y))
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
lookup_table = {
    (True, True): 'Extinguish',
    (True, False): 'Take Water',
    (False, True): random.choice(['Forward', 'TurnLeft', 'TurnRight']),
    (False, False): random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Take Water']),
}

def table_based_agent_program(percept, agent):
    wildfire_present = any(isinstance(p, Wildfire) for p in percept)
    holding_water = agent.holding_water is not None
    state = (wildfire_present, holding_water)
    action = lookup_table.get(state)
    if not action:
        action = random.choice(['Forward', 'TurnLeft', 'TurnRight', 'Take Water'])
    return action

# Create the firefighting environment
colors = {
    'Fireman':  (230, 115, 40),
    'Water':    (0, 200, 200),
    'Wildfire': (200, 0, 0),
    'Wall':     (50, 50, 50),
    'Visited':  (70, 110, 70),
    'Path':  (70, 110, 70)
}

# Define obstacles
obstacles = [(2, 2), (5, 4), (3, 1), (1, 4), (6, 4), (5, 7), (3, 3), (3, 5), (6, 1), (7, 3), (5, 2)]

# Create instances of the agents
reflex_agent = Fireman(program=lambda percept: reflex_agent_program(percept, reflex_agent))
random_agent = Fireman(program=lambda percept: random_agent_program(percept, random_agent))
table_based_agent = Fireman(program=lambda percept: table_based_agent_program(percept, table_based_agent))

agents = [reflex_agent, random_agent, table_based_agent]
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
env.add_thing(Water(), (6, 3))
env.add_thing(Wildfire(1), (7, 3))

# Create an empty dictionary to store performance metrics
performance_metrics = {
    'num_wildfires_extinguished': {},
    'water_used': {},
    'num_collisions': {},
    'path_length': {},
}

# Loop through agents one at a time and run the environment
agent_location = (6, 2)

for agent, agent_name in zip(agents, agent_names):
    env.add_thing(agent, location=agent_location)
    env.run(20, delay=0.001)  # Adjust the number of steps as needed

    # Collect performance metrics for the current agent
    performance_metrics['num_wildfires_extinguished'][agent_name] = agent.num_wildfires_extinguished
    performance_metrics['water_used'][agent_name] = agent.water_used
    performance_metrics['num_collisions'][agent_name] = agent.num_collisions
    performance_metrics['path_length'][agent_name] = agent.path_length

    # Remove the agent from the environment for the next iteration
    env.delete_thing(agent)

# Print performance metrics for each agent
for agent_name, metrics in performance_metrics.items():
    print(f'Performance Metrics for {agent_name}:')
    for metric_name, metric_value in metrics.items():
        print(f'{metric_name}: {metric_value}')
    print('-' * 40)


####################################################################
#
#
####################################################################

# Search initial state.
start = agent_location
goal = (6, 2)

class FirefightingProblem(Problem):
    def __init__(self, initial, goal=None, graph=None):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, state):
        # Return possible movements (up, down, left, right) that do not lead to obstacles.
        x, y = state
        possible_actions = []

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.graph) and 0 <= new_y < len(self.graph[0]) and self.graph[new_x][new_y] != 'Obstacle':
                possible_actions.append((new_x, new_y))

        return possible_actions

    def result(self, state, action):
        # Return the state after taking the given action.
        return action

    def goal_test(self, state):
        # Check if the state is at the exit point (goal).
        return state == self.goal

    def path_cost(self, cost_so_far, state1, action, state2):
        # Assign a cost of 1 per move (action).
        return cost_so_far + 1

    # def h(self, node):
    #     # Estimate the remaining distance to the goal using Euclidean distance.
    #     x1, y1 = node.state
    #     x2, y2 = self.goal
    #     return int(distance.euclidean((x1, y1), (x2, y2)))
    
    def h(self, node):
        # Manhattan distance
        x1, y1 = node.state
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)
    

class FirefightingNode(Node):
    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
        self.depth = 0 if parent is None else parent.depth + 1

def create_firefighting_graph(width, height, obstacles, start, goal):
    # Create a grid-based graph representing the firefighting environment.
    graph = [[''] * height for _ in range(width)]

    for x, y in obstacles:
        graph[x][y] = 'Obstacle'

    graph[start[0]][start[1]] = 'Start'
    graph[goal[0]][goal[1]] = 'Goal'

    return graph
# Create the grid-based graph.
graph = create_firefighting_graph(width, height, obstacles, start, goal)

# Create a FirefightingProblem instance with the defined initial and goal states.
problem = FirefightingProblem(start, goal, graph)

# Find the optimal path using A* search.
#from scipy.spatial import distance
goal_node_astar = astar_search(problem, display=True)

# Extract the optimal path from the goal node.
optimal_path_astar = [n.state for n in goal_node_astar.path()]

# Get the number of iterations
iterations = goal_node_astar.path_cost

# Print the optimal path and other information
print("Optimal Path:", optimal_path_astar)
print("Number of Iterations:", iterations)
print("Goal node:", goal_node_astar)


# Find the goal node using best first graph search.
goal_node_bfgs = best_first_graph_search(problem, problem.h, display=True)
# Find the goal node using best first graph search.
goal_node_bfgs = best_first_graph_search(problem, problem.h, display=True)
# Find the goal node using uniform cost search.
goal_node_ucs = uniform_cost_search(problem, problem.h)
# Extract the optimal path from the goal node.
goal_nodes = [goal_node_astar, goal_node_bfgs, goal_node_ucs]

optimal_path = [n.state for node in goal_nodes for n in node.path()]
print(optimal_path)

# Calculate the path cost
path_cost = len(optimal_path) - 1
def add_path(self, obstacles):
    for each in obstacles:
        print(each)
        x, y = each
        self.add_thing(Path(), (x, y))

# Display the optimal path
add_path(env, optimal_path)
env.run(0, delay=0.01)

###########################################################################

def compare_graph_searchers(uninformed_searchers):
    """Prints a table of search results."""
    outputString = 'Actions/Goal Tests/States/Goal\n'
    print(outputString)
    compare_searchers(problems=[problem], header=['Searcher', 'Path / Goal Tests/ States / Goal Found'], searchers=uninformed_searchers)


searchers=[breadth_first_tree_search,
           breadth_first_graph_search,
           depth_first_graph_search,
           iterative_deepening_search,
           depth_limited_search]
    
compare_graph_searchers(searchers)

"""
Complexity is expressed in terms of three quantities:
b, the branching factor or maximum number of successors of any node.
d, the depth of the shallowest goal node (i.e., the number of steps along the path from the root). 
m, the maximum length of any path in the state space.
"""
# Searcher                     Path / Goal Tests/ States / Goal Found at (2, 4) from (6, 2)
# breadth_first_tree_search    <   448/   449/  1368/(2, 4) >           
# breadth_first_graph_search   <    26/    33/    73/(2, 4) >           
# depth_first_graph_search     <    37/    38/   110/(2, 4) >           
# iterative_deepening_search   <   232/   681/   679/(2, 4) >           
# depth_limited_search         <   184/   463/   533/(2, 4) >
# depth_first_tree_search      < incomplete due to loopy path, resulted in infinite loop, ran out of memory. >