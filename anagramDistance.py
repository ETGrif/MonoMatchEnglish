#this script should find the enlgish word (with single use letters) that is the fewest changes away from a given string (anagrams allowed)

import string

enlishWordsFile = 'words_alpha.txt'
n = 5
def makeAnagramMap(wordFile, n):
    #first, find all enhish words of length 5
    words = set()
    with open(enlishWordsFile) as fin:
        lines = fin.read().splitlines()
        for s in lines:
            if len(s) == n:
                words.add(s)
                
                
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
    wordFam = ''.join(word.sort())
    anaFam = ''.join(word.sort())
    return levenshteinDistance(wordFam, anaFam)
    
def stringDifference(a, b):
    delete, insert = [],[]
    a = list(a)
    b = list(b)
    for e in b: insert.append(e)
    
    for i in a:
        if i in b:
            insert.remove(i)
        else:
            delete.append(i)
            
    doable = True
    for i in delete + insert:
        if not i.islower():
            doable = False
    return (delete, insert, doable)

print(stringDifference("abcde", "xcvbn"))
