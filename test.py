#!/usr/bin/env python3
# Imports
from student.utils import generate_point_sample, print_array, distance2
from geo.point import Point
from time import time
from random import random
from geo.tycat import tycat
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import student.naive.solution as naive
import student.tree_no_sort.solution as tree_no_sort

from main import main as realmain

# Constants
POINT_NUMBER = 50
TEST_NUMBER = 100
DEBUGGING = False # Only for deep debugging


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
        print("DEBUG --- Discrepancy")
        print("DEBUG --- closest1")
        print_array(closest1)
        print("DEBUG --- closest2")
        print_array(closest2)

    return same

def test_sorting():
    """
    Fait des tests simples de tri
    """
    points = generate_point_sample(POINT_NUMBER)
    link, sort_x, sort_y = tree_module.tri_points(points)

    print("-------LINK")
    print(link)
    print("-------sort_x")
    print_array(sort_x)
    print("-------sort_y")
    print_array(sort_y)

def test_compare_to_naive(compared_closest):
    """
    teste tree_no_sort en ayant
    pour reference le test naif
    Si rien ne s'affiche, c'est
    probablement que la fonction marche
    """
    for _ in range(TEST_NUMBER):
        points = generate_point_sample(POINT_NUMBER)
        closest_naive = naive.get_closest(points)
        closest_solution = compared_closest(points)

        if not papers_please(closest_naive, closest_solution):
            print(f"ERROR === Discrepancy ==============================")
            print(f"ERROR === naive    | distance : {distance2(closest_naive[0], closest_naive[1])}")
            tycat(points, closest_naive) 
            print(f"ERROR === compared | distance : {distance2(closest_solution[0], closest_solution[1])}")
            tycat(points, closest_solution)

def main():
    test_compare_to_naive(tree_no_sort.get_closest)

if __name__ == "__main__":
    main()
