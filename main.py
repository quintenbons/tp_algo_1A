#!/usr/bin/env python3

from sys import argv
from geo.point import Point
from eleve.naif import print_solution

def load_instance(filename):
    """
    loads .mnt file. 
    returns list of points.
    """
    with open(filename, "r") as instance_file:
        # line = next(iter(instance_file))
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]

    return points

def main():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """
    for instance in argv[1:]:
        points = load_instance(instance)
        print_solution(points)


main()