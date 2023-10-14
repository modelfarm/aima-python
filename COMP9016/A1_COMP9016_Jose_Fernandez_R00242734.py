import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import *
from search import *

from scipy.spatial import distance
#from notebook import psource

import random

random.seed(242734)

collections
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence

# Agent Class - Fire brigade Agent - Model
class ModelFireman(Agent):
    location = [0, 0]
    Name = 'ModelFireman'
    Agent.isHoldingWater = False

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
    

# model = {(x, y): None for x in range(6) for y in range(6)}

def programAgent(percept):
    location, things = percept
    for t in things:
        # if model[tuple(location)] not in['Visited']:
        if isinstance(t, Fire):
            model[tuple(location)] = 'Fire'
            print('There is Fire')
            return 'Estinguish Fire'
        elif isinstance(t, Water):
            model[tuple(location)] = 'Water'
            print('There is Water')
            return 'Take Water'
        model[tuple(location)] = t  # Update the model here

    if not isinstance(model[tuple(location)], (Water, Fire)):
        model[tuple(location)] = 'Visited'

    choice = random.choice(('L', 'R', 'D', 'U'))
    if choice !=0:
        if choice == 'L':
            pass
        elif choice == 'R':
            pass
        elif choice == 'D':
            pass
        elif choice == 'U':
            pass
    return 'Move' + choice

    return programAgent  # , model


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

class Wall(Obstacle):
    Name='Wall'
    pass

class Path(Thing):
    pass


class Forrest2D(GraphicEnvironment):
    def percept(self, agent):
        listThings = []
        for things in self.list_things_at(agent.location):
            if things != agent:
                listThings.append(things)
        """By default, agent perceives things within a default radius."""
        return agent.location, listThings

    def thing_classes(self):
        return [Fire, Water, ModelFireman]

    def execute_action(self, agent, action):
        if action == 'MoveR':
            if agent.location[0]>=0 and agent.location[0]< 5:
                agent.location[0]+=1
                agent.performance -= 1
                # print('R here we go')
        elif action == 'MoveL':
            if agent.location[0]>0 and agent.location[0]<=5:
                agent.location[0]-=1
                agent.performance -= 1
                # print('L here we go')
        elif action == 'MoveU':
            if agent.location[1]>=0 and agent.location[1]<5:
                agent.location[1]+=1
                agent.performance -= 1
                # print('U here we go')
        elif action == 'MoveD':
            if agent.location[1]>0 and agent.location[1]<=5:
                agent.location[1]-=1
                agent.performance -= 1
                # print('D here we go')
        elif action == 'Take Water':
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.takeWater(items[0]):
                    agent.performance += 100
                    self.delete_thing(items[0])
                    agent.isHoldingWater = True
                    print('New action to Take Water')
        elif action == 'Estinguish Fire':
            items = self.list_things_at(agent.location, tclass=Fire)
            if len(items) != 0:
                if agent.estinguishFire(items[0]) and agent.isHoldingWater:
                    agent.performance += 100
                    self.delete_thing(items[0])
                    agent.isHoldingWater = False
                    print('New action to Estinguish Fire')
                else:
                    agent.performance -= 100
                    print('Burning, no water')

            if model[tuple(agent.location)] == 'Visited':
                agent.performance -= 10

        print(model[tuple(agent.location)])
        print(agent.location)
        print(
            f'Fireman performance: {agent.performance} and is holding water: {agent.isHoldingWater}')

    def is_done(self):

        return False
    

width = 10
height = 10

model = {(x, y): None for x in range(width) for y in range(height)}
forrest = Forrest2D(width, height, color={'ModelFireman': (230, 115, 40), 'Water': (
    0, 200, 200), 'Fire': (200, 0, 0), 'Wall': (50, 50, 50), 'Path': (120, 0, 100)})

# Define the positions of obstacles.
obstacles = [(0,1),(5, 4), (3, 1), (1, 4), (6, 4), (5, 7), (3, 3),
            (3,5),(6,1),(7,3),(5,2)]


def add_obstacles(self, obstacles):
    for each in obstacles:
        print(each)
        x, y = each
        self.add_thing(Wall(), (x, y))


fireman = ModelFireman(programAgent)
fire = Fire()
water = Water()
wall = Wall()

forrest.add_thing(fireman, [1, 1])
forrest.add_thing(water, [3, 4])
forrest.add_thing(fire, [3, 5])
add_obstacles(forrest, obstacles)

#forrest.run(500, delay=0.01)
#print(f'Fireman performance: {fireman.performance} and is holding water: {fireman.isHoldingWater}')


###Search problem
def DicMapCreation(width,height,BlockPos):
    rows = height-1
    columns = width-1

    # Lista de posiciones bloqueadas
    GameMap = {}
    def is_inside_grid(x, y):
        return 0 < x <= columns and 0 < y <= rows

    # Generar las posibilidades de movimiento y sus costos, excluyendo las posiciones bloqueadas
    for x in range(1, columns + 1):
        for y in range(1, rows + 1):
            CurrPos = (x, y)
            
            # Verificar si la posición actual está bloqueada
            if CurrPos not in BlockPos:
                transitions = {}
                
                # Movimiento hacia arriba
                if is_inside_grid(x - 1,y) and (x - 1,y) not in BlockPos:
                    transitions[(x - 1,y)] = random.randint(1, 100)
                # Movimiento hacia abajo
                if is_inside_grid(x + 1,y) and (x + 1,y) not in BlockPos:
                    
                    transitions[(x + 1,y)] = random.randint(1, 100)
                # Movimiento hacia la izquierda
                if is_inside_grid(x,y - 1) and (x,y - 1) not in BlockPos:
                    transitions[(x,y - 1)] = random.randint(1, 100)
                # Movimiento hacia la derecha
                if is_inside_grid(x,y + 1) and (x,y + 1) not in BlockPos:
                    transitions[(x,y + 1)] = random.randint(1, 100)
                
                if transitions:
                    GameMap[CurrPos] = transitions

    # Prnint dictionary
    # for location, transitions in GameMap.items():
    #     print(f'From {location}: {transitions}')
    return GameMap
# print(model)


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

    def h(self, node):
        # Estimate the remaining distance to the goal using Euclidean distance.
        x1, y1 = node.state
        x2, y2 = self.goal
        return int(distance.euclidean((x1, y1), (x2, y2)))
    

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

# Define the dimensions of the grid and the initial state.
start = (0, 0)
goal = (6, 7)


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

add_path(forrest, optimal_path)

forrest.run(0, delay=0.01)

def compare_graph_searchers(uninformed_searchers):
    """Prints a table of search results."""
    outputString = 'Actions/Goal Tests/States/Goal\n'
    print(outputString)
    compare_searchers(problems=[problem], header=['Searcher', '(1,1) to (6,7)'], searchers=uninformed_searchers)


searchers=[breadth_first_tree_search,
           breadth_first_graph_search,
           depth_first_graph_search,
           iterative_deepening_search,
           depth_limited_search]
    
compare_graph_searchers(searchers)