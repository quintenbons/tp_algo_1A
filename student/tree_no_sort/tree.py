"""
Gestion d'arbres binaires (proche des kd-tree avec k = 1, d = 2)
"""

from student.utils import distance2
from random import shuffle

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
        Insere tous les points. renvoie le couple de
        plus proches voisins. Cette fonction est
        a appeler sur la racine seulement.
        Precondition: l'arbre est vide
        """
        # dans le cas ou on cree un arbre trop vide
        # pour parler de "voisins"
        if len(points) < 2:
            return [None, None]

        # On fait un petit shuffle (l'arbre sera
        # plus uniforme dans le cas ou points etait
        # deja trie)
        shuffle(points)

        # On commence a inserer les points
        self.insert_single(points[0])

        closest_dist2 = -1
        closest_neighbours = [None, None]

        for point in points[1:]:
            # On insere le point dans l'arbre
            neighbours, dist2 = self.insert_single(point)

            # N'arrive normalement pas, sachant
            # que l'on a deja place le premier point
            if dist2 == -1:
                raise "Inserted in empty tree"

            # Meilleur voisin
            if closest_dist2 == -1 or dist2 < closest_dist2:
                closest_neighbours = neighbours
                closest_dist2 = dist2

        return closest_neighbours

    def insert_single(self, point):
        """
        Insere un seul point et renvoie le couple
        de plus proches voisins, ainsi que la dist2
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
            closest, dist2 = self.children[not selected_child].get_closest(point)

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
        projected_dist2  = (self.point.coordinates[self.axis] - point.coordinates[self.axis]) ** 2
        return projected_dist2 < max_dist2

    def get_closest(self, point):
        """
        Renvoie le point le plus proche ainsi
        que la dist2. Methode naive en O(n).
        A ameliorer avec une technique de "tube"
        """
        # Cas de l'arbre vide
        if self.isEmpty():
            return None, -1

        possible_results = []

        # On cherche recursivement sur les enfants
        for i in range(len(self.children)):
            closest, dist2 = self.children[i].get_closest(point)
            if closest != None:
                possible_results.append((closest, dist2))

        # on ajoute aussi le cas du noeud courant
        possible_results.append((self.point, distance2(self.point, point)))

        # on cherche le couple (point, dist2) pout dist2 minimum
        result = min(possible_results, key=lambda res: res[1])

        return result
