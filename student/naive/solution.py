"""
solution naive au probleme
"""
from student.utils import distance2

def get_closest(points):
    """
    Solution naive
    """
    index_couples = [(i, j) for i in range(len(points)) for j in range(i+1, len(points))]
    solutions = [((points[i], points[j]), distance2(points[i], points[j])) for (i,j) in index_couples]
    best_solution = min(solutions, key=lambda t: t[1])

    return best_solution[0]
