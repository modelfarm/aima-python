# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:40 2020
@author: Ruairi.OReilly

The following imports assume that your aima repo could is in the parent folder
of the current file.
"""
import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from search import UndirectedGraph, GraphProblem, compare_searchers, breadth_first_tree_search, breadth_first_graph_search,  depth_first_graph_search, iterative_deepening_search, depth_limited_search, depth_first_tree_search

"""
QB - Discover Ireland - Uninformed search


Generate a graph based representation of Irish towns, cities, villages that 
adheres to the following requirements:
a) Contains at least 15 nodes. 
b) At least 5 nodes have a branching factor of 3.
c) At least one path with a depth of 8.

"""
  

# CHANGE TO IRELAND
# Precisely define your problem and solution#
#

"""
>> (a) >> So 15 node would indicate 15 towns/cities - I went with 16 which 
satisfies condition a.

(Cork, Waterford, Tralee, Limerick, Dublin, Carlow, Kilkenny, Portlaoise,
Galway, Westport, Belfast, Rosslare, Athlone, Sligo, Letterkenny, Derry)

The interconnectivity of these towns/cities is entirely fictional - I drew
them on a page and decided which town/city to connect to which city that would
give me an interesting graph. 

ireland_map = UndirectedGraph(dict(
    Cork=dict(Waterford=, Tralee=, Limerick=),
    Waterford=dict(Kilkenny=, Rosslare=),
    Tralee=dict(Limerick=),
    Carlow=dict(Kilkenny=, Portlaoise=),
    Portlaoise=dict(Limerick=, Dublin=),
    Galway=dict(Limerick=, Westport=, Athlone=),
    Dublin=dict(Athlone=, Belfast=))
    Sligo=dict(Westport=, Letterkenny=),
    Derry=dict(Letterkenny=, Belfast=))

Note: Some of the towns/cities are represented by their interconnectivity
between other towns/cities e.g. Athlone

>> (b) >> Dublin, Galway, Limerick, Cork, Waterford, Portlaoise have at least 3 
children which satisfies condition (b).

Now I used google maps to give my path cost for the distances between the 
towns/cities. (Not nessecary - any values would do but it makes it more
realistic for me)

ireland_map = UndirectedGraph(dict(
    Cork=dict(Waterford=121, Tralee=113, Limerick=99),
    Waterford=dict(Kilkenny=52, Rosslare=70),
    Tralee=dict(Limerick=100),
    Carlow=dict(Kilkenny=38, Portlaoise=37),
    Portlaoise=dict(Limerick=114, Dublin=89),
    Galway=dict(Limerick=98, Westport=79, Athlone=86),
    Dublin=dict(Athlone=123, Belfast=166))
    Sligo=dict(Westport=100, Letterkenny=112),
    Derry=dict(Letterkenny=34, Belfast=114))

INTERESTING OBSERVATION NOT RELATED TO COURSE - Using google maps from Sligo 
(Rep. of Ireland) to  Derry (Northern Ireland) provides the route in miles 
instead of km, while using  google maps from Dublin (Rep. of Ireland) to 
Belfast (Northern Ireland) uses km. It could that the units of measurement are
 decided based on the weighting of the distance in the respective country?

>> (b) >> Dublin, Galway, Limerick, Cork, Waterford, Portlaoise have at least 3 
children which satisfies condition (b).

>> (c) >> Rosslare to Letterkenny is at least 8 nodes which satisfies condition
(c).

"""

ireland_map = UndirectedGraph(dict(
    Cork=dict(Waterford=121, Tralee=113, Limerick=99),
    Waterford=dict(Kilkenny=52, Rosslare=70),
    Tralee=dict(Limerick=100),
    Carlow=dict(Kilkenny=38, Portlaoise=37),
    Portlaoise=dict(Limerick=114, Dublin=89),
    Galway=dict(Limerick=98, Westport=79, Athlone=86),
    Dublin=dict(Athlone=123, Belfast=166),
    Sligo=dict(Westport=100, Letterkenny=112),
    Derry=dict(Letterkenny=34, Belfast=114)))

"""
Generate three problem statements that will be used to evaluate the uninformed 
search strategies. These should be designed to demonstrate some property of the
 search approach which you found interesting - briefly discuss. 
 Compare the following search approaches performance:

- breadth\_first\_tree\_search 
- breadth\_first\_graph\_search 
- depth\_first\_tree\_search 
- depth\_first\_graph\_search.
- depth\_limited\_search
- iterative\_deepening\_search
- bidirectional\_search


Use the functionality made available by ``search.py'' (line 1500+) in order to
compare your approaches. Provide a table of results for each problem statement
and a rationale as the primary differentiation between graph and tree based 
approaches. Similarly discuss the pro's con's of each approach from your 
understanding of the theory and experimental validation. 
(print outs or comments in python - your call) 


To start off we generate three instance of the class GraphProblem provided by 
search.py that enables us to generate a problem for searching a graph from one 
node to another.
"""

#STUDENT_TO_DO Review the superclass Problem and the subclass GraphProblem

cork_To_Dublin_problem = GraphProblem('Cork', 'Dublin', ireland_map)
rosslare_To_Letterkenny_problem = GraphProblem('Rosslare', 'Letterkenny', ireland_map)
limerick_To_Belfast_problem = GraphProblem('Limerick', 'Belfast', ireland_map)

"""
Now we have our map defined and GraphProblems we can evaluate the running of 
different uninformed search approaches against them. There are two functions of
interest from search.py:
    
    compare_searchers - Takes an array of the uninformed search strategies that
    you are interested in comparing - this will have to be overwritten as 
    default in RBFS.
    
    compare_graph_searchers - Takes in an array of problems and runs it against
    the battery of search strategies. We will reimplement this below. 

It takes an array of problems, we will use one for now. Note: we have added an 
argument to define searchers array to compare_searchers will allows us omit 
RBFS (included in default) and enables us compare a selection of uninformed 
search strategies as we see fit.
"""

def compare_graph_searchers(uninformed_searchers):
    """Prints a table of search results."""
    outputString = 'Actions/Goal Tests/States/Goal\n'
    print(outputString)
    compare_searchers(problems=[cork_To_Dublin_problem, rosslare_To_Letterkenny_problem, limerick_To_Belfast_problem], header=['Searcher', 'ireland_map(Cork, Dublin)','ireland_map(Rosslare, Letterkenny)', 'ireland_map(Limerick, Belfast)'], searchers=uninformed_searchers)


searchers=[breadth_first_tree_search, 
#           depth_first_tree_search,
           breadth_first_graph_search,
           depth_first_graph_search,
           iterative_deepening_search,
           depth_limited_search]
    
compare_graph_searchers(searchers)

"""
To understand this we should look at the InstrumentedProblem(Problem) class
from search.py - particularly the variables that make up the statistics.

<Review the superclass Problem, and the subclasses GraphProblem and InstrumentedProblem>

Python __repr__() function returns the object representation. It could be
any valid python expression such as tuple, dictionary, string etc. This method 
is called when repr() function is invoked on the object, in that case, 
__repr__() function must return a String otherwise error will be thrown.

At present InstrumentedProblem returns self.succs, self.goal_tests, self.states
and self.found

self.succs - intially 0, incremented based on actions => invokes super.actions,
returns the actions that can be executed in the given state. The result 
would typically be a list. This value indicates the no. of times the set of 
admissable actions were returned for a node.

self.goal_tests, intially 0, incremented based on no. of goal tests performed.

self.states, intially 0, return the state that results from executing the given
action in the given state. The action must be one of  self.actions(state).

str(self.found) - whether the goal has been found or not
"""

"""
Remember how we measure problem-solving performance? 
Completeness: Is the algorithm guaranteed to find a solution when there is one?
Optimality: Does the strategy find the optimal solution? 
Time complexity: How long does it take to find a solution? 
Space complexity: How much memory is needed to perform the search?

In AI, the graph is often represented implicitly by the initial state, actions, and transition model and is frequently infinite.
Complexity is expressed in terms of three quantities:
b, the branching factor or maximum number of successors of any node.
d, the depth of the shallowest goal node (i.e., the number of steps along the path from the root). 
m, the maximum length of any path in the state space. 
Time is often measured in terms of the number of nodes generated during the search, and space in terms of the maximum number of nodes stored in memory.


############RESULTS############

Searcher                    ireland_map(Cork, Dublin)   ireland_map(Rosslare, Letterkenny)   ireland_map(Limerick, Belfast)
                            Path (d) /Goal Tests/States (No. of nodes generated - time)/ Goal Found

depth_first_tree_search      <incomplete due to loopy path, resulted in infinite loop, ran out of memory.
breadth_first_tree_search    <  32/  33/  93/Dubl>       < 483/ 484/1337/Lett>                <  37/  38/ 105/Belf>         

breadth_first_graph_search   <   7/  10/  18/Dubl>       <  14/  16/  34/Lett>                <   7/  13/  21/Belf>         
depth_first_graph_search     <   4/   5/  12/Dubl>       <   9/  10/  23/Lett>                <   4/   5/  12/Belf>         

iterative_deepening_search   <  17/  50/  48/Dubl>       < 300/ 784/ 777/Lett>                <  17/  55/  54/Belf>         
depth_limited_search         <  63/  90/ 160/Dubl>       < 157/ 349/ 416/Lett>                <  90/ 156/ 227/Belf>     


breadth_first_tree_search -
breadth_first_graph_search -

depth_first_graph_search -
iterative_deepening_search
depth_limited_search - 

bidirectional_search - ? 

"""


""""
QC - Missionaries and Cannibals - Uninformed search


> Formulate the problem precisely, making only those distinctions necessary to ensure a valid solution. Draw a diagram of the complete state space.
> Implement and solve the problem optimally using an appropriate search algorithm. Is it a good idea to check for repeated states?
> Why do you think people have a hard time solving this puzzle, given that the state space is so simple?


SOLUTION
1. Define the state.
2. Define valid actions and state transitions.
3. Implement the problem as a subclass of Problem from search.py.
4. Solve the problem using an appropriate search algorithm.



Problem Statement:
Three missionaries and three cannibals must cross a river using a boat which can carry at most two people, under the constraint that, for both banks, if there are missionaries present on the bank, they cannot be outnumbered by cannibals (if they were, the cannibals would eat the missionaries). The boat cannot cross the river by itself with no people on board.

    State Definition:
    A state can be represented as a tuple (M, C, B), where:

    M is the number of missionaries on the left bank.
    C is the number of cannibals on the left bank.
    B is the position of the boat (1 if it's on the left bank, 0 if it's on the right bank).

    Actions and State Transitions:
    For each state (M, C, B), the valid actions would be to move 1 or 2 missionaries or cannibals across the river, depending on the position of the boat.

Here's an implementation of the problem:

"""


from search import Problem, breadth_first_tree_search

class MissionariesAndCannibals(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def actions(self, state):
        M, C, B = state
        if B == 1:  # Boat is on the left bank
            possible_actions = [(-1, 0), (-2, 0), (0, -1), (0, -2), (-1, -1)]
        else:  # Boat is on the right bank
            possible_actions = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        return [action for action in possible_actions if self.is_valid(state, action)]

    def is_valid(self, state, action):
        M, C, B = state
        dM, dC = action
        # Check if resulting state is valid
        if 0 <= M + dM <= 3 and 0 <= C + dC <= 3 and ((M + dM >= C + dC) or (M + dM == 0)):
            M_other, C_other = 3 - M - dM, 3 - C - dC
            return (M_other >= C_other or M_other == 0)
        return False

    def result(self, state, action):
        M, C, B = state
        dM, dC = action
        return (M + dM, C + dC, 1 - B)

    def goal_test(self, state):
        return state == self.goal


# Solve the problem
initial_state = (3, 3, 1)
goal_state = (0, 0, 0)
problem = MissionariesAndCannibals(initial_state, goal_state)
solution = breadth_first_tree_search(problem)
if solution:
    print("Found solution:", solution.solution())
else:
    print("No solution found.")
