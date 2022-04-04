
"""
Gestion d'arbres binaires (proche des kd-tree avec k = 1, d = 2)
"""

from geo.point import Point

class Tree:
    """
    Chaque noeud contient un point (2 dimensions), chaque noeud a deux fils,
    Pour approcher un arbre minimal, idealement, il faut que la coordonnee
    orthogonale a l'axe soit medianne dans son demi plan.
    """
    def __init__(self, point=None, axis=True):
        """
        Initialise un narbre, et insere point si besoin.
        l'axe sert pour inserer les points selon l'axe
        x (coupure verticale) si True, y (coupure horizontale) si False
        """
        self.axis = axis
        self.child1 = None
        self.child2 = None
        self.point = point

    def __intersects(self, point, max_dist):
        """
        Retourne True seulement si le point est trop proche de la
        frontiere, et que l'arbre oppose peut avoir un point plus
        proche
        """
        projected_dist = 0;
        if self.axis:
            projected_dist = abs(self.point.coordinates[0] - point.coordinates[0])
        else:
            projected_dist = abs(self.point.coordinates[1] - point.coordinates[1])

        # on fait simplement une projection sur le bon axe
        return projected_dist < max_dist

    def find_closest(self, point, max_dist):
        """
        Retourne le point le plus proche de point avec une
        methode naive. Cette fonction n'est normalement pas
        souvent appelee. Renvoie (None, max_dist) si aucun
        point de l'arbre n'est assez proche.
        """
        closest = self.point
        dist = self.point.distance_to(point)

        if (self.child1 != None):
            closest1, dist1 = self.child1.find_closest(point, max_dist)
            if (dist1 < dist):
                closest, dist = closest1, dist1

        if (self.child2 != None):
            closest2, dist2 = self.child2.find_closest(point, max_dist)
            if (dist2 < dist):
                closest, dist = closest2, dist2

        return (closest, dist) if dist < max_dist else (None, max_dist)

    def insert(self, point):
        """
        Insere un point dans l'arbre du bon cote de l'axe
        renvoie un couple (closest, dist)
        """
        # Cas 1: a droite ou en haut (cote positif) child2
        if (self.axis and self.point.coordinates[0] > point.coordinates[0]) or (not self.axis and self.point.coordinates[1] > point.coordinates[1]):
            closest, dist = None, -1

            # Felicitations! C'est une feuille!
            if self.child1 == None:
                # On ajoute la feuille
                print(f"DEBUG --- New leaf 1 --- {self.point} / {point} ::: {self.point.distance_to(point)}")
                self.child1 = Tree(point, not self.axis)

                # Le meilleur voisin pour l'instant c'est self
                closest = self.point
                dist = self.point.distance_to(point)


            # On insere en dessous
            else:
                # On insere dans l'arbre fils
                print(f"DEBUG --- Further insert 1")
                closest, dist = self.child1.insert(point)

            # On a besoin de verifier l'autre plan s'il est trop proche (et qu'il existe)
            if self.child2 != None and self.__intersects(closest, dist):
                # Normalement on c'est assez rare d'arriver ici
                # On cherche un potentiel meilleur voisin O(nb_points(child))
                new_closest, new_dist = self.child2.find_closest(point, dist)

                # Si il y en a un, on garde celui ci
                if new_closest != None:
                    closest, dist = new_closest, new_dist

            return (closest, dist)

        # Cas 2: a gauche ou en bas (cote negatif) child1
        else:
            closest, dist = None, -1

            # Felicitations! C'est une feuille!
            if self.child2 == None:
                # On ajoute la feuille
                print(f"DEBUG --- New leaf 2 --- {self.point} / {point} ::: {self.point.distance_to(point)}")
                self.child2 = Tree(point, not self.axis)

                # Le meilleur voisin pour l'instant c'est self
                closest = self.point
                dist = self.point.distance_to(point)


            # On insere en dessous
            else:
                # On insere dans l'arbre fils
                print(f"DEBUG --- Further insert 2")
                closest, dist = self.child2.insert(point)

            # On a besoin de verifier l'autre plan s'il est trop proche (et qu'il existe)
            if self.child1 != None and self.__intersects(closest, dist):
                # Normalement on c'est assez rare d'arriver ici
                # On cherche un potentiel meilleur voisin O(nb_points(child))
                new_closest, new_dist = self.child1.find_closest(point, dist)

                # Si il y en a un, on garde celui ci
                if new_closest != None:
                    closest, dist = new_closest, new_dist

            return (closest, dist)

    def __str__(self):
        """
        print code generating the point.
        """
        if self.point == None:
            return "EmptyTree"

        return f"Tree_[{self.point.__str__()}]"
