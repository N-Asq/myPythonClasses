#!/usr/bin/python3
# coding: utf-8
# Comprendre la surcharge d''opérateurs et maîtriser les classes et les méthodes spéciales
from copy import deepcopy

class Duration:
    """
        Class to play with durations. Each time the object is modified, it is reformated so that it is human readable.
        Basic operations (+,-) supported with Duration and int.

    """    
    def __init__(self,dd=0,HH=0,MM=0,SS=0,_sign=True): # On passe par object, pour ne pas passer par self.__setattr__()
        object.__setattr__(self,"dd",dd)
        object.__setattr__(self,"HH",HH)
        object.__setattr__(self,"MM",MM)
        object.__setattr__(self,"SS",SS)
        self._format()
    
    def __setattr__(self,attr,valAttr): # A chaque fois qu'un attribut est modifié, on reformate
        object.__setattr__(self,attr,valAttr)
        self._format()

    def __delattr__(self,attr): # La suppression d'un attribut est impossible, à la place, on le met à 0
        object.__setattr__(self,attr,0)

    def _format(self): # Appelée à chaque instanciation et calcul, permet de formater la durée de manière humainement lisible
        NAtom = self.SS + self.MM*60 + self.HH*60*60 + self.dd*60*60*24 # On calcule la durée dans le plus petite unité possible
        object.__setattr__(self,"_sign",NAtom >= 0) # Si elle est négative, on le précise dans l'attribut _sign qui vaudra False (True sinon)
        if not self._sign: # Et on revient à une valeur positive pour travailler normalement
            NAtom = -NAtom 
        object.__setattr__(self,"dd",NAtom//(60*60*24))
        NAtom = NAtom%(60*60*24)
        object.__setattr__(self,"HH",NAtom//(60*60))
        NAtom = NAtom%(60*60)
        object.__setattr__(self,"MM",NAtom//(60))
        NAtom = NAtom%(60)
        object.__setattr__(self,"SS",NAtom)
        NAtom = NAtom

    def __add__(self,objToTreat): # Si on ajoute quelque chose        
        # Durée négative ou pas
        newDuration = deepcopy(self) # On copie l'objet dans une nouvelle instance
        if newDuration._sign:
            signNewDuration = 1
        else:
            signNewDuration = -1
        
        if isinstance(objToTreat,Duration): # Si l'objet à ajouter est une durée
            if objToTreat._sign:
                signObject = 1
            else:
                signObject = -1
            # On additionne tout en prenant en compte les signes des deux durées
            object.__setattr__(newDuration,"dd",newDuration.dd*signNewDuration + objToTreat.dd*signObject)
            object.__setattr__(newDuration,"HH",newDuration.HH*signNewDuration + objToTreat.HH*signObject)
            object.__setattr__(newDuration,"MM",newDuration.MM*signNewDuration + objToTreat.MM*signObject)
            object.__setattr__(newDuration,"SS",newDuration.SS*signNewDuration + objToTreat.SS*signObject)
        elif isinstance(objToTreat,int): # Si c'est un int, on l'ajoute aux secondes
            object.__setattr__(newDuration,"SS",newDuration.SS*signNewDuration + objToTreat)

        newDuration._format() # On est passé par la classe objet pour faire les attributions et ne pas avoir à formater à chaque fois mais il faut quand même le faire à la fin
        return newDuration
    
    def __radd__(self,objToTreat): # Addition commutative, pas de souci
        return self + objToTreat

    def __sub__(self,objToTreat): # On revient à une addition en mettant un moins devant l'objet à ajouter 
        if isinstance(objToTreat,Duration):
            object.__setattr__(objToTreat,"_sign",not objToTreat._sign)  # Changement de signe si c'est une durée
        elif isinstance(objToTreat,int):
            objToTreat = -objToTreat
        return self + objToTreat

    def __rsub__(self,objToTreat): # On fait la soustraction inverse et on change le signe (a-b) = -(b-a)
        newDuration = self - objToTreat
        object.__setattr__(newDuration,"_sign",not newDuration._sign)
        return newDuration

    def __repr__(self): # Affichage dans l'interpréteur
        if self._sign:
            return("({0} days, {1} hours, {2} minutes, {3} seconds)".format(self.dd,self.HH,self.MM,self.SS))
        else:
            return("-({0} days, {1} hours, {2} minutes, {3} seconds)".format(self.dd,self.HH,self.MM,self.SS))

    def __str__(self): # Affichage avec print      
        if self._sign:
            return("({0} days, {1:02}:{2:02}:{3:02})".format(self.dd,self.HH,self.MM,self.SS))
        else:
            return("-({0} days, {1:02}:{2:02}:{3:02})".format(self.dd,self.HH,self.MM,self.SS))
    
if __name__ == "__main__":
    print("Tests :")

    print("\nCréation de t1 : 1 jour + 32 h -128 min + 256 sec ")
    t1 = Duration(1,32,-128,256)
    print(t1)

    print("\nCréation de t2 : -1 jour - 45 h + 63 min + 20 sec ")
    t2 = Duration(-1,-45,63,20)
    print(t2)

    print("\nt1 + t2 =",t1+t2)

    print("\n50 + t1 =",50+t1)

    print("\nt1 + 50 =",t1+50)

    print("\nSuppression des heures de t1")
    del(t1.HH)
    print(t1)

    print("\n50 - t1 =",50-t1)

    print("\nt1 - 50 =",t1-50)

