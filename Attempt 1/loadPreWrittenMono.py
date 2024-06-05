import random as rand
import string

def getMonoMatches(n):
    if n != 5:
        print("Error: oof, try the other mono match system, but also fix it first")
    alph = string.ascii_lowercase
    with open("Attempt 1\onenmore.txt") as fin:
        lines = fin.read().splitlines()
        words = set()
        for e in lines: words.add(e)
        
        #scramble the letters up a bit
        for i in range(100):
            a = rand.choice(alph)
            b = rand.choice(alph)
            newMonoMatch = set()
            for w in words:
                newMonoMatch.add(w.replace(a, "+").replace(b, a).replace("+", b))
            words.clear()
            words = newMonoMatch
            
    
    return words
            

            
    