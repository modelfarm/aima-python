"""
Created on Tue Oct 3rd 13:40 2023
@author: Ruairi.OReilly

The following imports assume that your aima repo could is in the parent folder
of the current file.
"""
import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 


"""

Exercise - The Farmer's Dilemma

> Note we assume the farmer starts in location A along with the chicken, feed and fox.
> Specify a \href{https://en.wikipedia.org/wiki/State_diagram}{state diagram} that realises the above solution (text, table, drawing - your choice).
> Derive the list of percepts that would be experienced by a farmer agent to include location, chicken, feed and fox.
> Define the appropriate actions needed for solving the problem.
>  Generate the percept sequence necessary map the appropriate actions for the problem to be solved.
 > Implement a TableDrivenAgentProgram (see agents.py) that will solve this problem - note may require customisation of a TableDrivenAgentProgram and associated environment.

State Diagram: Each state can be represented as a tuple. Each item can be at location A or B. Initial state. Everything at location A.

(Farmer, Chicken, Fox, Feed)
(A,A,A,A)

The actions are as follows:
                                (Farmer, Chicken, Fox, Feed)    
Farmer and chicken cross to B.  (A,A,A,A)   => (B,B,A,A)
Farmer returns to A.                        => (A,B,A,A)
Farmer and fox cross to B.                  => (B,B,B,A)
Farmer and chicken return to A.             => (A,A,B,A) 
Farmer and feed cross to B.                 => (B,A,B,B)
Farmer returns to A.                        => (A,A,B,B)
Farmer and chicken cross to B.              => (B,B,B,B)

Success! Everything at location B.

Actions required: 
take_chicken        - change location of chicken and farmer
take_fox            - change location of fox and farmer
take_feed           - change location of feed and farmer
return_alone        - change location of farmer

(A,A,A,A)
(A,A,A,A), (B,B,A,A)
(A,A,A,A), (B,B,A,A), (A,B,A,A)
(A,A,A,A), (B,B,A,A), (A,B,A,A), (B,B,B,A)
(A,A,A,A), (B,B,A,A), (A,B,A,A), (B,B,B,A), (A,A,B,A)
(A,A,A,A), (B,B,A,A), (A,B,A,A), (B,B,B,A), (A,A,B,A), (B,A,B,B) 
(A,A,A,A), (B,B,A,A), (A,B,A,A), (B,B,B,A), (A,A,B,A), (B,A,B,B), (A,A,B,B)
(A,A,A,A), (B,B,A,A), (A,B,A,A), (B,B,B,A), (A,A,B,A), (B,A,B,B), (A,A,B,B), (B,B,B,B) 




"""
from agents import Agent, Environment, TableDrivenAgentProgram

class RiverCrossingEnvironment(Environment):
    
    def __init__(self, agent):
        super().__init__()
        self.agents = [agent]
        self.status = {agent: ('A', 'A', 'A', 'A')}  # Set the initial status here
               
    def percept(self, agent):
        current_percept = self.status[agent]

        # Return the current state as a percept.
        print("Current Percept: {}".format(current_percept))
        print("Current Percept Type: {}".format(type(current_percept)))
        return current_percept

    def execute_action(self, agent, action):
        state = list(self.status[agent])
        print("Current state: {}, Action: {}".format(state, action))

        if action == "take_chicken":
            state[0] = 'B' if state[0] == 'A' else 'A'
            state[1] = 'B' if state[1] == 'A' else 'A'
            agent.performance -= 1
        elif action == "take_fox":
            state[0] = 'B' if state[0] == 'A' else 'A'
            state[2] = 'B' if state[2] == 'A' else 'A'
            agent.performance -= 1
        elif action == "take_feed":
            state[0] = 'B' if state[0] == 'A' else 'A'
            state[3] = 'B' if state[3] == 'A' else 'A'
            agent.performance -= 1
        elif action == "return_alone":
            state[0] = 'B' if state[0] == 'A' else 'A'
            agent.performance -= 1

        self.status[agent] = tuple(state)
        
        if tuple(state) == '[B,B,B,B]': agent.performance += 10

table = {
    (('A', 'A', 'A', 'A'),): "take_chicken",
    (('A', 'A', 'A', 'A'), ('B', 'B', 'A', 'A')): "return_alone",
    (('A', 'A', 'A', 'A'), ('B', 'B', 'A', 'A'), ('A', 'B', 'A', 'A')): "take_fox",
    (('A', 'A', 'A', 'A'), ('B', 'B', 'A', 'A'), ('A', 'B', 'A', 'A'), ('B', 'B', 'B', 'A')): "take_chicken",
    (('A', 'A', 'A', 'A'), ('B', 'B', 'A', 'A'), ('A', 'B', 'A', 'A'), ('B', 'B', 'B', 'A'), ('A', 'A', 'B', 'A')): "take_feed",
    (('A', 'A', 'A', 'A'), ('B', 'B', 'A', 'A'), ('A', 'B', 'A', 'A'), ('B', 'B', 'B', 'A'), ('A', 'A', 'B', 'A'), ('B', 'A', 'B', 'B')): "return_alone",
    (('A', 'A', 'A', 'A'), ('B', 'B', 'A', 'A'), ('A', 'B', 'A', 'A'), ('B', 'B', 'B', 'A'), ('A', 'A', 'B', 'A'), ('B', 'A', 'B', 'B'), ('A', 'A', 'B', 'B')): "take_chicken"
}


def qA():

    program = TableDrivenAgentProgram(table)
    agent = Agent(program)
    env = RiverCrossingEnvironment(agent)

    # Simulate the steps to solve the problem.
    for _ in range(8):
        env.step()
    print("Final state: {}".format(env.status[agent]))
    print(agent.performance)

qA()

"""
An agent's performance is tied to the environment in which it operates. While an agent might excel in one environment due to favourable conditions or well-suited tasks, the same agent could underperform in another with different dynamics or unpredictabilities. This dependency arises because the agent's actions, based on its perceptions and actuators, often have varied consequences across different environments. Thus, optimal performance requires an agent to be tailored to the specific characteristics and challenges of its environment.

To that end, taking the four agents discussed in lectures:
> RandomVacuumAgent, TableDrivenVacuumAgent, ReflexVacuumAgent, ModelBasedVacuumAgent
> Specify the PEAS for each (in a 5x5 table).
+---------------------+-------------+--------------+------------+---------+
| Agent               | Performance | Environment  | Actuators  | Sensors |
+---------------------+-------------+--------------+------------+---------+
| RandomVacuum        | Clean sqrs  | 2-sq (D/C)   | L, R, Suck | Sq & Loc|
+---------------------+-------------+--------------+------------+---------+
| TableDrivenVacuum   | Clean sqrs  | 2-sq (D/C)   | L, R, Suck | Sq & Loc|
+---------------------+-------------+--------------+------------+---------+
| ReflexVacuum        | Clean sqrs  | 2-sq (D/C)   | L, R, Suck | Sq & Loc|
+---------------------+-------------+--------------+------------+---------+
| ModelBasedVacuum    | Clean sqrs  | 2-sq (D/C)   | L, R, Suck | Sq & Loc|
+---------------------+-------------+--------------+------------+---------+
Legend:

    Clean sqrs = Number of clean squares
    2-sq (D/C) = Two-square environment (Dirty/Clean)
    L, R, Suck = Left move, Right move, Suck dirt
    Sq & Loc = Square status and location
+---------------------+-------------+--------------+------------+---------+


> Perform a comparative analysis of the agents operating in a TrivialVacuumEnvironment.

In the context of TrivialVacuumEnvironment, the PEAS descriptor for all these agents is pretty similar since they all operate in the same environment and have access to the same actuators and sensors. The main distinction among these agents is in their internal decision-making algorithms, which decide their actions based on their perceptions.


> Detail the different characteristics of the agents and how that relates to their performance.

"""

from agents import (TrivialVacuumEnvironment, RandomVacuumAgent, 
                    TableDrivenVacuumAgent, ReflexVacuumAgent, ModelBasedVacuumAgent)


def simulate_environment(agent, environment, steps):
    environment.add_thing(agent)
    for _ in range(steps):
        environment.step()
    return agent.performance


def qB():

    steps = 100

    random_agent = RandomVacuumAgent()
    random_performance = simulate_environment(random_agent, TrivialVacuumEnvironment(), steps)

    table_driven_agent = TableDrivenVacuumAgent()
    table_driven_performance = simulate_environment(table_driven_agent, TrivialVacuumEnvironment(), steps)

    reflex_agent = ReflexVacuumAgent()
    reflex_performance = simulate_environment(reflex_agent, TrivialVacuumEnvironment(), steps)

    model_based_agent = ModelBasedVacuumAgent()
    model_based_performance = simulate_environment(model_based_agent, TrivialVacuumEnvironment(), steps)

    print("Performance after {} steps:".format(steps))
    print("RandomVacuumAgent:", random_performance)
    print("TableDrivenVacuumAgent:", table_driven_performance)
    print("ReflexVacuumAgent:", reflex_performance)
    print("ModelBasedVacuumAgent:", model_based_performance)

# qB()


""""
Moving from a static two-tile environment to an arbitrary one-dimensional environment requires a more dynamic approach to measuring performance. Instead of simply checking two states, performance should now consider the agent's ability to navigate and adapt across a broader range of tiles. Performance metrics could involve the efficiency in covering all tiles, the no. steps taken to achieve an ``is done'' state. The increased complexity emphasizes adaptability and comprehensive understanding of the entire environment.


To that end, try and utilise the ``VacuumEnvironment''for the following three agents discussed in lectures:
> RandomVacuumAgent, ReflexVacuumAgent, ModelBasedVacuumAgent
> Ensure you alter the env to be 1-dimensional.
> Alter the three agents as nessecary to operate in this environment.
> Perform a comparative analysis of the agents.
> Detail the different characteristics of the agents and how the change in the environment relates to their performance.
"""

myagent = ModelBasedVacuumAgent()