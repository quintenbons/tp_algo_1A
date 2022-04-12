"""
Implementation de Inge Li Gørtz
Algorithme tres simple a implementer,
et tres intuitif. Mais neanmoins tres
efficace, surtout grace a l'astuce du
"Merge" dans le diviser pour reigner
"""
from student.utils import distance2, dichotomy_insert

def get_closest(points):
    """
    Renvoie les meilleurs voisins.
    Il nous faut d'abord trier les points
    comme dans tree.
    """
    # on trie les points
    spoints = [sorted(points, key=lambda point: point.coordinates[i]) for i in range(2)]

    # on divise pour reigner
    closest_two, _ = divide_and_conquer(spoints)

    return closest_two


def divide_and_conquer(spoints, axis=False):
    """
    Renvoie les meilleurs voisins ainsi que
    la dist2.

    Parametres:
    spoints: [sortedx, sortedy]

    Precondition: n >= 2
    """
    n = len(spoints[0])

    # algo naif
    if n < 4:
        indexes = [(i, j) for i in range(n) for j in range(i+1, n)]
        couples = [(spoints[0][i], spoints[0][j]) for (i,j) in indexes]
        dists2 = [distance2(p1, p2) for (p1, p2) in couples]
        best_solution = min([(c, d2) for (c, d2) in zip(couples, dists2)], key=lambda t: t[1])

        return best_solution

    # algo diviser pour reigner
    sorted0, sorted1, axis_coordinate = split_sorted(spoints, axis)

    closest0, d0 = divide_and_conquer(sorted0, not axis)
    closest1, d1 = divide_and_conquer(sorted1, not axis)

    closest_two, min_dist2 = (closest0, d0) if d0 < d1 else (closest1, d1)

    # on selectionne uniquement les points qui sont assez proche de l'axe
    doubted = select_doubted(spoints, min_dist2, axis, axis_coordinate)

    # on merge. On a possiblement d2 = -1 si il n'y a pas assez de doubted
    closest2, d2 = best_doubted(doubted)

    return (closest_two, min_dist2) if d2 == -1 or min_dist2 < d2 else (closest2, d2)

def best_doubted(doubted):
    """
    Astuce: comme deux poitns du meme
    cote de l'axe ne peuvent pas etre a moins
    de min_dist2 en distance, il suffit de
    verifier les 7 prochains voisins.

    Ceci permet une complexite O(n)
    """
    closest_two = None
    min_dist2 = -1

    for i in range(len(doubted)):
        for j in range(i+1, len(doubted)):
            d2 = distance2(doubted[i], doubted[j])

            if min_dist2 == -1 or d2 < min_dist2:
                closest_two = (doubted[i], doubted[j])
                min_dist2 = d2

    return closest_two, min_dist2

def select_doubted(spoints, min_dist2, axis, axis_coordinate):
    """
    Selectionne uniquement les points
    assez proche de l'axe pour le merge.
    """
    def doubted_condition(point):
        """
        Il suffit d'etre a une distance2 projetee < min_dist2
        """
        projected_dist2 = (point.coordinates[axis] - axis_coordinate) ** 2
        return projected_dist2 < min_dist2

    res = []

    # n'utilisons pas filter pour la perf
    for p in spoints[not axis]:
        if (doubted_condition(p)):
            res.append(p)

    return res


def split_sorted(spoints, axis):
    """
    Renvoie sorted0 et sorted1 de facon
    a pouvoir diviser pour reigner.

    On mettra le point median a droite

    Precondition: >= 4 points
    (ceci permet de ne jamais avoir a renvoyer
    None, -1 comme dans student.tree.solution)
    """

    sorted0 = [[] for _ in range(2)]
    sorted1 = [[] for _ in range(2)]

    median_index = len(spoints[0]) // 2 - 1
    median_point = spoints[axis][median_index]

    # cote deja trie
    sorted0[axis] = spoints[axis][:median_index+1]
    sorted1[axis] = spoints[axis][median_index+1:]

    # cote a trier
    axis_coordinate =  median_point.coordinates[axis]


    # ce cas pose probleme:
    # [0 1 1 1 1 1 1 3 5] par exemple
    # [0 1 1 1] [1 1 3 5] des 1 de chaque cote

    # solution: les points sur l'axe sont ajoutes a la fin
    # normalement les points sur l'axe sont rares, je ne
    # m'attarde donc pas trop sur ce probleme
    on_axis = []
    for point in spoints[not axis]:
        # on discrimine le point median
        if point == median_point:
            sorted0[not axis].append(point)
            continue

        # pour le fils 0
        if point.coordinates[axis] < axis_coordinate:
            sorted0[not axis].append(point)

        # pour le fils 1
        elif point.coordinates[axis] > axis_coordinate:
            sorted1[not axis].append(point)

        # sur l'axe (sauf cas point median)
        else:
            on_axis.append(point)


    for point in on_axis:
        # il manque des points au fils gauche
        if len(sorted0[not axis]) < len(sorted0[axis]):
            # on utilise ici une insertion par dichotomie
            dichotomy_insert(point, sorted0[not axis], not axis)

        # il manque des points au fils droit (sinon bizarre...)
        else:
            dichotomy_insert(point, sorted1[not axis], not axis)


    return sorted0, sorted1, axis_coordinate
