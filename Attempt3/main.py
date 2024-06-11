import multiprocessing.spawn
import anagramMap as am
import monoStructure as ms
import random as rand
import multiprocessing
from exceptions import OverrestrictedError
import os

anagramMap = am.make_anagram_map("Attempt3\wordleWords.txt")
debug = False

def find_mono_match():
    mono = ms.MonoStruct()


    while True:
        monoAvail = [] #set of letters availble to restrict to for each mono
        
        #find the letters available to each mono
        for i, m in enumerate(mono.loose):
            monoAvail.append(set())
            for w in anagramMap.keys():
                #for each word and mono pair, check if word is possible
    
                if not mono.word_is_restricted(w, m[0]):
                #word is possible. Find the letters that work
                    for l in w:
                        #dont consider if::
                        #the letter is in the tightened alphabet
                        if l not in mono.tightenedAlph:
                            monoAvail[i].update(l) #adds each letter possible 

        #count the outcomes possible for each var char pair:
        # pairs[var][int(char)]
        pairs = [[0 for i in range(len(mono.looseAlph))] for j in range(21)]
        
        for i, m in enumerate(mono.loose):
            #find the loose vars
            looseVars = []
            for l in m[0]:
                if l not in mono.tightenedAlph:
                    looseVars.append(l)
                    
            #for each loose var, update that row of pairs
            for v in looseVars:
                v = int(v) -1#so it can be used for an index
                for l in monoAvail[i]:
                    #find the index of the character
                    lInd = mono.looseAlph.index(l)
                    pairs[v][lInd] += 1

        
        #sort into buckets
        pairsWithCount = [[] for i in range(6)]
        for v in range(21):
            for l in range(len(mono.looseAlph)):
                count = pairs[v][l]
                pairsWithCount[count].append((v+1, mono.looseAlph[l]))
        

        #pick the list of pairs of highest count
        maxInd = 5
        while len(pairsWithCount[maxInd])==0:
            maxInd -=1
         
        # END CONDITION
        if maxInd == 0:
            break
         
        #pick a random pair from this list
        (v, l) = rand.choice(pairsWithCount[maxInd])
        
        #restrict it
        mono.restrict(v, l)
        
            
            
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
                        out.write(str(len(found)) + "\n" + str(found)+ " ["+str(discard)+"]\n")
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