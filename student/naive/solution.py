"""
solution naive au probleme
"""
from student.utils import print_answer

# debugging #########
from geo.tycat import tycat
from timeit import timeit
from geo.segment import Segment

DEBUGGING = False
######################

def get_closest(points):
    min_dst = -1
    closest = [-1, -1]

    for p1 in points:
        min_p1_dst = -1
        closest_p1 = -1
        for p2 in points:
            dst = p1.distance_to(p2)

            if dst == 0:
                continue

            if (min_p1_dst == -1 or min_p1_dst > dst):
                min_p1_dst = dst
                closest_p1 = p2

        if min_p1_dst == 0:
            continue

        if (min_dst == -1 or (dst != 0 and min_dst > dst)):
            min_dst = min_p1_dst
            closest = [p1, closest_p1]

    if closest == [-1, -1]:
        raise Exception("Not enough Points")

    return closest
