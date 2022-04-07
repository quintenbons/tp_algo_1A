#!/usr/bin/env python3
# Imports
from geo.point import Point
from time import time
from random import random
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import student.naive.solution as naive
import student.tree.solution as tree
import student.tree_no_sort.solution as tree_no_sort

# Constants
MIN_POINTS = 10
MAX_POINTS = 300
SAMPLE_SIZE = 10 # automatic linspace
TEST_REPEAT = 20 # number of repeats (uniformize)


def generate_point_sample(number):
    """
    Genere un tableau de points (a manger pour
    les fonctions get_closest des solutions)
    """
    points = [Point((random(), random())) for _ in range(number)]
    return points

def main():
    """
    Compare les durees d'execution des differentes
    solutions. Le but est d'avoir une idee de la
    complexite en fonction d'un graphe de perf
    """
    X = np.linspace(MIN_POINTS, MAX_POINTS, SAMPLE_SIZE, dtype="i")

    naive_time = np.zeros(len(X))
    tree_no_sort_time = np.zeros(len(X))
    tree_time = np.zeros(len(X))

    # On mute l'output pendant les tests
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    for i in range(len(X)):
        print(f"Starting test {i} with {X[i]} points.", file=old_stdout)
        # on teste sur le meme sample de points
        # sur toutes les solutions
        for _ in range(TEST_REPEAT):
            points = generate_point_sample(X[i])

            temp = time();
            naive.get_closest(points)
            naive_time[i] += time() - temp

            temp = time();
            tree_no_sort.get_closest(points)
            tree_no_sort_time[i] += time() - temp

            temp = time();
            tree.get_closest(points)
            tree_time[i] += time() - temp


        # on n'oublie pas de rediviser
        naive_time[i] /= TEST_REPEAT
        tree_no_sort_time[i] /= TEST_REPEAT
        tree_time[i] /= TEST_REPEAT


    # On remete le stdout qui va bien, sans oublier de fermer /dev/null
    sys.stdout.close
    sys.stdout = old_stdout

    plt.plot(X, naive_time, label="naive")
    plt.plot(X, tree_no_sort_time, label="tree_no_sort")
    plt.plot(X, tree_time, label="tree")
    plt.legend()
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
