"""
Il s'agit de la solution decrite sur wikipedia.
Nous avions eu l'idee de la faire, mais on aurait
pas ose s'y plonger sans guide.

On s'est prive des classes python pour gagner un peu
en perf
"""
from random import random # pour la perf
from math import sqrt # rassurez vous on s'en sert qu'une fois
from student.utils import distance2

# DEBUGING
from geo.tycat import tycat
from geo.segment import Segment
from geo.point import Point
pts = []
checked_pts = []
sgts = []
dmin1 = 1
DEBUGGING = False

def hash_grid(x, y):
    """
    Hash pour le dictionnaire grid qui contient
    la grille
    """
    # Possibles collisions, mais assez rare
    # attention, hash(x) ^ hash(y) donnerait
    # une symetrie.
    return hash((x, y))

def point_to_grid(point, dist_min):
    """
    Traduit les coordonnees. Possiblement
    negatives dans grid, et les ajoute au
    point. Le resultat est stoque dans
    point.grid et point.hash
    """
    [x, y] = [point.coordinates[i] // dist_min for i in range(2)]

    return int(x), int(y)

def closest_within(source, points):
    """
    retourne le couple (closest, dist2)
    ou closest est le point le plus
    proche de source.
    """
    # ATTENTION ici closest represente un point
    closest, min_dist2 = None, -1

    for p in points:
        dist2 = distance2(source, p)

        if min_dist2 == -1 or dist2 < min_dist2:
            closest = p
            min_dist2 = dist2

    return closest, min_dist2

def check_neighbours(point, grid, dist_min):
    """
    Trouve le plus proche voisin parmi
    les voisins de Moore
    """


    if DEBUGGING:
        checked_pts.append(point)

    xp, yp = point_to_grid(point, dist_min)
    hash_grid_source = -1

    points_seen = []

    # ATTENTION ici closest represente un point
    closest_yet, min_dist2 = None, -1

    s = []

    # Pour tous les voisins de Moore
    for x in range(xp-1, xp+2):
        for y in range(yp-1, yp+2):
            index = hash_grid(x, y)

            if DEBUGGING:
                s += rect(x, y)
                if index in grid:
                    print(f"DEBUG === {x, y}: {grid[index]}")
                    points_seen = points_seen + grid[index]
                else:
                    print(f"DEBUG === {x, y}: EMPTY")

            if x == xp and y == yp:
                # on evite de hash 2 fois
                # au cas ou on prend une
                # fonction de hashage un peu
                # costaud. Celle de python est
                # tres legere.
                hash_grid_source = index

            # case vide
            if not (index in grid):
                continue

            closest, dist2 = closest_within(point, grid[index])

            if min_dist2 == -1 or dist2 < min_dist2:
                closest_yet = closest
                min_dist2 = dist2

    if DEBUGGING:
        print(f"DEBUG === Min dist2: {min_dist2:5f} | Closest: {closest_yet}")
        tycat(s, pts, checked_pts, points_seen, point, sgts)

    return hash_grid_source, closest_yet, min_dist2


def closest_pair(points, dist_min2):
    """
    Ajoute les points au grid, tout en
    trouvant les plus proches voisins.
    Il suffit a chaque fois de verifier
    les voisins dits "de Moore", comme un
    deplacement de roi aux echecs.
    """
    # grid[hash(point)] = [point1, point2, ...]
    grid = {}

    # le seul sqrt de tout l'algorithme
    dist_min1 = sqrt(dist_min2)

    # Ici on ecrase dist_min2...
    closest_two, dist_min2 = None, -1

    # on commence maintenant a hacher les points
    for point in points:
        hash_grid, closest, dist2 = check_neighbours(point, grid, dist_min1)

        if dist2 != -1 and (dist_min2 == -1 or dist2 < dist_min2):
            closest_two = [point, closest]
            dist_min2 = dist2

        # on a possiblement une case vide
        if hash_grid in grid:
            grid[hash_grid].append(point)
        else:
            grid[hash_grid] = [point]

    return closest_two


def get_approx(points, n):
    """
    Retourne un tuple (closest, min_dist2)
    en cherchant les meilleurs voisins
    sur n couples choisis au hasard
    (fournit surtout une premiere approximation
    de dist_min2)

    ATTENTION IL EST CRUCIAL DE NE PAS SURCHARGER
    CETTE FONCTION, TANT PIS SI L'APPROXIMATION
    EST NULLE.
    """
    def randome_couple(l):
        """
        retourne un generateur de couples
        aleatoire de l (avec remise)
        """
        while True:
            i = int(random() * len(l))
            j = int(random() * len(l) - 1)
            yield (l[i], l[j]) if i != j else (l[i], l[-1])

    couple_generator = randome_couple(points)

    # le premier
    p1, p2 = next(couple_generator)
    closest_two, min_dist2 = (p1, p2), distance2(p1, p2)

    for _ in range(n):
        p1, p2 = next(couple_generator)
        d2 = distance2(p1, p2)

        if d2 < min_dist2:
            closest_two = (p1, p2)
            min_dist2 = d2

    return closest_two, min_dist2

def rect(x, y):
    """
    rectangle
    """
    segs = []
    x1 = x * dmin1
    y1 = y * dmin1
    x2 = x1+dmin1
    y2 = y1+dmin1
    points = [
        Point([x1, y1]),
        Point([x1, y2]),
        Point([x2, y2]),
        Point([x2, y1])
    ]

    for i in range(4):
        segs.append(Segment([points[i], points[i-1]]))

    return segs

def get_grid_segments(points):
    """
    renvoie les segments pour quadriller la zone de points
    """
    global dmin1
    segs = []

    for point in points:
        x, y = point_to_grid(point, dmin1)
        segs += rect(x,y)

    return segs


def get_closest(points):
    """
    Retourne le couple de meilleurs voisins

    Precondition: n>3 (nb couples >= nb points)
    """
    # premiere aproximation (len(points) pour rester en O(n))
    # ceci est un facteur crucial de la performance finale
    # on n'a pas besoin de closest_two si ce n'est pour le debug
    closest_two, min_dist2 = get_approx(points, len(points))

    if DEBUGGING:
        global pts
        pts = points
        global dmin1
        dmin1 = sqrt(min_dist2)
        global sgts
        sgts = get_grid_segments(points)
        tycat(points, closest_two, sgts)

    # on commence l'etape 2
    new_closest = closest_pair(points, min_dist2)

    return new_closest
