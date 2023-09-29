# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 11:00:18 2023

@author: josel
"""

import random
import matplotlib.pyplot as plt

class Environment:
    def __init__(self):
        self.grid = [[random.choice(['clean', 'dirty']) for _ in range(2)] for _ in range(2)]
        self.agent_location = (0, 0)
        self.steps = 0

    def is_dirty(self, x, y):
        return self.grid[x][y] == 'dirty'

    def clean(self, x, y):
        self.grid[x][y] = 'clean'

    def percept(self):
        x, y = self.agent_location
        return self.is_dirty(x, y)

    def step(self, action):
        x, y = self.agent_location
        if action == 'clean':
            self.clean(x, y)
        elif action == 'move_right':
            if y < 1:
                self.agent_location = (x, y + 1)
        elif action == 'move_down':
            if x < 1:
                self.agent_location = (x + 1, y)
        self.steps += 1

    def display(self):
        plt.imshow([[1 if self.is_dirty(i, j) else 0 for j in range(2)] for i in range(2)], cmap='gray')
        plt.title(f'Steps: {self.steps}')
        plt.axis('off')
        plt.show()

class VacuumCleanerAgent:
    def __init__(self):
        self.actions = ['clean', 'move_right', 'move_down']
        self.current_action = 0

    def choose_action(self, percept):
        if percept == 'dirty':
            return 'clean'
        else:
            return self.actions[self.current_action]

    def update_action(self):
        self.current_action = (self.current_action + 1) % len(self.actions)

# Create the environment and agent
env = Environment()
agent = VacuumCleanerAgent()

# Run for a few steps and display the environment
for _ in range(2):
    percept = env.percept()
    action = agent.choose_action(percept)
    env.step(action)
    agent.update_action()

    env.display()
