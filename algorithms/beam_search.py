"""
algorithms/beam_search.py
Local Beam Search maintaining K parallel candidate states.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class LocalBeamSearchSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.beam_width: int = self.params.get("beam_width", 5)
        self.max_iterations: int = self.params.get("max_iterations", 150)
        self.patience: int = self.params.get("patience", 5)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Local Beam Search.

        Guidelines:
        - Maintain a set of `beam_width` parallel configurations.
        - In each iteration, generate neighbors from all active states in the beam.
        - Pool and rank all generated successors collectively, then retain the top `beam_width` states.
        - Halt when the beam ceases to improve or reaches max_iterations.
        - Record the best cost of the population at each step in self.history.

        Encouraged:
        - Ensuring diversity across states in the beam to prevent collapse into a single redundant path.

        Prohibited:
        - Treating this as K independent, non-communicating searches.
        """
        self.history = []
        beststate = self.problem.generate_initial_state()
        bestcost = self.problem.evaluate(beststate)
        self.history.append(bestcost)
        noimprove = 0
        iteration = 0
        beam = [beststate]                                 
        while len(beam) > 0 and iteration < self.max_iterations:   
            candidates = []                                 
            for i in range(len(beam)):                      
                neighbors = get_neighbors(beam[i], self.problem)      
                for j in range(len(neighbors)):           
                    if neighbors[j] not in candidates:
                        candidates.append(neighbors[j])

            scored = []
            for i in range(len(candidates)):
                scored.append((self.problem.evaluate(candidates[i]), candidates[i]))
            scored.sort(key=lambda x: x[0])

            beam = []                                      
            for i in range(min(self.beam_width, len(scored))):
                beam.append(scored[i][1])

            if len(scored) > 0 and scored[0][0] < bestcost:
                bestcost, beststate = scored[0][0], scored[0][1]
                noimprove = 0
            else:
                noimprove += 1
            self.history.append(bestcost)
            if noimprove >= self.patience:
                break
            iteration += 1

        return beststate, bestcost
        # TODO: Implement Local Beam Search
        # raise NotImplementedError("Implement solve() in algorithms/beam_search.py")
