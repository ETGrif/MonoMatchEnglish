import anagramDistance as ad
import networkx as nx
import itertools
import math

outFile = "monomatches.txt"

##helper for reversing the anagram map
def deAnagram(anagramMap, anagrams):
    #basis
    if len(anagrams)==1:
        return [[x] for x in anagramMap[anagrams[0]]]
    
    #append a word to each possible list from deAnagram(anagrams[1:])
    words = anagramMap[anagrams[0]]
    list = deAnagram(anagramMap, anagrams[1:])
    newList = []
    for l in list:
        for w in words:
            c = l.copy()
            c.append(w)
            newList.append(c)
    return newList

#load in file and create anagram dict

anagramMap = ad.makeAnagramMap(wordFile="CleanWordsSmaller.txt")
anagrams = list(anagramMap.keys())
print("Anagram Family Made")
#create graph of all anagrams of distance 1
G = nx.Graph()

pairs= list(itertools.combinations(anagrams, 2))
edges = list(filter(lambda x : ad.isMonoMatch(x[0], x[1]), pairs))
G.add_edges_from(edges)
print("Graph made")

d = [x[1] for x in list(G.degree())]
k1 = sum(d)/len(d)
print(f"Size: {len(G.nodes)}, Avg Degree: {k1}, Density:{nx.density(G)}")

# k=21
# G2 = nx.k_core(G,k=21)
# print(f"k-Core (k={k}) Found")
# d= [x[1] for x in list(G2.degree)]
# k2 = sum(d)/len(d)
# print(f'Size: {len(G2.nodes)}, Avg Degree: {k2}')
G2 = G

print("Beginning Clique Search")
maximalCliques = list(nx.find_cliques(G2))

if(len(maximalCliques)==0):
    print("No cliques found")
else:   
    lens = [len(x) for x in maximalCliques]
    maxSize = max(lens)
    maximalCliques = list(filter(lambda x: len(x)==maxSize, maximalCliques))
    print(f"Found {len(maximalCliques)}, of max length {maxSize}")
    print("Generating monoMatches from anagrams")
    
    # generate monomatches using the anagramMap
    monomatches = []
    for m in maximalCliques:
        # monomatches.append([anagramMap[x][0] for x in m])
        monomatches.extend(deAnagram(anagramMap, m))
        
    
    with open(outFile, "w") as file:
        for c in monomatches:
            file.write(str(c) + "\n")
    print(f"Results Published to {outFile}")



    
