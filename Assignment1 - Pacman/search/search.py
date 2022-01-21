# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from random import choice

import util
from game import Actions, Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def randomSearch(problem):
    current_state = problem.getStartState()
    solution = []
    while not (problem.isGoalState(current_state)):
        successors = problem.getSuccessors(current_state)
        next_state = choice(successors)  # randomly chooses an element from successors list
        current_state = next_state[0]
        solution.append(next_state[1])
    # print "Solution: ", solution
    return solution


def getSuccessorsWithoutReverse(successors, curr_dir):
    rev_dir = Actions.reverseDirection(curr_dir)
    reverseSuccessor = None
    for successor in successors:
        nextAction = successor[1]
        if rev_dir == nextAction:  # i am trying to not go in the opposite direction
            reverseSuccessor = successor
    if reverseSuccessor is not None:
        successors.remove(reverseSuccessor)
    return successors


def mouseSearch(problem):
    from game import Directions
    current_state = problem.getStartState()
    solution = []
    curr_dir = Directions.EAST
    while not (problem.isGoalState(current_state)):
        successors = problem.getSuccessors(current_state)
        if len(successors) >= 2:  # i am at a junction
            successorsWithoutReverse = getSuccessorsWithoutReverse(successors, curr_dir)  # i dont want to go back
            nextState = choice(successorsWithoutReverse)  # i will choose a random move
        elif len(successors) == 2:  # i am at a passageway
            keepDirectionSuccessor = getSuccessorsWithoutReverse(successors, curr_dir)
            nextState = keepDirectionSuccessor[0]  # since reverse is removed, there is only one option left
        else:  # dead end
            nextState = successors[0]  # the only option left is going back
        current_state = nextState[0]
        curr_dir = nextState[1]
        solution.append(curr_dir)
    return solution


def desiredAction(action, hand):
    if hand == "left":
        if action == Directions.WEST:
            return Directions.SOUTH
        elif action == Directions.SOUTH:
            return Directions.EAST
        elif action == Directions.EAST:
            return Directions.NORTH
        else:
            return Directions.WEST
    else:
        if action == Directions.WEST:
            return Directions.NORTH
        elif action == Directions.NORTH:
            return Directions.EAST
        elif action == Directions.EAST:
            return Directions.SOUTH
        else:
            return Directions.WEST


def getDesiredSuccessor(successors, curr_dir, hand):
    desired_dir = desiredAction(curr_dir, hand)
    desiredSuccessor = None
    for successor in successors:
        nextAction = successor[1]
        if desired_dir == nextAction:  # i am looking for the successor with the desired action
            desiredSuccessor = successor
    return desiredSuccessor


def getKeepDirectionSuccessor(successors, curr_dir):  # assumes there are more than or 2 successors,
    # and the desired action is not possible
    keepDirSuccessor = None
    reverseSuccessor = None
    rev_dir = Actions.reverseDirection(curr_dir)
    for successor in successors:
        nextAction = successor[1]
        if curr_dir == nextAction:  # successor that keeps my direction
            keepDirSuccessor = successor
        if rev_dir == nextAction:  # i am trying to not go in the opposite direction
            reverseSuccessor = successor
    if reverseSuccessor is not None:  # since there is more than one successor i dont need this
        successors.remove(reverseSuccessor)
    if keepDirSuccessor is not None:
        return keepDirSuccessor
    return successors[0]  # in case there is no keep dir successor there is only one left successor


def wallFlowerSearch(problem):
    current_state = problem.getStartState()
    solution = []
    curr_dir = Directions.NORTH
    hand = "left"
    while not (problem.isGoalState(current_state)):
        successors = problem.getSuccessors(current_state)
        if len(successors) >= 2:  # keep going forward
            desiredSuccessor = getDesiredSuccessor(successors, curr_dir, hand)
            if desiredSuccessor is not None:
                nextState = desiredSuccessor
            else:
                nextState = getKeepDirectionSuccessor(successors, curr_dir)
        else:  # dead end
            nextState = successors[0]
        current_state = nextState[0]
        curr_dir = nextState[1]
        solution.append(curr_dir)
    return solution


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    exploredStates = []
    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return []
    frontier.push((initial_state, [], 0))
    while not frontier.isEmpty():
        currentState, currentActions, currentCost = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)
            if problem.isGoalState(currentState):
                return currentActions
            for nextState, nextAction, nextCost in problem.getSuccessors(currentState):
                newActions = currentActions + [nextAction]
                newCost = currentCost + nextCost
                frontier.push((nextState, newActions, newCost))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    exploredStates = []
    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return []
    frontier.push((initial_state, [], 0))
    while not frontier.isEmpty():
        currentState, currentActions, currentCost = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)
            if problem.isGoalState(currentState):
                return currentActions
            for nextState, nextAction, nextCost in problem.getSuccessors(currentState):
                newActions = currentActions + [nextAction]
                newCost = currentCost + nextCost
                frontier.push((nextState, newActions, newCost))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    exploredStates = []
    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return []
    frontier.push((initial_state, [], 0), 0)
    while not frontier.isEmpty():
        currentState, currentActions, currentCost = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)
            if problem.isGoalState(currentState):
                return currentActions
            for nextState, nextAction, nextCost in problem.getSuccessors(currentState):
                newActions = currentActions + [nextAction]
                newCost = currentCost + nextCost
                frontier.push((nextState, newActions, newCost), newCost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def greedySearch(problem, heuristic=nullHeuristic):
    frontier = util.PriorityQueue()
    exploredStates = []
    initial_state = problem.getStartState()
    start_heuristic = heuristic(initial_state, problem)
    if problem.isGoalState(initial_state):
        return []
    frontier.push((initial_state, [], 0), start_heuristic)
    while not frontier.isEmpty():
        currentState, currentActions, currentCost = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)
            if problem.isGoalState(currentState):
                return currentActions
            for nextState, nextAction, nextCost in problem.getSuccessors(currentState):
                newActions = currentActions + [nextAction]
                getHeuristics = heuristic(nextState, problem)
                frontier.push((nextState, newActions, nextCost), getHeuristics)


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    exploredStates = []
    initial_state = problem.getStartState()
    start_heuristic = heuristic(initial_state, problem)
    if problem.isGoalState(initial_state):
        return []
    frontier.push((initial_state, [], 0), start_heuristic)
    while not frontier.isEmpty():
        currentState, currentActions, currentCost = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)
            if problem.isGoalState(currentState):
                return currentActions
            for nextState, nextAction, nextCost in problem.getSuccessors(currentState):
                newActions = currentActions + [nextAction]
                newCost = currentCost + nextCost
                getHeuristics = heuristic(nextState, problem)
                frontier.push((nextState, newActions, newCost), newCost + getHeuristics)


def getOppositeDirections(directions):
    oppositeDirections = []
    for direction in directions:
        if direction == Directions.NORTH:
            oppositeDirections.append(Directions.SOUTH)
        elif direction == Directions.SOUTH:
            oppositeDirections.append(Directions.NORTH)
        elif direction == Directions.WEST:
            oppositeDirections.append(Directions.EAST)
        else:
            oppositeDirections.append(Directions.WEST)
    return oppositeDirections


def bidirectionalSearch(problem, heuristic=nullHeuristic):
    startFrontier = util.PriorityQueue()
    goalFrontier = util.PriorityQueue()
    allStatesInStartFrontier = set()  # to visualize the nodes in the frontier
    allStatesInGoalFrontier = set()
    exploredStatesByStart = []
    exploredStatesByGoal = []
    initial_state = problem.getStartState()
    end_state = problem.goal
    start_heuristic = heuristic(initial_state, problem)
    goal_heuristic = heuristic(end_state, problem)
    startFrontier.push((initial_state, []), start_heuristic)
    goalFrontier.push((end_state, []), goal_heuristic)

    while startFrontier.isEmpty() is not True and goalFrontier.isEmpty() is not True:
        if startFrontier.isEmpty() is not True:  # this is the search that starts from the start
            currentState, currentActions = startFrontier.pop()
            if currentState not in exploredStatesByStart:
                exploredStatesByStart.append(currentState)
                if problem.isGoalState(currentState):
                    print "did not meet"
                    return currentActions
                if currentState in allStatesInGoalFrontier:  # this means we found a common path
                    while not goalFrontier.isEmpty():
                        current_state, current_actions = goalFrontier.pop()
                        if current_state == currentState:
                            current_actions.reverse()  # we have to reverse the states that come from the search
                            # that was performed from goal to start
                            solution = currentActions + getOppositeDirections(current_actions)  # this states specify
                            # how the pacman should move from the goal to the meeting point sa we have to
                            # also reverse the actions(directions) inside the states
                            return solution
                for (nextState, nextAction, nextCost) in problem.getSuccessors(currentState):
                    # if common path not met, continue searching
                    getHeuristics = heuristic(nextState, problem)
                    # this is greedy searching but it can be bfs if no heuristic is given
                    startFrontier.push((nextState, currentActions + [nextAction]), getHeuristics)
                    allStatesInStartFrontier.add(nextState)

        if goalFrontier.isEmpty() is not True:  # this is the search that starts from the goal
            currentState, currentActions = goalFrontier.pop()
            if currentState not in exploredStatesByGoal:
                exploredStatesByGoal.append(currentState)
                if currentState == initial_state:
                    print "did not meet"
                    currentActions.reverse()
                    return getOppositeDirections(currentActions)
                if currentState in allStatesInStartFrontier:
                    while not startFrontier.isEmpty():
                        current_state, current_actions = startFrontier.pop()
                        if current_state == currentState:
                            currentActions.reverse()
                            solution = current_actions + getOppositeDirections(currentActions)
                            return solution
                for (nextState, nextAction, nextCost) in problem.getSuccessors(currentState):
                    getHeuristics = heuristic(nextState, problem)
                    goalFrontier.push((nextState, currentActions + [nextAction]), getHeuristics)
                    allStatesInGoalFrontier.add(nextState)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
mouse = mouseSearch
wall = wallFlowerSearch
bi = bidirectionalSearch
greedy = greedySearch
