"""
algorithms/simulated_annealing.py
Stochastic optimization governed by a temperature schedule.
"""

import math
import random
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class SimulatedAnnealingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.initial_temp: float = self.params.get("initial_temp", 100.0)
        self.cooling_rate: float = self.params.get("cooling_rate", 0.995)
        self.min_temp: float = self.params.get("min_temp", 1e-3)
        self.max_iterations: int = self.params.get("max_iterations", 2000)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Simulated Annealing optimization.

        Guidelines:
        - Start from a high temperature where worse moves are accepted with significant probability.
        - Lower temperature over iterations according to a cooling schedule.
        - Downhill moves (improvements) must always be accepted.
        - Uphill moves (worse costs) should be accepted probabilistically according to temperature.
        - Record objective values throughout the run in self.history.

        Prohibited:
        - Ignoring the temperature parameter or turning this into pure hill climbing.
        """
        current = self.problem.generate_initial_state()
        current_temprature = self.initial_temp
        infinity = self.max_iterations
        self.history = []
        visited = [(current_cost, current)]
        for i in range(infinity):
            current_temprature *= self.cooling_rate
            if current_temprature < self.min_temp:
                break

            neighbors = get_neighbors(current, self.problem)
            if not neighbors:
                break
            next_state = random.choice(neighbors)
            current_cost = self.problem.evaluate(current)
            next_cost = self.problem.evaluate(next_state)
            delta_cost = next_cost - current_cost
            if delta_cost < 0:
                current = next_state
            else:
                acceptance_probability = math.exp(-delta_cost / current_temprature)
                if random.random() < acceptance_probability:
                    current = next_state
            visited.append((current_cost, current))
            self.history.append(self.problem.evaluate(current))
        visited.sort(key=lambda x: x[0])
        return visited[0][1], visited[0][0]
        # TODO: Implement Simulated Annealing
        raise NotImplementedError("Implement solve() in algorithms/simulated_annealing.py")
