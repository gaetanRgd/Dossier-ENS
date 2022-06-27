import math
import random
from PIL import Image
blanc=(255,255,255,255)
noir=(0,0,0,255)
# empreinte2,empreinte2+pisur2,empreinteType2,empreinteType3,empreinte4,empreinte6,empreinte7,empreinte8,empreinte9,empreinte10
def init_():
    nomFichier= '/home/usrgaetan/Documents/Fermat/Spe/TIPE/empreinte2.png'
    ImageFile = nomFichier

    try:
        img = Image.open(ImageFile)
    except IOError:
        print ('Erreur sur ouverture du fichier ' + ImageFile)
        exit(1)

    print(img.size)
    print(img.mode)


    return img,nomFichier

# transformer l'image en gris
def grisage(imgGris):
    print('grisage')
    colonne,ligne=imgGris.size
    for i in range(colonne):
        for j in range(ligne):
            p=img.getpixel((i,j))
            gris=0.33*p[0]+0.33*p[1]+0.33*p[2]
            if gris<120:
                imgGris.putpixel((i,j),noir)
            else:
                imgGris.putpixel((i,j),blanc)

# lissage de l'image
def lissageMoyenne(img):
    imgLisse=Image.new(img.mode,img.size)
    colonne,ligne=img.size

    for i in range(1,colonne-1):
        for j in range(1, ligne-1):
            pixel = img.getpixel((i,j))
            moyenne=0
            if pixel[0]==255:
                if pixel[0]==img.getpixel((i,j-1))[0]:
                    moyenne+=1
                else:
                    moyenne-=1
                if pixel[0]==img.getpixel((i-1,j))[0]:
                    moyenne+=1
                else:
                    moyenne-=1
                if pixel[0]==img.getpixel((i,j+1))[0]:
                    moyenne+=1
                else:
                    moyenne-=1
                if pixel[0]==img.getpixel((i+1,j))[0]:
                    moyenne+=1
                else:
                    moyenne-=1

                if moyenne<=0:
                    imgLisse.putpixel((i,j), noir)
                else:
                    imgLisse.putpixel((i,j), blanc)
            else:
                imgLisse.putpixel((i,j), noir)

    return imgLisse

def lissageLocal(img):
    print('lissage')
    imgLisse=img.copy()
    colonne,ligne=img.size

    for i in range(2,colonne-2):
        for j in range(2, ligne-2):
            pixel = img.getpixel((i,j))[:3]
            if pixel==blanc:
                moyenne=0
                for k in range(-2,3):
                    for l in range(-2,3):
                        if img.getpixel((i+k,j+l))[:3]==blanc:
                            moyenne+=1
                if moyenne<12:
                    imgLisse.putpixel((i,j),noir)
                else:
                    imgLisse.putpixel((i,j),blanc)

    return imgLisse

def linearisation(img):
    print('linearisation')
    imgLin=Image.new(img.mode,img.size)
    colonne,ligne=img.size

    nSuite=0

    for i in range(colonne):
        nSuite=0
        for j in range(ligne):
            imgLin.putpixel((i,j),blanc)
            pixel=img.getpixel((i,j))[:3]
            if pixel==noir and j!=ligne-1:
                nSuite+=1
            else:
                if nSuite>=3:
                    if i>0 and i<ligne -1 and imgLin.getpixel((i+1,j-int(nSuite/2)))!=blanc and imgLin.getpixel((i+1,j-int(nSuite/2)))!=blanc:
                        imgLin.putpixel((i,j-int(nSuite/2)),(255,0,0))
                    # if nSuite%2==0:
                    #     imgLin.putpixel((i,min(ligne-1,j-int(nSuite/2)+1)),noir)
                nSuite=0

    for j in range(ligne):
        nSuite=0
        for i in range(colonne):
            pixel=img.getpixel((i,j))[:3]
            if pixel==noir and i!=colonne-1:
                nSuite+=1
            else:
                if nSuite>=3:
                    if j>0 and j<colonne-1 and imgLin.getpixel((i-int(nSuite/2),j-1))!=blanc and imgLin.getpixel((i-int(nSuite/2),j+1))!=blanc:
                        imgLin.putpixel((i-int(nSuite/2),j),(0,255,0))
                    # if nSuite%2==0:
                    #     imgLin.putpixel((min(colonne-1,i-int(nSuite/2)+1),j),noir)
                    # if imgLin.getpixel((i-int(nSuite/2),j))!=noir:
                    #     imgLin.putpixel((i,j),blanc)
                nSuite=0
    return imgLin

def superLinearisation(img):
    print('super linearisation')
    imgLin=Image.new(img.mode,img.size)
    colonne,ligne=img.size

    for i in range(0,ligne):
        for j in range(0, colonne):
            imgLin.putpixel((j,i),blanc)
            pi = img.getpixel((j,i))
            h=0
            v=0
            ki=i
            kj=j
            h1=-1
            h2=-1
            v1=-1
            v2=-1
            if pi[0] == 0:
                while ki >=0 and img.getpixel((j,ki))[0] == 0:
                    h+=1
                    ki-=1
                    h1+=1
                ki=i
                while ki <ligne and img.getpixel((j,ki))[0] == 0:
                    h-=1
                    ki+=1
                    h2+=1

                while kj >=0 and img.getpixel((kj,i))[0] == 0:
                    v+=1
                    kj-=1
                    v1+=1
                kj=j
                while kj<colonne and img.getpixel((kj,i))[0] == 0:
                    v-=1
                    kj+=1
                    v2+=1

                if (v==0 or v==1) and (h1!=0 and h2!=0):
                    imgLin.putpixel((j,i), noir)
                if (h==0 or h==1) and (v1!=0 and v2!=0):
                    imgLin.putpixel((j,i), noir)
    return imgLin

def epaissir(img):
    print('epaissir')
    imgEpais=img.copy()
    colonne,ligne=img.size

    for i in range(1,colonne-1):
        for j in range(1, ligne-1):
            pixel = img.getpixel((i,j))[:3]
            if pixel!=blanc:
                imgEpais.putpixel((i+1,j), noir)
                imgEpais.putpixel((i,j+1), noir)
                imgEpais.putpixel((i-1,j), noir)
                imgEpais.putpixel((i,j-1), noir)

                imgEpais.putpixel((i+1,j+1), noir)
                imgEpais.putpixel((i-1,j+1), noir)
                imgEpais.putpixel((i-1,j-1), noir)
                imgEpais.putpixel((i+1,j-1), noir)
    return imgEpais

def c_connexes(img):
    print("composantes")
    colonne,ligne=img.size
    ptsTraites=[]
    attente=[]
    composante=[]
    num=-1

    for i in range(ligne):
        for j in range(colonne):
            # if (i,j) not in ptsTraites:
            #     ptsTraites.append((i,j))
            if img.getpixel((j,i))==noir and (i,j) not in ptsTraites:
                ptsTraites.append((i,j))
                composante.append([(i,j)])
                num+=1
                attente=[(i,j)]
                while attente != []:
                    a,b=attente.pop(0)
                    for k in range(a-3,a+4):
                        for l in range(b-3,b+4):
                            if k>=0 and l>=0 and k<ligne and l<colonne:# and (a-k)**2+(b-l)**2<=9:
                                # if (k,l) not in ptsTraites:
                                #     ptsTraites.append((k,l))
                                if img.getpixel((l,k))==noir and (k,l) not in ptsTraites:
                                    attente.append((k,l))
                                    composante[num].append((k,l))
                                    ptsTraites.append((k,l))
                if len(composante[num])<20:
                    for i,j in composante[num]:
                        img.putpixel((j,i),(255,255,255,255))
                    composante.pop()
                    num-=1
    return composante

def colorier(img):
    lis=c_connexes(img)
    print("colorier")
    tabCoul=[]
    coul=(random.randint(1,254),random.randint(1,254),random.randint(1,254),255)
    for comp in lis:
        while coul in tabCoul:
            if img.mode=='RGBA':
                coul=(random.randint(1,254),random.randint(1,254),random.randint(1,254),255)
            else:
                coul=(random.randint(1,254),random.randint(1,254),random.randint(1,254))
        tabCoul.append(coul)
        for (i,j) in comp:
            img.putpixel((j,i),coul)

    tab=[]
    for i in range(len(tabCoul)):
        tab.append((lis[i],tabCoul[i]))

    return tab

def barycentre(t):
    tBary=[]
    for comp,coul in t:
        moyx=0
        moyy=0
        for i,j in comp:
            moyx+=i
            moyy+=j
        tBary.append((moyx//len(comp),moyy//len(comp),coul))

    return tBary

def graphe(t,img):
    mVois=[]
    tB=barycentre(t)
    sommets=tB
    for comp,c in t:
        tc=voisins(img,comp,c)
        tcNum=[]
        for j in range(len(tc)):
            for i in range(len(t)):
                if t[i][1]==tc[j]:
                    tcNum.append(i)
        mVois.append(tcNum)
    return sommets,mVois

def voisins(img,comp,c):
    disM=20
    iter=0
    rien=True
    res=[]
    colonne,ligne=img.size

    for i,j in comp:
        while iter<disM and rien:
            iter+=1
            if j+iter<colonne:
                cc=img.getpixel((j+iter,i))
                if cc!=blanc and cc not in res and cc!=c:
                    res.append(cc)
                    rien=False
        iter=0
        rien=True
        while iter<disM and rien:
            iter+=1
            if j-iter>=0:
                cc=img.getpixel((j-iter,i))
                if cc!=blanc and cc not in res and cc!=c:
                    res.append(cc)
                    rien=False
        iter=0
        rien=True
        while iter<disM and rien:
            iter+=1
            if i+iter<ligne:
                cc=img.getpixel((j,i+iter))
                if cc!=blanc and cc not in res and cc!=c:
                    res.append(cc)
                    rien=False
        iter=0
        rien=True
        while iter<disM and rien:
            iter+=1
            if i-iter>=0:
                cc=img.getpixel((j,i-iter))
                if cc!=blanc and cc not in res and cc!=c:
                    res.append(cc)
                    rien=False
    return res

def ligne_def (a,x,x0,y0,img) : #Pour une droite donnée, rend l'ordonnée d'une abscisse donnée
    colonne,ligne = img.size
    y = int(a*(x-x0)+y0)
    return(y)


def get_ligne (a,p1,img) : #donne la liste des points d'une droite de coefficient a et contenant p1
    colonne,ligne = img.size
    (x0,y0) = p1
    L1=[]
    for k in range(colonne) :
        if 0 <= ligne_def (a,k,x0,y0,img) and ligne_def (a,k,x0,y0,img) < (ligne) :
            L1.append((k,ligne_def (a,k,x0,y0,img)))
    n=len(L1)
    if a != 0 :
      k=int(a/abs(a))
    else : a=int(0)
    L2=[]
    for i in range(0,n-1) :
        L2.append(L1[i])
        if L1[i][1] != L1[i+1][1] :
            for j in range(k,L1[i+1][1]-L1[i][1],k) :
                L2.append((L1[i][0],L1[i][1]+j))
    L2.append(L1[-1])
    L3 = []
    if k>0 :
      if (L2[-1][1] != (ligne-1)) and (L2[-1][0] != (colonne-1)) :
        a=L2[-1][0]
        o=L2[-1][1]
        for i in range(1,ligne-L2[-1][1]) :
          L2.append((a,o+i))
      if (L2[0][1] != 0) and (L2[0][0] != 0) :
        a=L2[0][0]
        o=L2[0][1]
        for i in range(o) :
          L3.append((a,0+i))
      L3=L3+L2
    if k<0 :
      if (L2[-1][1] != 0) and (L2[-1][0] != (colonne-1)) :
        a=L2[-1][0]
        o=L2[-1][1]
        for i in range(o-1,-1,-1) :
          L2.append((a,i))
      if (L2[0][1] != (ligne-1)) and (L2[0][0] != 0) :
        a=L2[0][0]
        b=L2[0][1]
        for i in range(ligne-1,b,-1) :
          L3.append((a,i))
      L3=L3+L2
    return(L3)

def print_segment (p1,p2,image) :
    (i1,j1) = p1
    (i2,j2) = p2
    if i1 != i2 :
      a = (j2-j1)/(i2-i1)
    else : a = 5000
    L3=get_ligne(a,p1,image)
    for i in L3 :
        if (i[0] >= min(i1,i2) and i[0] <= max(i1,i2)) and (i[1] >= min(j1,j2) and i[1] <= max(j1,j2)) :
            image.putpixel(i, (0,0,0))

def distance(a,b,x,y):
    return math.sqrt((a-x)**2+(b-y)**2)

def fus(l,k):
    if k==[]:
        return l
    elif l==[]:
        return k
    else:
        if l[0]>k[0]:
            return [l[0]]+fus(l[1:],k)
        else:
            return [k[0]]+fus(l,k[1:])
def triF(l):
    if len(l)<=1:
        return l
    elif len(l)==2:
        if l[0]<l[1]:
            return  [l[1],l[0]]
        else:
            return l
    else:
        m=len(l)//2
        l1=triF(l[:m])
        l2=triF(l[m:])

        return fus(l1,l2)

def ecrireDsBase(lis,nom):
    li=list.copy(lis)
    li=[nom]+li
    fichier=open("/home/usrgaetan/Documents/Fermat/Spe/TIPE/baseEmpreintes2.txt", "a")
    for i in range(len(li)):
        li[i]=str(li[i])
        fichier.write(li[i])
        if i!=len(li)-1:
            fichier.write(',')
    fichier.write('\n')
    fichier.close()

def lireDsBase():
    fichier=open("/home/usrgaetan/Documents/Fermat/Spe/TIPE/baseEmpreintes2.txt", "r")
    lignes=[]
    ligne=fichier.readline()
    ligne=ligne.replace('\n','')
    ligne=ligne.split(',')
    lignes.append(ligne[1:])
    while ligne != '' and ligne!=['']:
        ligne=fichier.readline()
        ligne=ligne.replace('\n','')
        ligne=ligne.split(',')
        # for i in range(len(ligne)):
        #     print(ligne[i])
        #     ligne[i]=float(ligne[i])
        lignes.append(ligne[1:])
    lignes.pop(-1)
    for ligne in lignes:
        for i in range(len(ligne)):
            ligne[i]=float(ligne[i])

    return lignes


def comparer(lis):# ajouter les tests de comoapraison pr les 3
    print("comparer")
    tabLisB=lireDsBase()
    tabR=[]
    for lisB in tabLisB:
        prcent=1
        prcent*=(1-(abs(lis[0]-lisB[0]))/max(lis[0],lisB[0]))**0.2
        prcent*=(1-(abs(lis[1]-lisB[1]))/max(lis[1],lisB[1]))
        prcent*=(1-(abs(lis[2]-lisB[2]))/max(lis[2],lisB[2]))**0.4



        lpct=[]
        for i in range(3,23):
            lpct.append(abs(lis[i]-lisB[i]))
        p=0
        for dif in lpct:
            p+=dif
        p=p/(len(lpct)*max(lpct)+1)**0.5
        prcent*=(1-p)


        lD=[]
        p=0
        for i in range(23,63,2):
            lD.append(abs((lis[i]-lisB[i])**2+(lis[i+1]-lisB[i+1])**2))

        for dif in lD:
            p+=dif
        p=p/(len(lD)*max(lD)+1)**0.5
        prcent*=(1-p)

        lM=[]
        p=0
        for i in range(63,83):
            lM.append(abs(lis[i]-lisB[i]))
        p=0
        for dif in lM:
            p+=dif
        p=p/(len(lM)*max(lM)+1)
        prcent*=(1-p)


        ld=lis[83:].copy()
        ldB=lisB[83:].copy()
        d=len(ld)
        dB=len(ldB)
        m=max(d,dB)

        # while ld !=[]:
        #     j=0
        #     traite=False
        #     while ldB!=[] and j<len(ldB):
        #         if (ld[0]>ldB[j]-10 or ld[0]<ldB[j]+10) and not traite:
        #             ld.pop(0)
        #             ldB.pop(j)
        #             traite=True
        #         j+=1
        #     if not traite:
        #         mauvais.append(ld.pop(0))
        i=0
        js=0
        while i<d:
            traite=False
            for j in range(dB):
                if not traite and (ld[i]<ldB[j]+10 and ld[i]>ldB[j]-10):
                    traite=True
                    ld.pop(i)
                    d-=1
                    js=j
            if traite:
                ldB.pop(js)
                dB-=1
            else:
                i+=1

        n=len(ld)+len(ldB)
        prcent*=abs(n-m)/m
        # print('dis',abs(n-m)/m)

        tabR.append(prcent)
    return tabR


img,nom=init_()
if img.mode=='RGB':
    blanc=(255,255,255)
    noir=(0,0,0)
grisage(img)
img=lissageLocal(img)

for i in range(0):
    img=superLinearisation(img)
    img=epaissir(img)
img=superLinearisation(img)
t=colorier(img)
gr=graphe(t,img)
tBary=barycentre(t)
tabDis=[]

colonne,ligne=img.size
iBar=Image.new(img.mode,img.size)
for i in range(ligne):
    for j in range(colonne):
        iBar.putpixel((j,i),blanc)
for i,j,c in tBary:
    for k in range(i-2,i+3):
        for l in range(j-2,j+3):
            iBar.putpixel((l,k),c)
for i in range(len(gr[1])):
    for j in range(len(gr[1][i])):
        print_segment((tBary[i][1],tBary[i][0]),(tBary[gr[1][i][j]][1],tBary[gr[1][i][j]][0]),iBar)
        tabDis+=[distance(tBary[i][1],tBary[i][0],tBary[gr[1][i][j]][1],tBary[gr[1][i][j]][0])]
tabDis=triF(tabDis)
iBar.show()
iBar.close()
img.show()
img.close()


listeComparaison=[]

# nbre de composantes
listeComparaison.append(len(gr[0]))

#arite max
m=max(len(i) for i in gr[1])
listeComparaison.append(m)

# nbre de triangle
nbT=0
for i in range(len(gr[1])):
    for j in gr[1][i]:
        for k in gr[1][j]:
            for l in gr[1][k]:
                if i==l:
                    nbT+=1
listeComparaison.append(nbT/3)

# print(listeComparaison)

# nbre de voisins des sommets
nbV=[0 for i in range(20)]
ariS=[[] for i in range(20)]
a=0
aTot=0
for l in gr[1]:
    if len(l)<20:
        nbV[len(l)]+=1
        aTot+=1
        ariS[len(l)].append(a)
    a+=1
prcentV=[nbV[i]/aTot for i in range(20)]
for i in prcentV:
    listeComparaison.append(i)
# bary des degres
baryDeg=[]
imgB=Image.new(img.mode,img.size)
for i in range(imgB.size[0]):
    for j in range(imgB.size[1]):
        imgB.putpixel((i,j),blanc)
for l in ariS:
    moyX=0
    moyY=0
    i=0
    for b in l:
        moyX+=tBary[b][0]
        moyY+=tBary[b][1]
        i+=1
    if i!=0:
        baryDeg.append([moyX//i,moyY//i])
        for k in range(-2,3):
            for l in range(-2,3):
                imgB.putpixel((baryDeg[-1][1]+k,baryDeg[-1][0]+l),(random.randint(1,254),random.randint(1,254),random.randint(1,254)))
for i in baryDeg:
    listeComparaison.append(i[0])
    listeComparaison.append(i[1])

imgB.show()
imgB.close()

# moyenne du nombre de voisins des voisins
moyV=[0 for i in range(20)]
totV=[0 for i in range(20)]

for l in gr[1]:
    for v in l:
        moyV[len(l)]+=len(gr[1][v])
    totV[len(l)]+=len(l)
for i in range(len(moyV)):
    if totV[i]!=0:
        moyV[i]=moyV[i]/totV[i]
for i in moyV:
    listeComparaison.append(i)
# distance entre les sommets
for d in tabDis:
    listeComparaison.append(d)

# ecrireDsBase(listeComparaison,nom)
comparer(listeComparaison)



