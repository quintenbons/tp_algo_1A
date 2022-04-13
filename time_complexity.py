#!/usr/bin/env python3
# Imports
from geo.point import Point
from time import time
from random import random
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys, os
import student.naive.solution as naive
import student.tree.solution as tree
import student.tree_no_sort.solution as tree_no_sort
import student.tree_functional.solution as tree_functional
import student.tree_functional_no_sort.solution as tree_functional_no_sort
import student.randomized.solution as randomized

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

def plot_data(data):
    """
    pyplot magic
    """
    [X, naive_time, tree_no_sort_time, tree_time, tree_functional_time, tree_functional_no_sort_time, randomized_time] = data

    plt.plot(X, naive_time, label="naive", color="blue")
    plt.plot(X, tree_no_sort_time, label="tree_no_sort", color="orange")
    plt.plot(X, tree_time, label="tree", color="magenta")
    plt.plot(X, tree_functional_time, label="tree_functional", color="red")
    plt.plot(X, tree_functional_no_sort_time, label="tree_functional_no_sort", color="green")
    plt.plot(X, randomized_time, label="randomized", color="cyan")
    plt.legend()
    plt.show()

def measure_and_save():
    """
    Compare les durees d'execution des differentes
    solutions. Le but est d'avoir une idee de la
    complexite en fonction d'un graphe de perf

    J'en profite aussi pour compter le nombre de
    noeuds sur lesquels on passe avec chaque
    methode kd-tree.
    """
    X = np.linspace(MIN_POINTS, MAX_POINTS, SAMPLE_SIZE, dtype="i")

    count_tree = 0
    count_tree_no_sort = 0

    naive_time = np.zeros(len(X))
    tree_no_sort_time = np.zeros(len(X))
    tree_time = np.zeros(len(X))
    tree_functional_time = np.zeros(len(X))
    tree_functional_no_sort_time = np.zeros(len(X))
    randomized_time = np.zeros(len(X))

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

            temp = time();
            tree_functional.get_closest(points)
            tree_functional_time[i] += time() - temp

            temp = time();
            tree_functional_no_sort.get_closest(points)
            tree_functional_no_sort_time[i] += time() - temp

            temp = time();
            randomized.get_closest(points)
            randomized_time[i] += time() - temp


        # on n'oublie pas de rediviser
        naive_time[i] /= TEST_REPEAT
        tree_no_sort_time[i] /= TEST_REPEAT
        tree_time[i] /= TEST_REPEAT
        tree_functional_time[i] /= TEST_REPEAT
        tree_functional_no_sort_time[i] /= TEST_REPEAT
        randomized_time[i] /= TEST_REPEAT


    # on affiche le nombre de points comptes par get_closest
    print(count_tree)
    print(count_tree_no_sort)

    # On remete le stdout qui va bien, sans oublier de fermer /dev/null
    sys.stdout.close
    sys.stdout = old_stdout

    data = [X, naive_time, tree_no_sort_time, tree_time, tree_functional_time, tree_functional_no_sort_time, randomized_time]

    plot_data(data)

    save(data)

def save(data, ext=''):
    """
    Sauvegarde avec pickle
    """
    filepath = f"./data/perf{'' if ext == '' else '-' + ext}"
    with open(filepath, "wb") as f:
        pickle.dump(data, f)

def load(ext=''):
    """
    Chargement avec pickle
    """
    filepath = f"./data/perf{'' if ext == '' else '-' + ext}"
    # with se chargera de fermer f avant le return
    with open(filepath, "rb") as f:
        return pickle.load(f)

def main():
    """
    Verifie les options
    par defaut: mesure la complexite et sauvegarde
    charger et afficher: -l [ext]
    """
    if len(sys.argv) > 1 and sys.argv[1] == "-l":
        ext = ''
        if len(sys.argv) > 2:
            ext = sys.argv[2]

        data = load(ext)
        plot_data(data)

    else:
        measure_and_save()

if __name__ == "__main__":
    main()
