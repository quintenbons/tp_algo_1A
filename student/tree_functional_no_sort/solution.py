"""
Implementation de Inge Li Gørtz
Algorithme tres simple a implementer,
et tres intuitif. Mais neanmoins tres
efficace, surtout grace a l'astuce du
"Merge" dans le diviser pour reigner
"""
from student.utils import distance2
from random import shuffle

def get_closest(points):
    """
    Renvoie les meilleurs voisins.
    Ici on ne trie pas les points.
    """
    # on shuffle les points
    shuffle(points)

    # on divise pour reigner
    closest_two, _ = divide_and_conquer(points)

    return closest_two


def divide_and_conquer(points, axis=False):
    """
    Renvoie les meilleurs voisins ainsi que
    la dist2.
    Renvoie None, -1

    Parametres:
    points: les points non tries
    """
    n = len(points)

    # algo naif
    if n < 4:
        if n == 1:
            return None, -1

        indexes = [(i, j) for i in range(n) for j in range(i+1, n)]
        couples = [(points[i], points[j]) for (i,j) in indexes]
        dists2 = [distance2(p1, p2) for (p1, p2) in couples]
        best_solution = min([(c, d2) for (c, d2) in zip(couples, dists2)], key=lambda t: t[1])

        return best_solution

    # algo diviser pour reigner
    points0, points1, axis_coordinate = split_points(points, axis)

    closest0, d0 = divide_and_conquer(points0, not axis)
    closest1, d1 = divide_and_conquer(points1, not axis)

    # au moins un des deux n'est pas vide
    closest_two, min_dist2 = (closest0, d0) if d0 != -1 and (d1 == -1 or d0 < d1) else (closest1, d1)

    # on selectionne uniquement les points qui sont assez proche de l'axe
    doubted = select_doubted(points, min_dist2, axis, axis_coordinate)

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
    for p in spoints:
        if (doubted_condition(p)):
            res.append(p)

    # malheureusement il faut trier maintenant
    # c'est ce qui fait que cette solution est moins
    # bonne.
    return sorted(res, key=lambda p: p.coordinates[not axis])

def split_points(points, axis):
    """
    Coupe le tableau en deux parties
    pas forcement de meme taille.
    Si tous les points sont dans le
    meme tableau, on shuffle.
    """
    # il s'agit de np.array.split en fait
    axis_point = points[0]
    points0, points1 = [], []

    for p in points[1:]:
        if p.coordinates[axis] < axis_point.coordinates[axis]:
            points0.append(p)

        else:
            points1.append(p)

    # on doit reshuffle
    if len(points0) == 0 or len(points1) == 0:
        shuffle(points)
        return split_points(points, axis)

    return points0, points1, axis_point.coordinates[axis]
