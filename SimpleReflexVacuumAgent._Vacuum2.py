# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:54:21 2023

@author: josel
"""

import random
import matplotlib.pyplot as plt


class Environment(object):
    def __init__(self):
        
        # instantiate locations and conditions
        # 0 indicates Clean and 1 indicates Dirty
    #     self.locationCondition = {'A': '0', 'B': '0','C': '0','D': '0','E': '0'}
        
    # # randomize conditions in locations A and B     
    #     self.locationCondition['A'] = random.randint(0, 1)     
    #     self.locationCondition['B'] = random.randint(0, 1)
    #     self.locationCondition['C'] = random.randint(0, 1)
    #     self.locationCondition['D'] = random.randint(0, 1)
    #     self.locationCondition['E'] = random.randint(0, 1)
        self.grid = [[random.choice(['clean', 'dirty']) for _ in range(2)] for _ in range(2)]
        self.grid == [['clean'], ['dirty']]
        
        #self.grid = [[random.choice(['clean', 'dirty']) for _ in range(2)] for _ in range(2)]
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
        


class SimpleReflexVacuumAgent(Environment):
    def __init__(self, Environment):
        self.actions = ['clean', 'move_right', 'move_down']
        self.current_action = 0
        
        print(Environment.locationCondition)
        
        
        # Instantiate performance measurement
        Score = 0
        # place vacuum at random location
        #vacuumLocation = random.randint(0, 1)
        
        def choose_action(self, percept):
            if percept == 'dirty':
                return 'clean'
            else:
                return self.actions[self.current_action]

        def update_action(self):
            self.current_action = (self.current_action + 1) % len(self.actions)
        
        
        
        
        # if vacuum at A
#        if vacuumLocation == 0:
        #print("Vacuum is randomly placed at Location A.")
        for eachEnvLocation in Environment.locationCondition:
            # and Location A is Dirty.
            if Environment.locationCondition[eachEnvLocation] == 1:
                print(f'Location { eachEnvLocation } is Dirty.')
                # suck the dirt  and mark it clean
                Environment.locationCondition[eachEnvLocation] = 0;
                Score += 1
                print(f'Location { eachEnvLocation } has been Cleaned.')
                # move to B
                #print(f'Moving to Location ')
                Score -= 1
                # if B is Dirty
                if eachEnvLocation == 1:
                    print("Location B is Dirty.")
                    # suck and mark clean
                    eachEnvLocation = 0;
                    Score += 1
                    print("Location B has been Cleaned.")
            else:
                print(f' Location { eachEnvLocation } is Clean.')
                # move to B
                Score -= 1
                print(f' Moving to the next Location.')
                # if B is Dirty
                if Environment.locationCondition[eachEnvLocation] == 1:
                    print(f' Location { eachEnvLocation } is Dirty.')
                    # suck and mark clean
                    Environment.locationCondition[eachEnvLocation] == 0;
                    Score += 1
                    print(f' Location { eachEnvLocation } has been Cleaned.')       
    
                    # done cleaning     
#         print(Environment.locationCondition)     
#         print("Performance Measurement: " + str(Score))

#theEnvironment = Environment()
#theVacuum = SimpleReflexVacuumAgent(theEnvironment)

# Create the environment and agent
env = Environment()
agent = VacuumCleanerAgent()

# Run for a few steps and display the environment
for _ in range(8):
    percept = env.percept()
    action = agent.choose_action(percept)
    env.step(action)
    agent.update_action()

    env.display()
    
[[random.choice(['clean', 'dirty']) for _ in range(2)] for _ in range(2)]