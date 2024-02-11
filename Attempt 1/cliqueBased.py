import time
import datetime
import os



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
crashProtectionFile = "crashProtection.txt"
        
def main():
    
    nodes = createNodes("wordleWordsSmall.txt")
    print("Completed graph import")
    
    #create the initial state stack
    maxClique = set()
    stateStack = []
    maxValStack = []
    foundSets = []
    newMaxFound = False
    prevSeed = ""
    totalCounted = 0
    totalSeeds = 0
    
    for node in nodes:
        newSet = set()
        newSet.add(node)
        stateStack.append(newSet)
        maxValStack.append(node.name)
        
    if os.path.exists(crashProtectionFile):
        #This is a crash recovery runthrough
        #remove previous seeds from the state stack (except the last one in the list)
        with open(crashProtectionFile, "r") as cpIn:
            lines = cpIn.read().splitlines()
            del lines[0]
            for n in stateStack:
                if list(n)[0].name in lines:
                    stateStack.remove(n)
                    maxValStack.remove(list(n)[0].name)
        
        with open(crashProtectionFile, "a") as cpOut:
            cpOut.write(f"Session recovered at {datetime.datetime.now().isoformat()}\n")
            
        #recover a set to compare against for writing to the files
        with open(outFile, "r") as ofIn:
            line = ofIn.read().splitlines()
            maxClique = set(line[1][1:-1].split(", "))
        
        
    else:
        with open(crashProtectionFile, "x") as cpOut:
            cpOut.write(f"Session started at {datetime.datetime.now().isoformat()}\n")

        
    while(len(stateStack) > 0):
        #make one pass in the state stack
        curClique = stateStack.pop()
        curCliqueMaxVal = maxValStack.pop()
        if len(curClique) == 1:
            print(f"Starting from new seed {list(curClique)[0].name}")
            #write the previous completed seed to the crash protection file
            with open(crashProtectionFile, "a") as cpOut:
                if prevSeed != "":
                    cpOut.write(prevSeed + "\n")
                prevSeed = list(curClique)[0].name
            
            #TODO: write the previous words
            writeSetsToOutFile(foundSets, newMaxFound)
            foundSets.clear()
            newMaxFound = False
                
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
            if n.name < curCliqueMaxVal: continue #This line enforces a weak ordering
            curClique.add(n)
            stateStack.append(curClique.copy())
            maxValStack.append(n.name)
            #here we will also update the max if necessary
            if(len(maxClique) < len(curClique)): 
                print(f'Max EMS found: {maxClique}')
                maxClique = curClique.copy()
                foundSets.clear()
                foundSets.append(maxClique.copy())
                newMaxFound = True
            elif(len(maxClique) == len(curClique)):
                if(verbose):
                    print(f'Equiv EMS found: {curClique}')
                foundSets.append(curClique.copy())
            curClique.remove(n)
        
        
    print(maxClique)
    
    #close the crash recovery file
    # os.remove(crashProtectionFile)
    
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

def writeSetsToOutFile(cliques, newMax):
    type = "w" if newMax else "a"
    with open(outFile, type) as out:
        if newMax:
            out.write(str(len(list(cliques)[0])))
        for clique in cliques:
            out.write("\n" + str(clique))

start = time.time()   
main()
end = time.time()
print(f"Took {end - start} seconds.")
            