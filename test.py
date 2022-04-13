#!/usr/bin/env python3
# Imports
from student.utils import generate_point_sample, print_array, distance2, dichotomy_insert
from geo.point import Point
from geo.segment import Segment
from geo.tycat import tycat
from time import time
from random import random
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import student.naive.solution as naive
import student.tree_no_sort.solution as tree_no_sort
import student.tree.solution as tree
import student.tree_functional.solution as tree_functional
import student.tree_functional_no_sort.solution as tree_functional_no_sort
import student.randomized.solution as randomized

from main import main as realmain

# Constants
MINIMUM_POINTS = 10
POINT_NUMBER = 50
TEST_NUMBER = 100
DEBUGGING = True # Only for deep debugging


def is_sorted(points, axis):
    """
    Renvoie True si points est trie selon
    l'axe
    """
    return all(points[i].coordinates[axis] < points[i+1].coordinates[axis] for i in range(len(points)-1))

def test_dicho_insert():
    """
    Fait des tests simples de tri
    """
    points = generate_point_sample(MINIMUM_POINTS)
    [point] = generate_point_sample(1)

    sorted_points_x = sorted(points, key=lambda p: p.coordinates[0])
    sorted_points_y = sorted(points, key=lambda p: p.coordinates[1])

    print(f"DEBUG === sorted x")
    print_array(sorted_points_x)
    print(f"DEBUG === adding {point}")
    dichotomy_insert(point, sorted_points_x, False)
    print_array(sorted_points_x)
    print()
    print(f"DEBUG === sorted y")
    print_array(sorted_points_y)
    print(f"DEBUG === adding {point}")
    dichotomy_insert(point, sorted_points_y, True)
    print_array(sorted_points_y)

    if not (is_sorted(sorted_points_x, False) and is_sorted(sorted_points_y, True)):
        print()
        print(f"ERROR === dicho_insert ne fonctionne pas")

def papers_please(closest1, closest2):
    """
    GLORY TO ARZTOTZKA
    Verifie les papiers pour confirmer
    que les points de closest1 sont les
    memes dans closest2. Bancal mais bon...
    C'est un test!
    """
    same = True

    for i, j in zip(range(len(closest1)), range(len(closest1[0].coordinates))):
        same &= (closest1[i].coordinates[j] == closest2[i].coordinates[j]) or (closest1[not i].coordinates[j] == closest2[i].coordinates[j])

    # discrepancy if same = False
    if DEBUGGING and not same:
        print("DEBUG === Discrepancy")
        print("DEBUG === closest1")
        print_array(closest1)
        print("DEBUG === closest2")
        print_array(closest2)

    return same

def test_compare_to_naive(compared_closest, algorithme="l'algorithme"):
    """
    teste tree_no_sort en ayant
    pour reference le test naif
    Si rien ne s'affiche, c'est
    probablement que la fonction marche
    """
    all_good = True

    for _ in range(TEST_NUMBER):
        points = generate_point_sample(POINT_NUMBER)
        closest_naive = naive.get_closest(points)
        closest_solution = compared_closest(points)

        if not papers_please(closest_naive, closest_solution):
            all_good = False
            print(f"ERROR === Discrepancy ==============================")
            print(f"ERROR === naive    | distance : {distance2(closest_naive[0], closest_naive[1])}")
            tycat(points, closest_naive)
            print(f"ERROR === compared | distance : {distance2(closest_solution[0], closest_solution[1])}")
            tycat(points, closest_solution)

    if all_good:
        print(f"\033[1;32mTout va bien, {algorithme} a les memes resultats que la fonctione naive.\033[0m")

def test_algo(fnc_closest):
    """
    Lance les tests sur l'algorithme
    donne en entree. Le but est de
    debug directement dans la fonction
    fnc_closest. DEBUGGING est donc
    sur false par defaut.
    """
    points = generate_point_sample(MINIMUM_POINTS)
    closest = fnc_closest(points)

    if DEBUGGING:
        print(f"DEBUG === Pas d'erreur fatale")
        seg = Segment(closest)
        tycat(points, closest, seg)

def run(fnc_closest1, fnc_closest2, n):
    """
    Lance simplement les fonction n fois
    sans debug. C'est utile pour compter
    le nombre de passages dans get_closest
    par exemple.
    """
    for _ in range(n):
        points = generate_point_sample(POINT_NUMBER)
        fnc_closest1(points)
        fnc_closest2(points)

def main():
    test_compare_to_naive(randomized.get_closest, "randomized")
    # test_algo(randomized.get_closest)
    # test_dicho_insert()
    # run(tree.get_closest, tree_no_sort.get_closest, 100)

if __name__ == "__main__":
    main()
