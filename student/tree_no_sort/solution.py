"""
solution qui utilise des arbres
cette solution est censee etre moins
efficace que tree/solution.py car
on ne cherche pas la mediane
"""

from student.tree_no_sort.tree import Tree

# debugging #########
from geo.segment import Segment
from student.traceur import display_instance
from geo.tycat import tycat

# Note: print_solution a aussi son debug
# mais le debug de ce fichier est plus parlant
# pour les arbres
DEBUGGING = False
######################

def get_closest(points):
    # Cree un arbre et insere les points
    tree = Tree()
    two_closest = tree.insert(points)

    if DEBUGGING:
        # debug plus pousse que print_solution (pour afficher l'arbre
        display_instance(tree, deeply=False, visualize=False, image_name="./out")

        print(f"DEBUG === two_closest: {two_closest}")
        # also displays the points, with root in a different color
        seg = Segment([two_closest[0], two_closest[1]])
        tycat(seg, points, two_closest, tree.point)

    return two_closest
