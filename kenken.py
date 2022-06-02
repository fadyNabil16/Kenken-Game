from time import time
import csp
from sys import stderr, stdin
from itertools import product, permutations
from functools import reduce
from random import seed, random, shuffle, randint, choice
from time import time
from csv import writer


def operation(operator):
    #mapping between the string symbol and the matmatical operation 
    
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

def adjacent(xy1, xy2): #check if the two point is adjacent or not like(1,2),(1,1)
  
    x1, y1 = xy1
    x2, y2 = xy2

    dx, dy = x1 - x2, y1 - y2

    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

def generate(size):
    #this function is responsilble for creating the random board 
    
    #steps: 
    #1- create a square with size equal size anl fill it with numbers from 1 to size

    board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]
    #2- shuffle the board to get some type of randomness 
    for _ in range(size):
        shuffle(board)

    for c1 in range(size):
        for c2 in range(size):
            if random() > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    board = {(i + 1, j+ 1): board[i][j] for i in range(size) for j in range(size)}
    
    #3- Initialize the 'uncaged' set with all cell coordinates
    
    uncaged = sorted(board.keys(), key=lambda var: var[1])  #set
    cliques = []
    while uncaged:
       
        cliques.append([])
        
        #4- initilize cage size with random it from 1 to 4 
        csize = randint(1, 4)
        
        #5- put the first cell from the "uncaged" set in the cliques set and remove it from the uncaged cell 
        cell = uncaged[0]
        uncaged.remove(cell)

        cliques[-1].append(cell)
        #6- loop for the cage size -1 times and repeat the previous steps 
        for _ in range(csize - 1):

            adjs = [other for other in uncaged if adjacent(cell, other)]

            cell = choice(adjs) if adjs else None

            if not cell:
                break

            uncaged.remove(cell)
            
            cliques[-1].append(cell)
            
        csize = len(cliques[-1])
        # 7- according to the cage size do the operation 
        """
        8- is csize == 1 , there is no operation just make the target equal to the element of the clique
        else if csize == 2 check
            if the clique can be divided without a remainder , set te operation to devision 
            if the clique can be divided with a remainder , set te operation to subtraction 
        else if csize >=2  choose random operation from addition or multiplication 
        
        """
        if csize == 1:
            cell = cliques[-1][0]
            cliques[-1] = ((cell, ), '.', board[cell])
            continue
        elif csize == 2:
            fst, snd = cliques[-1][0], cliques[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/" 
            else:
                operator = "-" 
        else:
            operator = choice("+*")

        target = reduce(operation(operator), [board[cell] for cell in cliques[-1]])

        cliques[-1] = (tuple(cliques[-1]), operator, int(target))

    return size, cliques
#----------------------------------------------------------------------

def validate(size, cliques):
    #checking for any problem:
   

    outOfBounds = lambda xy: xy[0] < 1 or xy[0] > size or xy[1] < 1 or xy[1] > size

    mentioned = set()
    for i in range(len(cliques)):
        members, operator, target = cliques[i]

        cliques[i] = (tuple(set(members)), operator, target)

        members, operator, target = cliques[i]
        # 1- check if the opertator is not "+-*/."
        if operator not in "+-*/.":
            print("Operation", operator, "of clique", cliques[i], "is unacceptable", file=stderr)
            exit(1)
        # 2- check if the clique member is out of the bound 
        problematic = list(filter(outOfBounds, members))
        if problematic:
            print("Members", problematic, "of clique", cliques[i], "are out of bounds", file=stderr)
            exit(2)
        problematic = mentioned.intersection(set(members))
        if problematic:
            print("Members", problematic, "of clique", cliques[i], "are cross referenced", file=stderr)
            exit(3)

        mentioned.update(set(members))

    indexes = range(1, size + 1)

    problematic = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)
    
    # 3- check if the clique member is  mentioned in any other clique 
    if problematic:
        print("Positions", problematic, "were not mentioned in any clique", file=stderr)
        exit(4)

def RowXorCol(xy1, xy2):
    # return true if the two cells in the same raw or in the same column 
    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])

def conflicting(A, a, B, b):
   
    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if RowXorCol(mA, mB) and ma == mb:
                """"
                if RowXorCol(mA, mB) evaluates to true and 
                the value of mA in 'assignment' a is equal to the value of mb in 'assignment' b

                """
                return True   
            
    return False

def satisfies(values, operation, target):
  
    for p in permutations(values):
        if reduce(operation, p) == target:
            return True

    return False

def gdomains(size, cliques):
    """
    @ https://docs.python.org/2/library/itertools.html
    @ product('ABCD', repeat=2) = [AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD]

    For every clique in cliques:
        * Initialize the domain of each variable to contain every product
        of the set [1...board-size] that are of length 'clique-size'.
        For example:

            board-size = 3 and clique-size = 2

            products = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

        * Discard any value (assignment of the members of the clique) that:
        * is resulting in the members of the clique 'conflicting' with each other
        * does not 'satisfy' the given operation
    """
    domains = {}
    for clique in cliques:
        members, operator, target = clique

        domains[members] = list(product(range(1, size + 1), repeat=len(members)))
        #Discard any value does not 'satisfy' the given operation
        
        qualifies = lambda values: not conflicting(members, values, members, values) and satisfies(values, operation(operator), target)

        domains[members] = list(filter(qualifies, domains[members]))

    return domains

def gneighbors(cliques):
  
    neighbors = {}
    for members, _, _ in cliques:
        neighbors[members] = []

    for A, _, _ in cliques:
        for B, _, _ in cliques:
            if A != B and B not in neighbors[A]:
               #if they are probable to 'conflict' they are considered neighbors 
                if conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors

class Kenken(csp.CSP): #create kenken class inherite from csp class

    def __init__(self, size, cliques):
       
        validate(size, cliques)
        
        variables = [members for members, _, _ in cliques]
        
        domains = gdomains(size, cliques)

        neighbors = gneighbors(cliques)

        csp.CSP.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size

        self.checks = 0

        # Used in displaying
        self.padding = 0

        self.meta = {}
        for members, operator, target in cliques:
            self.meta[members] = (operator, target)
            self.padding = max(self.padding, len(str(target)))        


    def constraint(self, A, a, B, b):
        #check for the constriants 
        #if any two variables in the same cli. or the same row must not have the same value
      
        self.checks += 1

        return A == B or not conflicting(A, a, B, b)

    def display(self, assignment):
        #print the kenken board we use it for debuggig 
        if assignment:
            atomic = {}
            for members in self.variables:
                values = assignment.get(members)

                if values:
                    for i in range(len(members)):
                        atomic[members[i]] = values[i]
                else:
                    for member in members:
                        atomic[member] = None
        else:
            atomic = {member:None for members in self.variables for member in members}

        atomic = sorted(atomic.items(), key=lambda item: item[0][1] * self.size + item[0][0])

        padding = lambda c, offset: (c * (self.padding + 2 - offset))

        embrace = lambda inner, beg, end: beg + inner + end

        mentioned = set()

        def meta(member):
            for var, val in self.meta.items():
                if member in var and var not in mentioned:
                    mentioned.add(var)
                    return str(val[1]) + " " + (val[0] if val[0] != "." else " ")

            return ""

        fit = lambda word: padding(" ", len(word)) + word + padding(" ", 0)

        cpadding = embrace(2 * padding(" ", 0), "|", "") * self.size + "|"

        def show(row):

            rpadding = "".join(["|" + fit(meta(item[0])) for item in row]) + "|"

            data = "".join(["|" + fit(str(item[1] if item[1] else "")) for item in row]) + "|"

            print(rpadding, data, cpadding, sep="\n")

        rpadding = embrace(2 * padding("-", 0), "+", "") * self.size + "+"

        print(rpadding)
        for i in range(1, self.size + 1):

            show(list(filter(lambda item: item[0][1] == i, atomic)))

            print(rpadding)



if __name__ == "__main__":

    board_num = 1
    generate_num = 7
    time1 = time()
    for i in range(board_num):
        size, cliques = generate(generate_num)

        ken = Kenken(size, cliques)
        
        assignment = csp.backtracking_search(ken, inference=csp.no_inference)
        #for  inference write forward_checking for forward cheching and mac for arc consistency 
        
        ken.display(assignment)
       
    time2 = time()
    print(time1)
    print(time2)
    print("time = ", (time2-time1))
