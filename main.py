import random as rand
import loadPreWrittenMono as mm
import anagramDistance as ad


def findMatches():
    n=5
    monoMatches = mm.getMonoMatches(n)
    anagramMap = ad.makeAnagramMap('words_alpha.txt', n)
    anagrams = anagramMap.keys()
    found = set()

    while(True):
        #find the monoMatch with lowwest distance to an anagram family
        minDist = float('inf')
        minMonoMatch = ''
        minAnagram = ''
        for m in monoMatches:
            for a in anagrams:
                diff = ad.findAnagramDistance(m, a)
                if diff >= 0 and diff < minDist:
                    minDist = diff
                    minMonoMatch = m
                    minAnagram = a
                    
        #Check for halting condition:
        if minMonoMatch=='':
            ad.clearBlist()
            return found
        
        #remove the chosen monomatch from the list of new considerations
        monoMatches.remove(minMonoMatch)

        #remap letters letters (do this with random pairings to allow for monte carlo optimization later on)
        delete, insert, temp = ad.stringDifference(minMonoMatch, minAnagram)
        others = []
    #make sure to include the lower case direct match ups so that they get capitalized
        for l in minMonoMatch:
            if l not in delete and l.islower():
                others.append(l)
                # others.append(l)
        for d in delete:
            #pick what it will be swapped with
            i = rand.choice(insert)
            insert.remove(i)
            #make sure its blacklisted from future remaps
            ad.blacklist(i)
            
            newMonoMatches = set()
            #for all monoMatches, replace all lower case d with capital i
            #as well as all lower case i with lower case d
            # i -> '+'   d -> I   '+'  -> d
            for mono in monoMatches:
                newMono = mono.replace(i, '+').replace(d,i.upper()).replace('+', d)
                newMonoMatches.add(newMono)
                # newMonoMatches.add(mono.replace(d,i.upper()))
            monoMatches = newMonoMatches

        # make sure that letters that need to be capitalized that happened to already match are dealt with
        for l in others:
            newMonoMatches = set()
            for mono in monoMatches:
                newMonoMatches.add(mono.replace(l, l.upper()))
            monoMatches = newMonoMatches
            #dont forget to blacklist the letter from future remaps
            ad.blacklist(l)

        #pick random word from the mono match
        word = rand.choice(anagramMap[''.join(sorted(minAnagram.lower()))])
        found.add(word)


largestSet = set()
while(True):
    found = findMatches()
    if(len(found) > len(largestSet)):
        print("New largest EMS found!")
        largestSet = found
        print(found)
        
        with open("longestSet.txt", "w") as out:
            for i in largestSet:
                out.write(i+"\n")
    else:
        print(f'found {len(found)}')
        