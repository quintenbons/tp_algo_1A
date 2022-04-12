"""
Utilitaires utilises par differents programmes
"""
from random import random
from geo.point import Point

def print_answer(closest):
    """
    Affiche la solution comme le veut le sujet.
    print(point) semble ne pas fonctionner.
    """
    p1_coord = closest[0].coordinates
    p2_coord = closest[1].coordinates

    print(f"{p1_coord[0]}, {p1_coord[1]}; {p2_coord[0]}, {p2_coord[1]}")

def generate_point_sample(number):
    """
    Genere un tableau de points (a manger pour
    les fonctions get_closest des solutions)
    """
    points = [Point((random(), random())) for _ in range(number)]
    return points

def print_array(l):
    """
    Affiche une liste sur plusieurs lignes
    utile pour afficher des points
    """
    for i in range(len(l)):
        print(f"{i:4} : {l[i]}")

def distance2(point1, point2):
    """
    Renvoie le carre de la distance euclidienne
    C'est plus performant, et equivalent. On peut
    cependant aussi utiliser une autre distance,
    vu que le sujet ne precise rien a ce sujet.
    """
    d2  = (point1.coordinates[0] - point2.coordinates[0]) ** 2
    d2 += (point1.coordinates[1] - point2.coordinates[1]) ** 2

    return d2

def dichotomy_insert(point, sorted_points, axis, start=0, stop=-1):
    """
    Insere point dans la liste triee de points
    sorted_points selon l'axe axis.
    Methode: dichotomie recursive
    On ne cherche pas a battre des records de perf
    (sinon on ferait de l'assembleur)
    O(ln n)
    """
    # cas du debut d'algo
    if stop == -1:
        stop = len(sorted_points)

    # c'est bon
    if start == stop:
        sorted_points[start:start] = [point]
        return

    # point median
    median_index = (stop+start) // 2
    median_point = sorted_points[median_index]

    # a gauche
    if point.coordinates[axis] < median_point.coordinates[axis]:
        dichotomy_insert(point, sorted_points, axis, start, median_index)

    # a droite
    else:
        dichotomy_insert(point, sorted_points, axis, median_index + 1, stop)
