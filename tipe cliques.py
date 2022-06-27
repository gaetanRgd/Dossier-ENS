from pylab import *
from random import sample, randint
from mpl_toolkits import mplot3d#.axes3d.Axes3D
import numpy as np


def graphe_vide():
    return []
def creer_graphe_complet(n):
    return [ (n, [[] for i in range(n)] ) ]

# renvoie tous les autres exemplaires du sommet s de la clique cl
# sous la forme de couples (clique, numero) :
def idem_sommet(graphe,cl,s):
    return [(cl,s)] + graphe[cl][1][s]
# donne les cliques auxquelles appartient un sommet :
def cliques_commun(graphe,cl,s):
    res = []
    for (c,t) in idem_sommet(graphe,cl,s):
        res.append(c)
    return res
# donne les sommets reliés par une arête au sommet (cl,s) :
# (il y a des doublons)
def relies(graphe, cl, s):
    res = []
    for c in cliques_commun(graphe,cl,s):
        for i in range( graphe[c][0] ):
            res += idem_sommet(graphe,c,i)
    return res
# teste si deux listes sont disjointes :
def sont_disjointes(l1,l2):
    for x in l1:
        for y in l2:
            if x==y:
                return False
    return True
# ajoute une clique sans liens :
def ajouter_clique_disjoint(graphe,n):
    graphe.append( creer_graphe_complet(n)[0] )

# fusionne deux sommets de deux cliques distinctes :
def ajouter_lien(graphe, cl1,s1,cl2,s2):
    if not sont_disjointes( relies(graphe,cl1,s1) , relies(graphe,cl2,s2) ):
        return None
    S1, S2 = idem_sommet(graphe,cl1,s1), idem_sommet(graphe,cl2,s2)
    for (c1,i1) in S1:
        for (c2,i2) in S2:
            graphe[c1][1][i1].append((c2,i2))
            graphe[c2][1][i2].append((c1,i1))
    return graphe

# ici, liens est une liste à n éléments telle que liens[i] est la liste des couples (cl,s)
# tels que le sommet i de la clique ajoutée est relié au sommet s de la clique cl existante
# (ces deux sommets sont alors confondus)
def ajouter_clique(graphe, n, liens):
    ajouter_clique_disjoint(graphe,n)
    N = len(graphe)
    for i in range(n):
        for (cl, s) in liens[i]:
            ajouter_lien(graphe, N-1,i, cl,s)
    return graphe

def conversion_listes_adj(graphe):
    numeros = [[-1 for i in range(n)] for (n,l) in graphe]
    indice = 0
    res = []
    for clique in range(len(graphe)):
        n = len(graphe[clique][1])
        for s in range(n):
            # on numérote les sommets non déjà numérotés dans la clique visitée
            if numeros[clique][s] == -1:
                numeros[clique][s] = indice
                indice += 1
                res = res + [[]]
            # on numérote les autres exemplaires des sommets
            for (cl,t) in graphe[clique][1][s]:
                if numeros[cl][t] == -1:
                    numeros[cl][t] = numeros[clique][s]
        # on remplit les listes d'adjacence avec les éléments de la clique
        for s in range(n):
            for t in range(n):
                i = numeros[clique][s]
                if t != s:
                    res[i].append(numeros[clique][t])
    return res, numeros


def majorant_theorique(graphe):
    res = 0
    for clique in graphe:
        n = clique[0]
        res += floor(n/2) * ceil(n/2)
    return res

# crée un graphe à N cliques, de taille au plus m, dont le graphe des cliques a une densité p
def creer_graphe_alea(N,m,p):
    def test():
        x = random()
        return (x <= p)
    # créer le graphe des cliques avec ses liens aléatoires de probabilité p
    graphe_cliques = zeros((N,N),dtype=bool)
    for i in range(N):
        for j in range(i+1,N):
            graphe_cliques[i,j] = test()
    graphe = graphe_vide()
    tailles_cliques = []
    # créer les cliques, séparées
    for i in range(N):
        n = randint(2,m)
        ajouter_clique_disjoint(graphe,n)
        tailles_cliques.append(n)
    # fusionner les cliques conformémént au graphe des cliques
    for i in range(N):
        for j in range(i+1,N):
            if graphe_cliques[i,j]:
                s1, s2 = randint(0, tailles_cliques[i] - 1) , randint(0, tailles_cliques[j] - 1)
                # pour s'assurer de ne pas relier à nouveau des cliques déjà reliées par des points communs à une autre :
                for (k,kk) in idem_sommet(graphe,i,s1):
                    for (l,ll) in idem_sommet(graphe,j,s2):
                        graphe_cliques[k,l] = False
                        graphe_cliques[l,k] = False
                ajouter_lien(graphe,i,s1,j,s2)
    return graphe

#Coloriage aleatoire des sommets
def maxcut_alea(graphe):
    maxcut=0
    #recuperation du graphe sous la forme de listes adjacentes
    sommets,numeros=conversion_listes_adj(graphe)
    listeColoriee=[0]*len(sommets)

    #coloriage aleatoire des sommets
    for i in range(len(sommets)):
        listeColoriee[i]=randint(0,1)

    # on compte pour chaque clique la coupe
    for cl in numeros:
        contamines=0
        for s in cl:
            contamines+=listeColoriee[s]
        maxcut+=(len(cl)-contamines)*contamines

    return maxcut

def maxcut_parcours_profondeur(graphe):
    maxcut = 0
    colories = [ [-1]*n for (n,l) in graphe ]
    marques = [False] * len(graphe)
    for i in range(len(graphe)):
        if not marques[i]:
            pile = [i]
            marques[i] = True
            # colorier(j,s,col) colorie le point (j,s) à la couleur col, et ajoute les cliques non marquées des voisins à la pile
            def colorier(j,s,col):
                for (k,ss) in idem_sommet(graphe,j,s):
                    colories[k][ss] = col
                    if not marques[k]:
                        pile.append(k)
                        marques[k] = True
            while pile != []:
                j = pile.pop()
                n = graphe[j][0]
                fixes = [[],[]]
                libres = []
                # trie les sommets de la clique par couleur (0, 1 ou non attribué)
                for s in range(n):
                    col = colories[j][s]
                    if col == -1:
                        libres.append(s)
                    else:
                        fixes[col] .append(s)
                # colorie les sommets de la clique de façon optimale avec les sommets déjà fixés
                if len(fixes[0]) >= n//2:
                    for s in libres:
                        colorier(j,s,1)
                elif len(fixes[1]) >= n//2:
                    for s in libres:
                        colorier(j,s,0)
                else:
                    aColorier = sample( libres, n//2 - len(fixes[1]) )
                    # (évite le recours à "if s in aColorier")
                    for s in aColorier:
                        colorier(j,s,1)
                    for s in libres:
                        if colories[j][s] == -1:
                            colorier(j,s,0)
                # compte les coupes dans la clique
                contamines = 0
                for s in range(n):
                    contamines += colories[j][s]
                maxcut += contamines * (n - contamines)
    return maxcut

def maxcut_parcours_profondeur_colorie(graphe):
    maxcut = 0
    colories = [ [-1]*n for (n,l) in graphe ]
    marques = [False] * len(graphe)
    for i in range(len(graphe)):
        if not marques[i]:
            pile = [i]
            marques[i] = True
            # colorier(j,s,col) colorie le point (j,s) à la couleur col, et ajoute les cliques non marquées des voisins à la pile
            def colorier(j,s,col):
                for (k,ss) in idem_sommet(graphe,j,s):
                    colories[k][ss] = col
                    if not marques[k]:
                        pile.append(k)
                        marques[k] = True
            while pile != []:
                j = pile.pop()
                n = graphe[j][0]
                fixes = [[],[]]
                libres = []
                # trie les sommets de la clique par couleur (0, 1 ou non attribué)
                for s in range(n):
                    col = colories[j][s]
                    if col == -1:
                        libres.append(s)
                    else:
                        fixes[col] .append(s)
                # colorie les sommets de la clique de façon optimale avec les sommets déjà fixés
                if len(fixes[0]) >= n//2:
                    for s in libres:
                        colorier(j,s,1)
                elif len(fixes[1]) >= n//2:
                    for s in libres:
                        colorier(j,s,0)
                else:
                    aColorier = sample( libres, n//2 - len(fixes[1]) )
                    # (évite le recours à "if s in aColorier")
                    for s in aColorier:
                        colorier(j,s,1)
                    for s in libres:
                        if colories[j][s] == -1:
                            colorier(j,s,0)
                # compte les coupes dans la clique
                contamines = 0
                for s in range(n):
                    contamines += colories[j][s]
                maxcut += contamines * (n - contamines)
    return maxcut, colories


# max pour un graphe donné
def maxMaxcut(graphe,f):
    N = 100
    maxi=0
    for i in range(N):
        maxi=max(maxi,f(graphe))
    return maxi

def maxMaxcutColo(graphe,f):
    N = 10000
    maxi=0
    colo=[]
    for i in range(N):
        val=f(graphe)
        if maxi<val[0]:
            maxi=val[0]
            colo=val[1]
    return maxi,colo

# compare la coupe de la fonction f au majorant théorique
# pour des graphes de type creer_graphe_alea(n,m,p)
def comparaison(n,m,p,f):
    N = 1000
    X = arange(N)
    Y = zeros(N)
    for i in range(N):
        g = creer_graphe_alea(n,m,p)
        Y[i] = f(g) / majorant_theorique(g)
    plot(X,Y)
    axis(ymin=0, ymax=1)
    show()

# moyenne du rapport (coupe trouvée) / (majorant théorique)
def moyenne_relative(n,m,p,f):
    N = 20
    S = 0
    for i in range(N):
        g = creer_graphe_alea(n,m,p)
        S += f(g) / majorant_theorique(g)
    return (S/N)

def moyenne_fiabilite(n,m,p,f):
    N = 20
    S = 0
    for i in range(N):
        g = creer_graphe_alea(n,m,p)
        S += maxMaxcut(g,f) / majorant_theorique(g)
    return (S/N)


def affichage_3d_influence_n_m(nmax,mmax,p,f,pasn=1,pasm=1):
    X = outer(arange(1,nmax+1,pasn), ones((mmax-2)//pasm + 1))
    Y = outer(ones((nmax-1)//pasn + 1), arange(2,mmax+1,pasm))
    Z = copy(X)
    for n in range(len(Z)):
        for m in range(len(Z[0])):
            Z[n,m] = moyenne_relative(int(X[n,m]),int(Y[n,m]),p,f)
    ax = mplot3d.axes3d.Axes3D(figure(0))
    ax.plot_surface(X,Y,Z,cmap="viridis")
    ax.plot_surface(array([[0]]),array([[0]]),array([[0]]))
    xlabel("n")
    ylabel("m")

def affichage_3d_fiabilite_n_m(nmax,mmax,p,f,pasn=1,pasm=1):
    X = outer(arange(1,nmax+1,pasn), ones((mmax-2)//pasm + 1))
    Y = outer(ones((nmax-1)//pasn + 1), arange(2,mmax+1,pasm))
    Z = copy(X)
    for n in range(len(Z)):
        for m in range(len(Z[0])):
            Z[n,m] = moyenne_fiabilite(int(X[n,m]),int(Y[n,m]),p,f)
    ax = mplot3d.axes3d.Axes3D(figure(0))
    ax.plot_surface(X,Y,Z,cmap="viridis")
    ax.plot_surface(array([[0]]),array([[0]]),array([[0]]))
    xlabel("n")
    ylabel("m")