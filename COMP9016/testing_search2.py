import random
import heapq

class GridEnvironment:
    def __init__(self, width, height, num_wildfires, num_water, num_obstacles):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]
        self.fireman = None
        self.wildfires = []
        self.water_sources = []
        self.obstacles = []
        
        # Create boundary walls
        for i in range(width):
            self.grid[0][i] = 1
            self.grid[height - 1][i] = 1
        for i in range(height):
            self.grid[i][0] = 1
            self.grid[i][width - 1] = 1
        
        # Randomly place wildfires, water sources, and obstacles
        self.place_objects(num_wildfires, self.wildfires)
        self.place_objects(num_water, self.water_sources)
        self.place_objects(num_obstacles, self.obstacles)

    def place_objects(self, num_objects, objects_list):
        for _ in range(num_objects):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if self.grid[y][x] == 0:
                    self.grid[y][x] = 2  # 2 represents wildfires or water
                    objects_list.append((x, y))
                    break

    def set_fireman(self, x, y):
        self.fireman = (x, y)
    
    def is_valid_location(self, x, y):
        return 0 < x < self.width - 1 and 0 < y < self.height - 1

    def get_neighbors(self, x, y):
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(nx, ny) for nx, ny in neighbors if self.is_valid_location(nx, ny) and self.grid[ny][nx] != 1]

class AStarSearch:
    def __init__(self, environment):
        self.environment = environment

    def heuristic(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def search(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {node: float('inf') for node in self.environment.water_sources}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.environment.water_sources}
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            for neighbor in self.environment.get_neighbors(current[0], current[1]):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None

    def execute_plan(self, path):
        for i in range(len(path) - 1):
            start = path[i]
            goal = path[i + 1]
            self.environment.set_fireman(start[0], start[1])
            self.environment.grid[goal[1]][goal[0]] = 0  # Remove water source

def main():
    width, height = 10, 10
    num_wildfires, num_water, num_obstacles = 3, 3, 3

    environment = GridEnvironment(width, height, num_wildfires, num_water, num_obstacles)
    fireman_x, fireman_y = random.randint(1, width - 2), random.randint(1, height - 2)
    environment.set_fireman(fireman_x, fireman_y)

    astar_search = AStarSearch(environment)

    while environment.wildfires:
        for wildfire in environment.wildfires:
            path = astar_search.search(environment.fireman, wildfire)
            if path:
                astar_search.execute_plan(path)
            else:
                print("No path to wildfire.")
            environment.wildfires.remove(wildfire)
            if not environment.wildfires:
                print("All wildfires extinguished.")
                break

if __name__ == "__main":
    main()
