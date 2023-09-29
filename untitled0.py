# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 10:56:35 2023

@author: josel
"""

import pygame
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define grid dimensions and cell size
GRID_SIZE = 2
CELL_SIZE = 100

class Environment:
    def __init__(self):
        # Initialize a 2x2 grid with random dirt distribution
        self.grid = [[random.choice(['clean', 'dirty']) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.agent_location = (0, 0)

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
            if y < GRID_SIZE - 1:
                self.agent_location = (x, y + 1)
        elif action == 'move_down':
            if x < GRID_SIZE - 1:
                self.agent_location = (x + 1, y)

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

# Initialize Pygame
pygame.init()

# Create a window
window_size = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Vacuum Cleaner Agent")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Create instances of the environment and agent
env = Environment()
agent = VacuumCleanerAgent()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    percept = env.percept()
    action = agent.choose_action(percept)
    env.step(action)
    agent.update_action()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if env.is_dirty(x, y):
                pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(2)

pygame.quit()
