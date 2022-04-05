#!/usr/bin/env python3

from sys import argv

from student.utils import print_answer
from geo.point import Point
from student.naive.solution import get_closest

# Debugging only
from geo.segment import Segment
from geo.tycat import tycat
from timeit import timeit

# Constantes
DEBUGGING = False

def load_instance(filename):
    """
    loads .mnt file.
    returns list of points.
    """
    with open(filename, "r") as instance_file:
        # line = next(iter(instance_file))
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]

    return points

def print_solution(points):
    """
    calcul et affichage de la solution
    """
    closest = get_closest(points)

    if (DEBUGGING):
        seg = Segment([closest[0], closest[1]])
        tycat(seg, points, closest)

        duree = timeit(lambda: get_closest(points), number=10000)

        print(f"DEBUG === Distance minimale: {closest[0].distance_to(closest[1])}")
        print(f"DEBUG === Duree d'execution: {duree}")
        print()

    print_answer(closest)

def main():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """
    for instance in argv[1:]:
        points = load_instance(instance)
        print_solution(points)


main()
