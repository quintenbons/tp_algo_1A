"""
solution using randomization 
"""
from student.utils import print_answer
from geo.point import Point

# debugging #########
from geo.tycat import tycat
from timeit import timeit
from geo.segment import Segment

DEBUGGING = False
######################

# We extend class Point
class PointHash(Point):

    # hash both coordinate and XOR the result
    def __hash__(self):
        return hash(self.coordinate[0]) ^ hash(self.coordinate[1])

class Grid(object):

    # n : len(points)
    def __init__(self, points, min_dist):
        self.width = min_dist
        self.points = dict()
        for point in points:
            # Todo, grid coordinate of point
            grid_coords = "something"

            self.points[point] = grid_coords


    # o(log n)
    # find the cell where point is
    def find_cell(self, point):
        ...

    # o(log n)
    # get all points in cell
    def get_points_from(self, cell):
        ...

    # o(log n)
    # insert a new point in the grid
    def insert(self, point):
        ...


def get_closest(points):

    # We take distance from two random points
    current_min_dist = points[0].distance_to(points[1])
    last_min_dist = current_min_dist

    # Data structure helper
    grid = Grid(points[:2], current_min_dist / 2)

    for i in range(3, len(points)):
        # step 1 : find the cell in the grid where points[i] insert
        # o(1)
        cell_i = grid.find_cell(points[i])

        # step 2 : recalculate current_min_dist
        for j in range(i):
            # if point was not previously seen, we add it in our grid
            cell_j = grid.find_cell(points[j])

            # 2 points in the same cell -> new min
            if cell_i == cell_j:
                current_min_dist = points[i].distance_to(points[j])
                break


        # step 3
        if current_min_dist == last_min_dist:
            # we didn´t found a better min_dist with points[i]
            grid.insert(points[i])
        else:
            # new min_dist found, we recreate a new grid
            grid = Grid(points[:i], current_min_dist / 2)

    # Solution
    return current_min_dist
