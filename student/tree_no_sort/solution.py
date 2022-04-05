"""
solution qui utilise des arbres
cette solution est censee etre moins
efficace que tree/solution.py car
on ne cherche pas la mediane
"""

# debugging #########
from geo.tycat import tycat
from timeit import timeit
from geo.segment import Segment
from student.tree.tree import Tree

DEBUGGING = True
######################

def get_closest(points):
    two_closest = [None, None]
    min_dist = -1

    # l'idee c'est qu'en calculant les plus
    # proches voisins d'un point, on peut garder
    # une partie de l'information pour calculer
    # le plus proche du suivant. Ainsi on sortira
    # de l'algorithme avec encore beaucoup d'infos
    # superflues (le plus proche voisin de CHAQUE
    # point) mais c'est toujours mieux qu'un O(n^2)

    # On fait un arbre
    print(f"DEBUG --- Adding {points[0]} #######################")
    tree = Tree(points[0])

    for point in points[1:]:
        print(f"DEBUG --- Adding {point} #######################")
        # une insertion renverra
        closest_point, dist = tree.insert(point);

        if (min_dist == -1 or dist < min_dist):
            print(f"DEBUG --- NEW CLOSEST {point} / {closest_point} --- {min_dist} / {dist}")
            two_closest = [point, closest_point]
            min_dist = dist

    return two_closest
