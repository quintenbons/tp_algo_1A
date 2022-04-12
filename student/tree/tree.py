"""
Gestion d'arbres binaires (proche des kd-tree avec k = 1, d = 2)
"""

from student.utils import distance2, dichotomy_insert
from random import shuffle

# DEBUG
from geo.tycat import tycat
from student.traceur import display_instance
from student.utils import print_array

def split_sorted(sorted_points, median_index, axis):
    """
    Renvoie sorted0 et sorted1 de facon
    a inserer dans l'arbre les medianes.
    Attention axis != self.axis
    il n'y a pas d'interet a en faire
    une methode de tree

    Notez que cette fonction peut etre
    optimisee, assez facilement d'ailleurs
    mais je doute qu'on puisse
    avoir une meilleure complexite.
    Je privilégie la simplicité.
    """
    sorted0 = [[] for _ in range(2)]
    sorted1 = [[] for _ in range(2)]

    # cote deja trie
    sorted0[axis] = sorted_points[axis][:median_index]
    sorted1[axis] = sorted_points[axis][median_index+1:]

    # cote a trier
    # la coordonnee de l'axe
    axis_coordinate =  sorted_points[axis][median_index].coordinates[axis]

    # ce cas pose probleme:
    # [0 1 1 1 1 1 1 3 5] par exemple
    # [0 1 1 1] [1 1 3 5] des 1 de chaque cote

    # solution: les points sur l'axe sont ajoutes a la fin
    # normalement les points sur l'axe sont rares, je ne
    # m'attarde donc pas trop sur ce probleme
    on_axis = []
    for point in sorted_points[not axis]:
        # c'est le point median, on ignore
        if point == sorted_points[axis][median_index]:
            continue

        # pour le fils 0
        if point.coordinates[axis] < axis_coordinate:
            sorted0[not axis].append(point)

        # pour le fils 1
        elif point.coordinates[axis] > axis_coordinate:
            sorted1[not axis].append(point)

    for point in on_axis:
        # il manque des points au fils gauche
        if len(sorted0[not axis]) < len(sorted0[axis]):
            # on utilise ici une insertion par dichotomie
            dichotomy_insert(point, sorted0, not axis)

        # il manque des points au fils droit (sinon bizarre...)
        else:
            dichotomy_insert(point, sorted1, not axis)

    return sorted0, sorted1

class Tree:
    """
    Arbre binaire triant les points selon un axe
    qui alterne de pere en fils. L'arbre est concu
    pour etre construit d'une traite. On decline toute
    responsabilite au sujet des inserts post-creation.
    Astuce: pour l'affichage, utiliser le module traceur
    """
    def __init__(self, axis=False):
        """
        Initialise un arbre vide.
        axis=0 (Falsy) implique que l'on divise le plan
        verticalement pour diviser les points.
        """
        # Par defaut, un arbre vide. Pas de fils (None)
        # Mais pret a accueillir un point (auquel cas
        # on initialisera les fils)
        self.axis = axis
        self.point = None
        self.children = [None, None]

    def insert(self, points):
        """
        Insere tous les points. Renvoie le couple de
        plus proches voisins. Cette fonction est
        a appeler sur la racine seulement.
        Precondition: l'arbre est vide (sans quoi
        les insert_single ne se feront pas bien)
        """
        # dans le cas ou on cree un arbre trop vide
        # pour parler de "voisins"
        if len(points) < 2:
            return [None, None]

        # On trie les points selon les deux axes
        sorted_points = [sorted(points, key=lambda point: point.coordinates[i]) for i in range(2)]

        # On insere tous les points (pas encore recursif ici)
        closest_two, _ = self.insert_sorted(sorted_points, self.axis)

        return closest_two

    def insert_sorted(self, sorted_points, axis):
        """
        Insere les points de sorted_points et
        renvoie le couple de plus proches voisins
        ainsi que la dist2.
        sorted_points=[sorted_x, sorted_y]
        avec sorted_x et sorted_y les
        points tries selon les coordonnees.
        """
        # sorted_points est vide, pas besoin de continuer.
        if len(sorted_points[axis]) == 0:
            return [None, None], -1

        # souci de lisibilite
        potential_best = []

        # On cree un noeud avec le point median
        # dans le cas d'un nombre pair on prefere
        # le dernier
        median_index = len(sorted_points[axis]) // 2
        median_point = sorted_points[axis][median_index]

        potential_best.append(self.insert_single(median_point))

        # On prepare le terrain pour les fils
        sorted0, sorted1 = split_sorted(sorted_points, median_index, axis)

        # et on appelle recursivement SUR SELF
        potential_best.append(self.insert_sorted(sorted0, not axis))
        potential_best.append(self.insert_sorted(sorted1, not axis))

        # on selectionne le meilleur... on aurait pu utiliser
        # min(x for x in potential_best if x[1] != -1, key=lambda x: x[1])
        closest_two, min_dist2 = [None, None], -1

        for couple, dist2 in potential_best:
            if min_dist2 == -1 or (dist2 != -1 and dist2 < min_dist2):
                closest_two, min_dist2 = couple, dist2


        return closest_two, min_dist2

    def insert_single(self, point):
        """
        Insere un seul point et renvoie le couple
        de plus proches voisins, ainsi que la dist2

        Notez que le couple contient forcement point
        sans quoi on pourrait rater un point plus
        proche encore dans l'arbre parent
        """
        # On est a la feuille
        if self.isEmpty():
            self.point = point
            self.children = [Tree(axis=not self.axis) for _ in range(2)]
            return [None, point], -1

        # On selectionne le fils. On profite des booleens python (0=False, 1=True)
        selected_child = point.coordinates[self.axis] >= self.point.coordinates[self.axis]

        # On insere dans l'arbre fils (deja initialise)
        closest_neighbours, closest_dist2 = self.children[selected_child].insert_single(point)

        # Variable indiquant si il faut verifier l'arbre oppose
        inter = False

        # On verifie si self.point est un meilleur candidat
        node_dist2 = distance2(self.point, point)
        if closest_dist2 == -1 or node_dist2 < closest_dist2:
            closest_neighbours = [self.point, point]
            closest_dist2 = node_dist2
            # Auquel cas il a necessairement intersection
            # Ceci economise quasiment rien (un appel de __intersects)
            inter = True

        # On verifie si l'arbre oppose a un potentiel
        # meilleur point
        if inter or self.__intersects(point, closest_dist2):
            # on cherche le meilleur dans l'arbre oppose
            closest, dist2 = self.children[not selected_child].get_closest(point, closest_dist2)

            # si c'est un meilleur voisin (et qu'il existe), on garde celui ci
            if closest != None and dist2 < closest_dist2:
                closest_neighbours = [closest, point]
                closest_dist2 = dist2

        return closest_neighbours, closest_dist2

    def isEmpty(self):
        """
        Renvoie true si l'arbre est vide
        """
        return self.point==None

    def __intersects(self, point, max_dist2):
        """
        Renvoie true si l'arbre oppose a celui
        de point a potentiellement  un meilleur
        voisin. (plus proche que max_dist2)
        """
        projected_dist2 = (self.point.coordinates[self.axis] - point.coordinates[self.axis]) ** 2
        return projected_dist2 < max_dist2

    def __too_far(self, child_number, point, max_dist2):
        """
        Verifie si il l'arbre fils child_number
        est assez loin de point pour ne pas avoir
        a s'en soucier dans get_closest.
        """
        # point sur l'axe ou du bon cote de l'axe. (utilisation de xor)
        if (point.coordinates[self.axis] == self.point.coordinates[self.axis]) or ((point.coordinates[self.axis] > self.point.coordinates[self.axis]) ^ (child_number == 0)):
            return False

        # sinon on projette pour voir si point est assez loin
        return self.__intersects(point, max_dist2)

    def get_closest(self, point, max_dist2=-1):
        """
        En cas d'intersection
        Renvoie le point le plus proche ainsi
        que la dist2.
        max_dist2 est optionnel, mais le preciser
        ameliore les performances (permet a l'algo
        de snobber les arbres trop eloignes)

        Notez que la methode utilisee differe
        de tree_no_sort, simplement pour montrer
        montrer une difference sur les graphes
        de performances. En prennant la fonction
        de tree_no_sort ca ne change presque rien.
        """
        # Cas de l'arbre vide
        if self.isEmpty():
            return None, -1

        possible_results = []

        # pour compter le nombre de noeuds vus avec tree_no_sort
        # print("tree point")

        # technique de tube ou plutot rectangle (voir readme)
        for i in range(len(self.children)):
            # cas desirable (n'entamme pas de recursion)
            if (max_dist2 != -1 and self.__too_far(i, point, max_dist2)):
                continue;

            # mince alors, il faut chercher plus loin
            closest, dist2 = self.children[i].get_closest(point, max_dist2)
            if closest != None:
                possible_results.append((closest, dist2))

        # on ajoute aussi le cas du noeud courant
        possible_results.append((self.point, distance2(self.point, point)))

        # on cherche le couple (point, dist2) pout dist2 minimum
        result = min(possible_results, key=lambda res: res[1])

        return result

    def to_array(self):
        """
        Renvoie un tableau de points
        Utile pour deboguer.
        """
        if self.point == None:
            return []

        return [self.point] + self.children[0].to_array() + self.children[1].to_array()

    def point_count(self):
        """
        Renvoie le nombre de points
        Utile pour deboguer.
        """
        if self.point == None:
            return 0

        return 1 + self.children[0].point_count() + self.children[1].point_count()
