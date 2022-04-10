# Sommaire
- [Structure](#structure)
- [Solutions](#solutions)
    - [lineaire (naive)](#lineaire)
    - [Arbre aleatoire](#arbre-aleatoire)
    - [Arbre median](#arbre-median)
    - [Grille](#grille)

# Structure

Le projet est ecrit en anglais, mais les commentaires sont en francais.
Les sous dossiers de student/ ont tous un script solution.py qui contient une fonction get_closest(points) qui retourne un couple de points plus proches voisins.<br>
Il arrive que les structures utilisees soint programmees dans des fichiers autres que solution.py (comme tree.py).

Voici la structure de git:

- exemple_x.pts -> Exemples de nuages de points 
- hello.py -> Exemple de debug (import initial)
- main.py -> Programme principal qui lance la solution la plus efficace par defaut
- test.py -> Programme de tests (il faut lire un peu pour comprendre)
- time_complexity.py -> Tests de performances (affichage grace a pyplot)
- geo/ -> Modules geometriques
    - point.py
    - quadrant.py
    - segment.py
    - tycat.py
- student/ -> Coeur du travail des eleves
    - traceur.py -> Traceur (merci au prof de BPI qui a cree ceci)
    - utils.py -> Utilitaires utilises dans les autres scripts
    - naive/ -> [lineaire (naive)](#lineaire)
    - tree_no_sort/ -> [Arbre aleatoire](#arbre-aleatoire)
    - tree/ -> [Arbre median](#arbre-median)
    - grid/ -> [Grille](#grille)

# Solutions

-- --

## lineaire

#### Explication

Solution naive consistant a trouver pour chaque point le voisin le plus proche en calculant la distance de chaque voisin, avant de chercher le minimum de distance.

#### Complexite | cas quelconque: O(n<sup>2</sup>)<br>

Il s'agit d'une double boucle: O(n) dans O(n).

-- --

## Arbre aleatoire

#### Explication

Insere tous les points un a un dans un arbre k-d avec k=1 d=2. Les points sont inseres dans un ordre aleatoire pour eviter d'etre influence par l'ordre des points
(au cas ou ils seraient tries par exemple, ce qui menerait a un cas tres peu performant).

Dans le meilleur des cas, l'insertion du i-eme point permet de trouver son voisin le plus proche en O(ln i).<br>
Dans le pire des cas, il faudra passer par tous les points, ce qui reste mieux que la solution lineaire en performance (equivalent en complexite)

Une amelioration de cette solution, si on ne fait pas confiance au dieu de la chance, serait d'inserer dans l'ordre les points mediants de chaque hyperplan ceci mene a un kd-tree "plus parfait".
(Voir la solution [Arbre median](#arbre-median))

#### Complexite | meilleur cas: O(n ln(n)) | pire cas: O(n<sup>2</sup>) | cas moyen: O(n ln<sup>a</sup>n)<br>

Le meilleur des cas est atteint quand l'arbre est parfait, et qu'il n'y a jamais d'intersection entre la boule de proximite et l'hyperplan oppose. Voir la solution k-d dans le meilleur des cas.

Le pire des cas est atteint quand l'arbre est un peigne droit ou gauche, et que la racine est toujours le point le plus proche de chacune des feuilles.
L'insertion du i-eme point se fait en O(i), il suffit donc de faire la somme des i pour i allant de 2 a n. (Note: c'est un peu mieux que la solution naive quand meme)

Il reste assez raisonable de penser que l'on n'aura pas souvent besoin de gerer le cas d'intersection en inserant le i-eme point.
On pourrait faire un long calcul probabiliste pour essayer de montrer qu'approcher ce nombre par un O(i) est grandement exagere, mais cela ne me semble pas tres interessant.
On peut donc faire une supposition tres bancale que ce nombre est en O(ln i), ET que ces occurrences se prononcent loin de la racine (sur les C dernieres branches, avec C constant... ou en O(ln i) si vous voulez).
Ce qui mene avec des calculs assez simples au fait que l'insertion et la recherche du i-eme point se fait en moyenne en O(ln i) (ou en O(ln<sup>a</sup> i).

Ainsi le cas moyen est quand meme quasi lineaire. Et si vous n'arrivez pas a avaler l'hypothese bancale, on sera du moins en O(n ln<sup>a</sup>(n)). La page wikipedia anglaise qui ressemble le plus a notre implementation dit pour l'insertion d'un point "The performance of this algorithm is nearer to logarithmic time than linear time".

-- --

## Arbre median

#### Explication

Idem que l'arbre aleatoire, mais selectionne le meilleur point a inserer a chaque fois. La fonction de tri ne sera executee qu'une seule fois, au debut de l'algorithme. 
Ce tri est fait pour les deux axes, en O(n ln n). Nous utilisons ici le qsort de python, mais un algorithme en diviser pour reigner pourrait aussi marcher.

Une petite "amelioration" (qui au final en python n'en est pas une) de la fonction get_closest a aussi etee apportee. Le but n'est pas tant

![image explicative](./explanations/kdtree.png)

Le dessin le montre bien: les ensembles de points B et A seront de toute facon trop loin de P2 pour etre un meilleur voisin. Autant ne pas les regarder du tout (cela couterait une simple projection). Au final le fait de projeter 1 fois par noeud coute plus cher que de quand meme verifier tous les points de A et B dans le cas moyen. Mais c'etait quand meme une experience interessante.

#### En pratique

Il s'avere que 1/4 des noeuds sont esquives par la petite amelioration. Mais la courbe de performance monte a notre grand etonnement.
Il est aussi a noter qu'en python (peut etre pas en C) l'arbre aleatoire etait plus efficace sur des points generes aleatoirement.

#### Complexite | cas quelconque: O(n ln(n))

Tri en O(n ln n).

On se retrouve ensuite dans le meilleur des cas de l'arbre aleatoire, a quelques O(1) pres...
Sans trop rentrer dans les details, on est en O(n ln n) si notre algorithme de recherche d'intersection s'effectue assez rarement.

Ainsi le total se fait en temps proche de O(n ln n).

-- --

## Grille

#### Explication

TODO

#### Complexite | cas quelconque: O(n)

TODO mais bon wikipedia dit en O(n)
