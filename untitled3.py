# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:53:03 2023

@author: josel
"""
import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define classes for objects in the environment
class Fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def extinguish(self):
        self.active = False

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Firefighter:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.water = 0
        self.performance = 100

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def grab_water(self):
        self.water = 100

    def extinguish_fire(self, fire):
        if self.water > 0 and fire.active:
            fire.extinguish()
            self.water -= 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Firefighter AI")

# Create objects in the environment
firefighter = Firefighter()
fires = [Fire(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(5)]
obstacles = [Obstacle(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(10)]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input here (e.g., arrow key presses)

    # Update the environment
    # Implement the logic for moving the firefighter, grabbing water, and extinguishing fires

    # Draw the environment
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (firefighter.x, firefighter.y), 20)  # Firefighter
    for fire in fires:
        if fire.active:
            pygame.draw.circle(screen, RED, (fire.x, fire.y), 10)  # Active fire
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, (obstacle.x, obstacle.y, 30, 30))  # Obstacle
    pygame.display.flip()

# Quit Pygame
pygame.quit()
