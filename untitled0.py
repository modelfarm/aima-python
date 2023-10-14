# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:44:44 2023

@author: josel
"""

class Agent:
    def __init__(self):
        self.position = (0, 0)
        self.knowledge = {}  # Knowledge representation

    def perceive(self, environment):
        # Agent perceives its current location
        self.knowledge['current_location'] = self.position

    def act(self, environment):
        # Simple movement towards a goal
        goal = (3, 3)  # The agent's goal is to reach position (3, 3)
        x, y = self.position
        if x < goal[0]:
            x += 1
        elif x > goal[0]:
            x -= 1
        elif y < goal[1]:
            y += 1
        elif y > goal[1]:
            y -= 1
        self.position = (x, y)

class Environment:
    def __init__(self):
        self.grid_size = (5, 5)

    def is_goal_reached(self, agent):
        return agent.position == (3, 3)

if __name__ == "__main__":
    agent = Agent()
    environment = Environment()

    while not environment.is_goal_reached(agent):
        agent.perceive(environment)
        print(f"Agent's knowledge: {agent.knowledge}")
        agent.act(environment)

    print("Agent reached the goal!")
