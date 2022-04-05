"""
solution naive au probleme
"""
from student.utils import distance2

def get_closest(points):
    min_dst2 = -1
    closest = [-1, -1]

    for p1 in points:
        min_p1_dst2 = -1
        closest_p1 = None

        # double boucle O(n^2)
        for p2 in points:
            # cas p1 = p2
            if p1 == p2:
                continue

            dst2 = distance2(p1, p2)

            # Meilleur voisin
            if (min_p1_dst2 == -1 or dst2 < min_p1_dst2):
                min_p1_dst2 = dst2
                closest_p1 = p2

        # Meilleur couple de voisins
        if min_dst2 == -1 or min_p1_dst2 < min_dst2:
            min_dst2 = min_p1_dst2
            closest = [p1, closest_p1]

    if closest == [-1, -1]:
        raise Exception("Not enough Points")

    return closest
