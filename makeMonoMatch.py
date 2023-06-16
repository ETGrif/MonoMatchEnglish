# this script is to create the list of monomatch strings (to be remapped later).
import string

n = 5 # this is the side length of the square to be used

alph = string.ascii_lowercase
alph = alph[0:pow(n,2)]


#find all the horizontal ones
for i in range(n):
    mono = alph[n*i:n*i+n]
    print(mono)
    
#find the other ones
for s in range(n): #s is the 'slope' of the matching line
    for i in range(n): #i is the starting index
        ind = i
        row = 0
        mono = ""
        while row < n:
            mono += alph[n*row + ind]
            ind = (ind + s) % n
            row += 1
        
        print(mono)
        
    

