#!/usr/bin/python3
# coding: utf-8

class smartDict():
    """
        Class which works as an organized and sortable dictionnary.
        Can be instatiate with sd = smartDict([unnamedParam,key0=value0,...,keyN=valueN])
        Where:
            -unnamedParam are parameters which will be ignored unless they are dict or smartDict. 
            If it is the case, their keys and values will be used to the created smartDict.
            -keyX is a key in the created smartDict and valueX its corresponding value.
        Note that during instantiation, if there are identical keys along the parameters passed, 
        the priority will go to the named key, then to the first dictionnary in the otherParams, etc... 
    """
    def __init__(self,*unnamedParam,**namedParam):
        # On commence par créer des dictionnaires vides
        self._keyList = list()
        self._valueList = list()
        # On ajoute le dico constitué des paramètres nommés
        self.addDict(namedParam)
        # On ajoute les dicos contenus dans les paramètres non nommés (on ignore les autres paramètres)
        notDictFlag = False
        for param in unnamedParam: 
            if isinstance(param,dict) or isinstance(param,smartDict):
                self.addDict(param)
            else:
                notDictFlag = True
        if notDictFlag:
            print("Warning. Unnamed argument(s) of type different from smartDict or dict have been ignored during instantiation.")

    def addDict(self,dico): 
            """ 
                Adds the dictionnary or smartDictionnary dico to the smartDict.
            """ 
            if isinstance(dico,dict) or isinstance(dico,smartDict):
                addedKeyList = [key for (key,value) in dico.items() if key not in self._keyList]
                addedValueList = [value for (key,value) in dico.items() if key not in self._keyList]
                self._keyList.extend(addedKeyList)
                self._valueList.extend(addedValueList)
            else:
                raise TypeError("The addition only works with another dict or smartDict.")
    
    def getIndex(self,arg):
        """
            Returns the index of an item of key "arg".  
            Returns None if the key doesn't exist.
            If "arg" is already an int, checks if it is in bound and returns itself. 
        """
        if isinstance(arg,str):
            # L'argument est une clé
            if arg in self._keyList:
                # La clé existe
                index = self._keyList.index(arg)
            else:
                index = None
        elif isinstance(arg,int):
            # L'argument est déjà un index.
            if arg in range(-len(self._keyList),len(self._keyList)):
                # L'index est correctement défini
                index = arg
            else:
                raise IndexError("smartDict index out of range") 
        else:
            # L'argument n'est pas valide
            raise TypeError("The argument must be a key (str) or an index (int)")
        return index

    def sort(self):
        """
            Sort the smartDict by keys
        """
        newIndices = [x[0] for x in sorted(enumerate(self._keyList),key=lambda x:x[1])]
        self._keyList = [self._keyList[index] for index in newIndices]
        self._valueList = [self._valueList[index] for index in newIndices]
    
    def reverse(self):
        """
            Reverse the smartDict
        """
        self._keyList.reverse()
        self._valueList.reverse()

    def keys(self):
        """
            Returns the keys like the dict.keys method 
        """
        return [key for (index,key,value) in self._browseDict()]
    
    def values(self):
        """
            Returns the values like the dict.values method 
        """
        return [value for (index,key,value) in self._browseDict()]

        
    def items(self):
        """
            Returns the (key,value) tuples like the dict.items method 
        """
        return [(key,value) for (index,key,value) in self._browseDict()]

    
    def _browseDict(self):
        """
            Generator to return the (index,key,value) tuples of the smartDict
        """
        index = 0
        while index < len(self._keyList):
            yield (index,self._keyList[index],self._valueList[index])
            index += 1

    def __getitem__(self,arg):
        """
            Returns the value of an item of key or index "arg".
        """
        index = self.getIndex(arg)
        if index is None:
            raise KeyError(arg) 
        return self._valueList[index]

    def __setitem__(self,arg,value):
        """
            Sets the value of an item of key or index "arg" to "value".
            Creates the item if the key doesn't exist.
        """
        index = self.getIndex(arg)
        if index is None:
            # Si la clé n'existe pas, on la créée
            self._keyList.append(arg)
            self._valueList.append(value)
        else:
            # Sinon on la modifie
            self._valueList[index] = value

    def __delitem__(self,arg):
        """
            Deletes the item of key or index "arg".
        """
        index = self.getIndex(arg)
        if index is not None:
            del(self._keyList[index])
            del(self._valueList[index])

    def __add__(self,thing):
        from copy import deepcopy
        newSmartDict = deepcopy(self)
        newSmartDict.addDict(thing)
        return newSmartDict

    def __radd__(self,thing):
        return self+thing

    def __contains__(self,key):
        if not isinstance(key,str):
            raise TypeError("The key must be a string.")
        return key in self._keyList

    def __len__(self):
        return len(self._keyList)

    def __repr__(self): 
        tupleStr = " | ".join(["["+str(index)+"] "+key+": "+str(value) for index,key,value in self._browseDict()])
        return(tupleStr)
    
    def __str__(self): 
        return(repr(self))
        


if __name__ == "__main__":
    print("Tests :")
    aliments = {"fraises": 113,"melons":7,"pommes":30}

    print("\nCréation avec conflit de clés:")
    fruits = smartDict(aliments,bananes = 26,pommes = 17,mangue = 12) 
    print(fruits)

    print("\nSuppression de clé:")
    del(fruits["pommes"])
    print(fruits)

    print("\nModification de valeur:")
    fruits["fraises"] = 121
    print(fruits)

    print("\nAjout de clé:")
    fruits["pommes"] = 13
    print(fruits)

    print("\nVérification avec in:")
    if "pommes" in fruits:
        print("Les pommes sont là.")

    print("\nAddition d'un dict:")
    fruits = fruits + {"peches": 16, "pasteques":2}
    print(fruits)

    print("\nAddition d'un smartDict:")
    fruits = fruits + smartDict(framboises=89)
    print(fruits)

    print("\nInversement du smartDict:")
    fruits.reverse()
    print(fruits)

    print("\nTriage par clés:")
    fruits.sort()
    print(fruits)

help(smartDict)