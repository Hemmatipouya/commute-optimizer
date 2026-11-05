"""
algorithms/genetic_algorithm.py
Population-based optimization using selection, recombination, and mutation.
"""

import random
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, crossover


class GeneticAlgorithmSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.population_size: int = self.params.get("population_size", 30)
        self.generations: int = self.params.get("generations", 100)
        self.crossover_rate: float = self.params.get("crossover_rate", 0.8)
        self.mutation_rate: float = self.params.get("mutation_rate", 0.2)
        self.elitism: int = self.params.get("elitism", 2)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Genetic Algorithm optimization.

        Guidelines:
        - Initialize a population of valid candidate solutions.
        - Design a fitness metric suitable for minimizing commute travel time (lower cost -> higher fitness).
        - Use selection operators (such as tournament or roulette selection) to pick parents.
        - Pair parents to produce offspring via `crossover()`, and apply stochastic mutation.
        - Preserve the top candidates across generations if using elitism.
        - Track best population performance per generation in self.history.

        Encouraged:
        - Experimenting with population size, selection pressure, and operator rates to balance exploration vs. exploitation.
        """
        self.history = []
        self.population =[]
        domain = self.problem.get_valid_time_domain()
        for i in range(self.population_size):
            sibling = self.problem.generate_initial_state()
            sibling = State(sibling.path, random.choice(self.problem.get_valid_time_domain()))
            randomint = random.randint(0,15)
            for _ in range(randomint):
                sibling = random.choice(get_neighbors(sibling,self.problem))
            self.population.append(sibling)
        childrenandcosts : list[Tuple] = []
        for i in range(self.population_size):
            childrenandcosts.append((self.problem.evaluate(self.population[i]),self.population[i]))
        childrenandcosts.sort( key=lambda  x :  x[0])
        def fitness(a:float)->float:
            return 1/(1+a)
        def tournament():
            group = random.sample(childrenandcosts, 3)
            return min(group, key=lambda x: x[0])[1]
        beststate = childrenandcosts[0][1]
        bestcost = childrenandcosts[0][0]
        self.history.append(bestcost)
        for generation in range(self.generations):
            new_generation = []
            for i in range (self.elitism):
                new_generation.append(childrenandcosts[i][1])
            while len(new_generation) < self.population_size:
                parent1= tournament()
                parent2 = tournament()
                if random.random() < self.crossover_rate:
                    child = crossover(parent1, parent2, self.problem)
                else:
                    child = parent1
                if random.random() < self.mutation_rate:
                    neighbors = get_neighbors(child, self.problem)
                    if neighbors:
                        child = random.choice(neighbors)
                new_generation.append(child)
            childrenandcosts = []
            for i in range(len(new_generation)):
                childrenandcosts.append((self.problem.evaluate(new_generation[i]), new_generation[i]))
            childrenandcosts.sort(key=lambda x: x[0])
            if childrenandcosts[0][0] < bestcost:
                bestcost = childrenandcosts[0][0]
                beststate = childrenandcosts[0][1]
            self.history.append(bestcost)
                




        
        # TODO: Implement Genetic Algorithm
        return beststate, bestcost
        # raise NotImplementedError("Implement solve() in algorithms/genetic_algorithm.py")
