"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors
import random 
import math

class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Hill Climbing optimization.

        Guidelines:
        - Search through the neighborhood greedily for candidates that minimize total travel time.
        - Handle flat local maxima / shoulders by allowing up to `max_sideways` non-improving steps.
        - Apply up to `max_restarts` to explore different starting basins.
        - Track the best objective cost seen at each major step in self.history.

        Prohibited:
        - Looping indefinitely on flat plateaus.
        """
        
        eps = 1e-9
        self.history = []
        best_state = self.problem.generate_initial_state()
        best_cost = self.problem.evaluate(best_state)
        for i in range(self.max_restarts + 1):
            current = self.problem.generate_initial_state()
            if i > 0:
                current = State(current.path, random.choice(self.problem.get_valid_time_domain()))
            currentcost = self.problem.evaluate(current)
            sideways = 0
            visited = {current}
            self.history.append(best_cost)
            while True:
                neighbors = get_neighbors(current, self.problem)
                if not neighbors:
                    break
                lowestcostneighbor = []
                lowest = float('inf')
                for j in range(len(neighbors)):
                    cost = self.problem.evaluate(neighbors[j])
                    lowestcostneighbor.append((cost, neighbors[j]))
                    if cost < lowest:
                        lowest = cost
                if lowest < currentcost - eps:
                    current = random.choice([s for c, s in lowestcostneighbor if abs(c - lowest) <= eps])
                    currentcost = lowest
                    sideways = 0
                    visited = {current}
                elif abs(lowest - currentcost) <= eps and sideways < self.max_sideways:
                    candidates = [s for c, s in lowestcostneighbor
                                  if abs(c - currentcost) <= eps and s not in visited]
                    if not candidates:
                        break
                    current = random.choice(candidates)
                    visited.add(current)
                    sideways += 1
                else:
                    break 
                if currentcost < best_cost:
                    best_state, best_cost = current, currentcost
                self.history.append(best_cost)
        return best_state, best_cost
                    
                 




        # TODO: Implement Hill Climbing with sideways moves and restarts
        raise NotImplementedError("Implement solve() in algorithms/hill_climbing.py")
