#!/usr/bin/env python3
# Imports
from student.utils import generate_point_sample, print_array
from geo.point import Point
from time import time
from random import random
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import student.naive.solution as naive
import student.tree.solution as tree
import student.tree.tree as tree_module

# Constants
MIN_POINTS = 10
MAX_POINTS = 100
SAMPLE_SIZE = 10 # automatic linspace
TEST_REPEAT = 20 # number of repeats (uniformize)


def main_sorting():
    """
    Fait des tests simples de tri
    """
    points = generate_point_sample(5)
    link, sort_x, sort_y = tree_module.tri_points(points)

    print("-------LINK")
    print(link)
    print("-------sort_x")
    print_array(sort_x)
    print("-------sort_y")
    print_array(sort_y)

def main():
    """
    Insere dans l'arbre des points, en esperant
    prendre a chaque fois la mediane
    """
    points = generate_point_sample(10)
    my_tree = tree_module.Tree()
    my_tree.insert_array(points)

if __name__ == "__main__":
    main()
