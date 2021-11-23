import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
from random import random, randint, shuffle
from EightQueensPopulation import *

N = 8  # number of queens
N_POPULATION = 100  # size of population
P_MUTATION = 0.03  # probability of mutation

def addstats(data, val):
    if not data is None:
        data.append([i.fitness() for i in val._pop])

def genetic_algo(stdata=None):
    gen_i = 0  # Generation count
    old_gen = EightQueensPopulation(N, size=N_POPULATION, generation=gen_i)

    not_found = True
    while not_found:
        addstats(stdata, old_gen)
        next_gen = EightQueensPopulation(N, generation=gen_i + 1)

        for i in range(N_POPULATION):

            parents = old_gen.pick_n(culling=False)
            baby, inx = next_gen.offspring(parents)

            next_gen.log((parents[0], parents[1], inx, baby))

            if random() < P_MUTATION:
                baby, inx = baby.mutate()
                next_gen.log((baby, inx))

            if (next_gen.size() < old_gen.size()):
                next_gen.grow(baby)

            not_found = not baby.is_goal()

            if not not_found:
                # Found solution:
                print(baby)
                break
        old_gen = next_gen
        gen_i += 1
        # old_gen.print_state(dump_pop=False)


def vis_stats(stdata):
    print("Number of generations: ", len(stdata))
    sns.set_theme(style="whitegrid")

    x = []
    y1 = []
    y2 = []
    y3 = []

    for i in range(len(stdata)):
        l = stdata[i]
        x.append(i)
        y1.append(min(l))
        y2.append(sum(l) / len(l))
        y3.append(max(l))

    d = {'x': np.array(x), 'y1': np.array(y1), 'y2': np.array(y2), 'y3': np.array(y3)}
    df = pd.DataFrame(d)
    # print(df)


    g = sns.FacetGrid(df["x"], height=8, aspect=2)
    g.map(sns.lineplot, x=df["x"], y=df["y1"], color="lightblue")
    g.map(sns.lineplot, x=df["x"], y=df["y2"], color='red')
    g.map(sns.lineplot, x=df["x"], y=df["y3"], color='lightgreen')
    plt.show()

def stats():
    Nruns = 10 # number of runs
    print("Running a test of {}".format(Nruns))
    print("Queens {}".format(N))
    print("Population {}".format(N_POPULATION))
    print("P mutation {}".format(P_MUTATION))

    results = {}
    for i in range(Nruns):
        print("Run ", i)
        statsdata = []
        start = time.time()
        genetic_algo(stdata=statsdata)
        end = time.time()
        print("Done in {} seconds ".format(end-start))
        results[i] = statsdata

    for key, s in results.items():
        vis_stats(s)

stats()