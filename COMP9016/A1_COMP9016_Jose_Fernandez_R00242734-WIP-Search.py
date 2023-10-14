import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from search import Problem, Node, astar_search
import numpy as np
from scipy.spatial import distance

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
            if self.graph[new_x][new_y] != 'Obstacle':
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
width = 10
height = 10
start = (1, 1)
goal = (5, 5)

# Define the positions of obstacles.
obstacles = [(3, 3), (3, 4), (4, 3),(3, 2), (3,1), (3,5),(3,6), (3,0), (3,7),(3,8)]

# Create the grid-based graph.
graph = create_firefighting_graph(width, height, obstacles, start, goal)

# Create a FirefightingProblem instance with the defined initial and goal states.
problem = FirefightingProblem(start, goal, graph)

# Find the optimal path using A* search.
goal_node = astar_search(problem)

# Extract the optimal path from the goal node.
optimal_path = [n.state for n in goal_node.path()]

# Get the number of iterations
iterations = goal_node.path_cost

# Print the optimal path and other information.
print("Optimal Path:", optimal_path)
print("Number of Iterations:", iterations)
print(goal_node)
# In goal_node contains the final node 
# in the search tree, which includes the optimal path. 
# The number of iterations corresponds to the path_cost 
# of this goal node. To access these values directly 
# from the goal_node object.


