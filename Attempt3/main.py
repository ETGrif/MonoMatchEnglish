import multiprocessing.spawn
import anagramMap as am
import monoStructure as ms
import random as rand
import multiprocessing
from exceptions import OverrestrictedError
import os

anagramMap = am.make_anagram_map("Attempt3\wordleWords.txt")
debug = True

def find_mono_match():
    mono = ms.MonoStruct()

    while True:
        # find most restrictive monomatch
        restrictions = [[] for i in mono.loose]
        for i in range(len(restrictions)):
            m = mono.loose[i][0] #actually grab the mono
            for f in anagramMap.keys():
                #check if the word works, and then add to the lists
                if not mono.word_is_restricted(f,m):
                    restrictions[i].append(f)


        #pick the mono with most restrictions
        minInds = []
        minLen = 100000
        for i in range(len(restrictions)):
            if len(restrictions[i]) < minLen and len(restrictions[i]) > 0:
                minInds = [i]
                minLen = len(restrictions[i])
            elif len(restrictions[i]) == minLen:
                minInds.append(i)
    

        #if this results in no possible restrictions for the current state of mono, then the loop ends
        if minInds == []:
            break
        
        p=.10
        # minInds = rand.choices([minInds, list(range(len(restrictions)))], [p, 1-p])[0]
        
        #with probability p, chose any other viable mono to restrict
        if rand.choices([True, False], [p, 1-p]):
            minInds = [i for i, x in enumerate(restrictions) if len(x)>0]
        
        minInd = rand.choice(minInds) #if there are equally restricted
        
        
                
        
        # pick a possible match at random to restrict to
        word = rand.choice(restrictions[minInd])
        #find the loose letters, and shuffle them
        looseLetters = []
        for w in word:
            if w in mono.looseAlph:
                looseLetters.append(w)
        rand.shuffle(looseLetters)

        #find the loose variables
        looseVars = []
        for m in mono.loose[minInd][0]:
            if m not in mono.tightenedAlph:
                looseVars.append(m)

        #restrict them
        for v, l in zip(looseVars, looseLetters):
            mono.restrict(v,l)
            
            
    #from here on, we have a known, valid monomatch set, but need to solve for anagrams

    #TODO technically we can look for all possible monomatch sets using this set of anagrams.
    monomatchset = set()
    discardCount = 0
    for letters in mono.restricted:
        family = ''.join(sorted(letters))
        if family in anagramMap.keys(): 
            #some extra restrictions will be created by fully restricting other words, but might not have a family associated with it
            word = rand.choice(anagramMap[family])
            monomatchset.add(word)
        else:
            discardCount += 1
        
    return monomatchset, discardCount


def run_search(globalMax, lock, endCond, i):
    #repeatedly search for monomatches, saving the largest
    localMax = 0
    
    while(True):
        #check the end condition
        if bool(endCond.value):
            exit()
        
        try:
            found, discard = find_mono_match()
            
            if(len(found) > localMax):
                #verify check global max
                lock.acquire() #lock that shit down
                if len(found) > globalMax.value: #we are higher than the Global max
                                
                    print(f"New largest EMS found! {len(found)} ["+str(i)+"]")
                    globalMax.value = len(found)
                    localMax = globalMax.value
                    print(found)
                    
                    with open("longestSet.txt", "w") as out:
                        # for i in largestSet:
                        #     out.write(i+"\n")
                        out.write(str(len(found)) + "\n" + str(found)+ " ["+str(discard)+"] \n")
                else:
                    #the new found set was larger than the local, but not the global max
                    localMax = globalMax.value
                
                lock.release() #release the global Max
                
            elif len(found) == localMax:
                lock.acquire() #CRITICAL SECTION LOCK
                
                if localMax == globalMax.value:
                    print(f'found {len(found)}: (Additional) ['+str(i)+']')
                    
                    
                    with open("longestSet.txt", "a") as out:
                        out.write(str(found)+" ["+str(discard)+"]\n")
                else:
                    #the local max isnt aligned with the global
                    localMax = globalMax.value
                        
                lock.release() #CRITICAL SECTION RELEASE
    
            else:
                # print(f'found {len(found)}')
                pass
        except OverrestrictedError as e:
            print(f"The Bug happened...  [{e.args[1]}]")
            print(e.args[0])
            exit()
            # print(e.args[0])
        
if __name__ == "__main__":
    
    processeses = []
    
    #global max semaphore
    globalMax = multiprocessing.Value("i")
    globalMax.value = 0
    
    #lock
    lock = multiprocessing.Lock()
    
    #end condition
    endCond = multiprocessing.Value("i")
    endCond.value = 0
    
    #build processes
    num_jobs = multiprocessing.cpu_count() if not debug else 1
    for i in range(num_jobs):
                
        #build process
        processeses.append(multiprocessing.Process(target = run_search, args = (globalMax, lock, endCond, i)))
        
        #launch process
        processeses[i].start()
        print(f"Process {i} started.")
    
    
    #wait time
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
        
    
    endCond.value = 1 #trigger end condition in children processes
    #wait for processes
    for i, p in enumerate(processeses):
        p.join()
        print(f"Process {i} finished.")
        
    
    print("All processes Finished")