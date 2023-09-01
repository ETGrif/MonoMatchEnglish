import time


class Node:
    def __init__(self, name):
        self.name = name
        self.adjacencies = set()
        
        #search bits
        self.visited = False
        self.parent = "-no-parent-"
    
    def __eq__(self, other):
        return self.name == other.name
        
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return self.name
    
    def add_edge_to(self, n):
        self.add_adjacency(n)
        n.add_adjacency(self)
    
    def add_adjacency(self, n):
        self.adjacencies.add(n)
        
    def connects_to(self, n):
        count = 0
        for a in self.name:
            for b in n.name:
                if a == b:
                    count += 1
        return count == 1
                

verbose = False
outFile = "longestSet.txt"
        
def main():
    
    nodes = createNodes("wordleWordsSmall.txt")
    print("Completed graph import")
    
    #create the initial state stack
    maxClique = set()
    stateStack = []
    maxValStack = []
    totalCounted = 0
    totalSeeds = 0
    for node in nodes:
        newSet = set()
        newSet.add(node)
        stateStack.append(newSet)
        maxValStack.append(node.name)
        
    while(len(stateStack) > 0):
        #make one pass in the state stack
        curClique = stateStack.pop()
        curCliqueMaxVal = maxValStack.pop()
        if len(curClique) == 1:
            print("Starting from new seed")
            totalSeeds += 1
        totalCounted += 1
        
        
        #find the common neighborhood
        comNeighborhood = nodes
        for n in curClique:
            comNeighborhood = comNeighborhood.intersection(n.adjacencies)
        
        #print about backtracking
        if verbose:
            print(f'Backtrack   seeds:total {totalSeeds}:{totalCounted}')
        
        #push the next possible clique steps
        for n in comNeighborhood:
            if n.name < curCliqueMaxVal: continue
            #TODO: This is where an ordering would need to be implemented.. Not sure how to do that yet
            curClique.add(n)
            stateStack.append(curClique.copy())
            maxValStack.append(n.name)
            #here we will also update the max if necessary
            if(len(maxClique) < len(curClique)): 
                maxClique = curClique.copy()
                print(f'Max EMS found: {maxClique}')
                with open(outFile, "w") as out:
                    out.write(len(maxClique))
                    out.write(str(maxClique))
            elif(len(maxClique) == len(curClique)):
                print(f'Equiv EMS found: {curClique}')
                with open(outFile, "a") as out:
                    out.write("\n" + str(curClique))
            curClique.remove(n)
        
        
    print(maxClique)
        
    
def createNodes(file):
    nodes = set()
    
    with open(file) as fin:
        lines = fin.read().splitlines()
        for line in lines:
            if(len(line) != 5): continue
            count = 0
            for checkChar in line:
                for char in line:
                    if char == checkChar:
                        count+=1
            if count == 5:
                newNode = Node(line)
                for n in nodes:
                    if n.connects_to(newNode):
                        n.add_edge_to(newNode)
                nodes.add(newNode)
    return nodes



start = time.time()   
main()
end = time.time()
print(f"Took {end - start} seconds.")
            