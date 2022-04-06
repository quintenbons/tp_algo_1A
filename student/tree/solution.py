"""
solution qui utilise des arbres
insere les points medians en
priorite.
"""

from student.tree.tree import Tree

# debugging #########
from geo.segment import Segment
from student.traceur import display_instance
from geo.tycat import tycat

# Note: debug a privilegier
DEBUGGING = False
######################

def get_closest(points):
    tree = Tree()
    two_closest = tree.insert(points)

    if DEBUGGING:
        # image svg de l'arbre
        display_instance(tree, deeply=False, visualize=False, image_name="./out")

        print(f"DEBUG === Pas d'erreur fatale")
        # root de l'arbre a sa couleur propre
        seg = Segment([two_closest[0], two_closest[1]])
        tycat(seg, points, two_closest, tree.point)

    return two_closest
