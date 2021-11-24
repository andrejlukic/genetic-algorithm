from random import random, randint, shuffle, choices
from EightQueensState import *


class EightQueensPopulation:
    """This class represents a generation of puzzle game states"""

    def __init__(self, queen_count, population=None, size=None, generation=0):
        """
        If no population is passed at init the population will be created based
        on the size parameter.

        :param state: pass in a list of EightQueensState objects
        """
        if not population:
            self._pop = []
            if size:
                for i in range(size):
                    self._pop.append(EightQueensState(queen_count))

        else:
            self._pop = population
        self._gen = generation
        self.n = queen_count
        self._log = []

    def print_state(self, dump_pop=False, dump_log=False):
        """
        Prints debug output

        :param dump_pop: prints the whole population
        :param dump_log: prints the step log including parents, mutations
        """
        avg_fit = sum([i.fitness() for i in self._pop]) / len(self._pop)
        probs = self.probabilities()
        print("Generation {}, avg fit {}".format(self._gen, avg_fit))
        if dump_pop:
            for i in range(len(self._pop)):
                print("{}, {}".format(self._pop[i], probs[i] * 100))
        if dump_log:
            for t in self._log:
                if len(t) == 4:
                    print("{} + {} at {} = {}".format(t[0], t[1], t[2], t[3]))
                elif len(t) == 1:
                    print("Mutated to {}".format(t[0]))

    def grow(self, i):
        """Adds DNA to the population"""
        self._pop.append(i)

    def size(self):
        """Returns the size of population"""
        return len(self._pop)

    @staticmethod
    def norm(data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    def max_fitness(self):
        """Returns the maximum fitness score"""
        return (self.n * (self.n - 1)) / 2

    def probabilities(self):
        # fit_sum = sum([i.fitness() for i in self._pop])
        # normalized = EightQueensPopulation.norm(np.array([i.fitness()/fit_sum for i in self._pop])).tolist()
        # return [(p, i) for p, i in zip(normalized, self._pop)]
        return [i.fitness() / self.max_fitness() for i in self._pop]

    def cull(self, candidates, cutoff=0.2):
        """Cull worst solutions out of population"""
        return [(p, i) for p, i in candidates if p >= cutoff]

    def pick_n(self, n=2):
        """Random weighted pick from the population"""
        return choices(self._pop, weights=[i.fitness() for i in self._pop], k=n)

    def log(self, t):
        self._log.append(t)

    def offspring_V1(self, parents):
        """Create a new DNA by merging two parents' DNA codes at random point"""
        n = len(parents[0].state)
        inx = randint(0, n)
        left = parents[0].state.copy()[0:inx]
        right = parents[1].state.copy()[inx:n]
        return EightQueensState(self.n, state=np.concatenate([left, right])), inx

    def offspring_V2(self, parents):
        """Create a new DNA by merging two parents' DNA codes at random point.
           Take the better child"""
        n = len(parents[0].state)

        bestbaby = None
        bestinx = 0
        for tries in range(1):
            inx = randint(0, n)
            # baby 1
            left1 = parents[0].state.copy()[0:inx]
            right1 = parents[1].state.copy()[inx:n]
            b1 = EightQueensState(self.n, state=np.concatenate([left1, right1]))
            # baby 2
            left2 = parents[1].state.copy()[0:inx]
            right2 = parents[0].state.copy()[inx:n]
            b2 = EightQueensState(self.n, state=np.concatenate([left2, right2]))
            # return the better baby
            bestinx=inx
            if b1.fitness() <= b2.fitness():
                if not bestbaby or b2.fitness() > bestbaby.fitness():
                    bestbaby = b2
            else:
                if not bestbaby or b1.fitness() > bestbaby.fitness():
                    bestbaby = b1

        return bestbaby, bestinx

    def culling(self, percent=0.8, elite=None):
        """Remove X% of the least fit from the list based on fitness score"""
        l = sorted(self._pop, key=lambda x: x.fitness(), reverse=True)
        take = int(percent*len(l))
        l = l[:take]
        if elite:
            l.extend(elite)
        shuffle(l)
        self._pop = l

    def get_elite(self, percent=0.05):
        """Return top X% individuals based on the fitness score"""
        l = sorted(self._pop, key=lambda x: x.fitness(), reverse=True)
        take = int(percent*len(l))
        return l[:take]

