# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:54:21 2023

@author: josel
"""

import random
class Environment(object):
    def __init__(self):
        # instantiate locations and conditions
        # 0 indicates Clean and 1 indicates Dirty
        self.locationCondition = {'A': '0', 'B': '0','C': '0','D': '0','E': '0'}
        
    # randomize conditions in locations A and B     
        self.locationCondition['A'] = random.randint(0, 1)     
        self.locationCondition['B'] = random.randint(0, 1)
        self.locationCondition['C'] = random.randint(0, 1)
        self.locationCondition['D'] = random.randint(0, 1)
        self.locationCondition['E'] = random.randint(0, 1)


class SimpleReflexVacuumAgent(Environment):
    def __init__(self, Environment):
        print(Environment.locationCondition)
        
        # Instantiate performance measurement
        Score = 0
        # place vacuum at random location
        vacuumLocation = random.randint(0, 1)
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
        print(Environment.locationCondition)     
        print("Performance Measurement: " + str(Score))

theEnvironment = Environment()
theVacuum = SimpleReflexVacuumAgent(theEnvironment)
