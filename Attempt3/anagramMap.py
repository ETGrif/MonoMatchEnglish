def make_anagram_map(file):
    words = set()
    #read in the file
    with open(file) as fin:
        lines = fin.read().splitlines()
        for l in lines:
            addLine = True
            #filter words
            l = l.lower()
            if len(l) != 5: addLine = False
            
            #check if letters are unique
            letters=[]
            for c in l:
                if c in letters: addLine = False
                letters.append(c)
            
            if addLine:
                words.add(l)
    
    anagramMap = dict()
    #for each word
    for w in words:
        #find family
        anagramFamily = ''.join(sorted(w))
        
        #update or create entry in map
        if anagramFamily in anagramMap.keys():
            anagramMap[anagramFamily].append(w)
        else:
            anagramMap[anagramFamily] = [w]

    return anagramMap