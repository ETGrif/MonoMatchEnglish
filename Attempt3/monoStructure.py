import string
from exceptions import OverrestrictedError

class MonoStruct:
    def __init__(self):
        self.loose = read_file("Attempt3\monomatch_structure.txt")
        self.restricted = []
        
        self.looseAlph = list(string.ascii_lowercase)
        self.tightenedAlph = []
        self.tightenedNum = []
    
    def restrict(self, num: int, char: string):
        num = str(num)
        #check if the letter has already been restricted
        if num in self.tightenedNum:
            raise OverrestrictedError(f'Number {num} has already been restricted.', num)
        if char in self.tightenedAlph:
            raise OverrestrictedError(f'Char {char} has already been restricted.', char)
        
        #for each loose list, switch
        
        fullyTightened = []
        for l in self.loose:
            if num in l[0]:
                l[0].remove(num)
                l[0].append(char)
                l[1]-=1 # decrement the number of loose variables in this list
                if l[1] == 0:
                    fullyTightened.append(l) #tag to update loose lists, so we dont get a loop skip
                
        
        #update the loose and tightened lists
        for l in fullyTightened:
            self.restricted.append(l[0])
            self.loose.remove(l)
        
        self.looseAlph.remove(char)
        self.tightenedAlph.append(char)
        self.tightenedNum.append(num)
        
            
    def word_is_restricted(self, word, mono): #Returns True if not allowed 
        #check if the word has restricted letters that are not in the list
        for w in word: 
            if w in self.tightenedAlph:
                if w not in mono:
                    return True
        #check i fthe word has all restricted letters in the list
        for m in mono:
            if m in self.tightenedAlph:
                if m not in word:
                    return True
                
        return False
        
       
        
    
def read_file(file):
    
    with open(file) as fin:
        lines = fin.read().splitlines()
        structure = []
        for l in lines:
            l = l.split(" ")
            structure.append([l, len(l)])
        return structure