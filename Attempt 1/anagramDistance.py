#this script should find the enlgish word (with single use letters) that is the fewest changes away from a given string (anagrams allowed)

import string

enlishWordsFile = 'wordleWords.txt'
n = 5
blist = []

def blacklist(letter):
    blist.append(letter)
    
def clearBlist():
    blist.clear()

def makeAnagramMap(wordFile, n):
    #first, find all enhish words of length 5
    words = set()
    with open(enlishWordsFile) as fin:
        lines = fin.read().splitlines()
        for s in lines:
            if len(s) == n:
                words.add(s.lower())
                
                
    #remove the ones with repreated letters
    newWords = words.copy()
    for s in words:
        count = 0
        for checkChar in s:
            for char in s:
                if char == checkChar:
                    count+=1
        if count != n:
            newWords.remove(s)
        
    #generate map of anagrams
    anagramMaps = dict()
    for s in newWords:
        fam = ''.join(sorted(s))
        if fam in anagramMaps.keys():
            anagramMaps[fam].append(s)
        else:
            anagramMaps[fam] = [s]
    
    return anagramMaps
        
def findAnagramDistance(word, anagram):
    a, b, doable = stringDifference(word, anagram);
    if not doable: return -1
    return len(a)
    
def stringDifference(a, b):
    delete, insert = [],[]
    a = list(a)
    b = list(b)
    for e in b: insert.append(e)
    
    for i in a:
        if i.lower() in b:
            insert.remove(i.lower())
        else:
            delete.append(i)
            
    doable = True
    for i in delete:
        if not i.islower() or i in blist:
            doable = False
    for i in insert:
        if i in blist:
            doable = False
    return (delete, insert, doable)

