# règles du jeu sur https://www.trictrac.net/jeu-de-societe/streams-0

import numpy as np
import random as rd

#fonction qui créée le découpage d'une liste L en liste des longueurs des suites croissantes (sans joker)

def suitsanjok(L):
    if len(L)==1:
        return([1])
    else:
        A=L[1:]
        S=suitsanjok(A)
        if L[0]<=A[0]:
            S[0]+=1
        else:
            S.insert(0,1)
        return(S)

#fonction qui correspond au barême Streams

def f(i):
    rep=0
    if i==2:
        rep=1
    elif i==3:
        rep=3
    elif i==4:
        rep=5
    elif i==5:
        rep=7
    elif i==6:
        rep=9
    elif i==7:
        rep=11
    elif i==8:
        rep=15
    elif i==9:
        rep=20
    elif i==10:
        rep=25
    elif i==11:
        rep=30
    elif i==12:
        rep=35
    elif i==13:
        rep=40
    elif i==14:
        rep=50
    elif i==15:
        rep=60
    elif i==16:
        rep=70
    elif i==17:
        rep=85
    elif i==18:
        rep=100
    elif i==19:
        rep=150
    elif i==20:
        rep=300
    return(rep)


#fonction qui calcule le score final d'une suite L où il n'y a pas de joker

def scorsanjok(L):
    rep=0
    S=suitsanjok(L)
    for i in S:
        rep+=f(i)
    return(rep)

#modification pour prendre en compte le joker

def scoravecjok(L):
    jok=-1
    for i in range(len(L)):
        if L[i]=='J':
            jok=i
    if jok==-1:
        return(scorsanjok(L))
    else:
        L1,L2=L.copy(),L.copy()
        if jok==0:
            L1[0]=1
            return(scorsanjok(L1))
        elif jok==len(L)-1:
            L1[len(L)-1]=30
            return(scorsanjok(L1))
        else:
            L1[jok]=L1[jok-1]
            L2[jok]=L2[jok+1]
            S1=scorsanjok(L1)
            S2=scorsanjok(L2)
            if S1>S2:
                return(S1)
            else:
                return(S2)

#fonction qui donne la liste des places encore disponible

def listeplacesdispo(L):
    r=[]
    for i in range(len(L)):
        if L[i]==0:
            r+=[i]
    return(r)


#fonction récursive qui cherche à placer le nouvel élément tiré e dans la liste L, en maximisant l'espérance du score (rat pour "reste à tirer dans le sac)
def trouvemeilleureplace(L,e,rat):
    disp=listeplacesdispo(L)
    if len(disp)==1:
        L1=L.copy()
        L1[disp[0]]=e
        return(disp[0],scoravecjok(L1))
    else:
        bonplac=-1
        scortemp=0
        for p in disp:
            L1=L.copy()
            L1[p]=e
            moy=0
            for i in range(len(rat)):
                nouvrat=rat.copy()
                del(nouvrat[i])
                p2,s2=trouvemeilleureplace(L1,rat[i],nouvrat)
                moy+=s2/len(rat)
            if moy>scortemp:
                scortemp=moy
                bonplac=p
        return(bonplac,scortemp)


#fonction qui créée une liste dont les éléments sont les jetons d'un vrai sac Streams

def urnestreams():
    u=['J']
    for i in range(1,11):
        u+=[i]
    for i in range(11,20):
        u+=[i,i]
    for i in range(20,31):
        u+=[i]
    return(u)

#fonction qui tire au hasard sans remise nbtire éléments dans la liste L

def tirauhasard(L,nbtire):
    LL=L.copy()
    rep=[]
    n=len(L)
    for i in range(nbtire):
        a=rd.randint(0,n-i-1)
        rep+=[LL[a]]
        del(LL[a])
    return(rep)

#fonction qui compte le nombre d'éléments entre a et b dans une liste L (le 'J' étant entre a et b)

def nbelementsentre(a,b,L):
    nb=0
    for e in L:
        if e=='J':
            nb+=1
        elif a<=e and e<=b:
            nb+=1
    return(nb)

#fonction qui donne le nombre de cases non nulles dans une liste L

def nbnonnul(L):
    r=0
    for i in L:
        if i!=0:
            r+=1
    return(r)


#fonction qui, étant donnée une liste seq dans laquelle figure une liste d'éléments (entiers non nuls ou 'J'), les places encore libres étant représentées par des 0, et une liste tir, permet de voir si en piochant des éléments dans tir, on peut compléter seq en une suite croissante

def completable(seq,tir):
    rep=1
    g=1
    d=30
    n=0
    for e in seq:
        if e!='J':
            if e==0:
                n+=1
            else:
                d=e
                if g>d or nbelementsentre(g,d,tir)<n:
                    rep=0
                g=e
                d=30
                n=0
        if nbelementsentre(g,30,tir)<n:
            rep=0
    return(rep)


#fonction qui en fonction de l'état de la liste à 20 cases partiellement remplie, du reste à tirer, et du nombre de tirage, évalue la "qualité de la situation". La qualité est la somme des qualités des différentes sous-séquences de différentes longueur. La qualité d'une séquence dépend de sa longueur, de sa probabilité de complétion en effectuant des tirages, et du degré de complétion déjà effectif (avant tirage)

def evaluesit(L,rat,nbtir):
    scor=0
    tech=-10*nbtir+240
    for k in range(tech):
        tirage=tirauhasard(rat,nbtir)
        for i in range(19):
            for j in range(19-i):
                M=L[j:j+i+2]
                scor+=f(i+2)*(nbnonnul(M)+1)/(i+2)*completable(M,tirage)/tech
    return(scor)


#fonction qui trouve, à l'étape numetap,étant donné l'état L de la suite de 20 cases, et l'élément e qui vient d'être tiré, la place où il faut le mettre pour maximiser la qualité de la situation

def trouveplacedebut(L,e,rat,numetap):
    scormax=0
    plac=-1
    for i in range(20):
        if L[i]==0:
            LL=L.copy()
            LL[i]=e
            a=evaluesit(LL,rat,20-numetap)
            if a>scormax:
                scormax=a
                plac=i
    return(plac)


#fonction qui fait marcher le joueur artificiel : à 20 reprises, on demande quel est le numéro qui a été tiré, et la fonction répond où le placer dans la suite. au cours des 17 premières étapes, il utilise la fonction trouveplacedebut, puis sur les 3 dernières étapes, la fonction trouvemeilleureplace (qui est optimale, mais très gourmande en temps de calcul au délà de 4 étapes. A la fin, la liste de 20 cases est affichée, ainsi que le score (cela nous épargne de le calculer à la main...)
def partie():
    L=[]
    for i in range(20):
        L+=[0]
    a=urnestreams()
    for i in range(17):
        tir=input('numéro tiré ? ')
        if tir!='J':
            tir=int(tir)
        a.remove(tir)
        b=trouveplacedebut(L,tir,a,i+1)
        L[b]=tir
        print('à placer case numéro ',b+1)
    for i in range(18,21):
        tir=input('numéro tiré ? ')
        if tir!='J':
            tir=int(tir)
        a.remove(tir)
        b=trouvemeilleureplace(L,tir,a)[0]
        L[b]=tir
        print('à placer case numéro ',b+1)
    print(L)
    print(scoravecjok(L))


#pour réaliser une partie contre l'ordinateur : il suffit de lancer partiecontreordi() (places numérotées entre 1 et 20)

def partiecontreordi():
    Lord=[]
    for i in range(20):
        Lord+=[0]
    Ljoueur=Lord.copy()
    a=urnestreams()
    for i in range(17):
        tir=tirauhasard(a,1)[0]
        print('on a tiré le ',tir)
        placjoueur=int(input('Vous le mettez à quelle place ? '))
        Ljoueur[placjoueur-1]=tir
        a.remove(tir)
        print('l ordi réfléchit...')
        b=trouveplacedebut(Lord,tir,a,i+1)
        Lord[b]=tir
    for i in range(18,21):
        tir=tirauhasard(a,1)[0]
        print('on a tiré le ',tir)
        placjoueur=int(input('Vous le mettez à quelle place ? '))
        Ljoueur[placjoueur-1]=tir
        a.remove(tir)
        b=trouvemeilleureplace(Lord,tir,a)[0]
        Lord[b]=tir
    print('Vous avez créé la suite ',Ljoueur)
    scorjoueur=scoravecjok(Ljoueur)
    print('Vous marquez ',scorjoueur,' points')
    print('L ordinateur a créé la suite ',Lord)
    scorord=scoravecjok(Lord)
    print('il a marqué ',scorord,' points')
    if scorord>scorjoueur:
        print('Vous avez perdu')
    elif scorord==scorjoueur:
        print('match nul')
    else:
        print('Vous avez gagné')


def partiesansordi():
    a=urnestreams()
    encore=input('c est parti !')
    for i in range(20):
        tir=tirauhasard(a,1)[0]
        print('on a tiré le ',tir)
        encore=input('c est bon pour tout le monde ?')
        if encore=='0':
            return



a=input('Taper 1 pour jouer à un joueur (il peut y avoir davantage de joueurs réels, mais il faudra qu\'ils comptent leurs points tout seuls) contre l\'ordinateur, avec tirage des numéros par l\'ordinateur,\nTaper 2 pour jouer sans ordinateur (chaque joueur réel compte seul ses points à la fin\n Taper 3 pour faire jouer l\'ordinateur face à des tirages réalisés dans un vrai sac\n')

if a=='1':
    partiecontreordi()
elif a=='2':
    partiesansordi()
else:
    partie()






