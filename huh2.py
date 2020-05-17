calls = 0

def solve_puzzle (clues):
    matrix = [[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]],
              [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]],
              [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]],
              [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]]
    all_perms = []
    heapPermutation([1,2,3,4], 4, 4, all_perms)
    solved = False
    while not solved:
        for c in range(len(clues)):
            perms = generate_possible_perms(clues[c], clues[inverse(c)], get_rowcol(c, matrix), all_perms)
            for i in range(4):
                indices = []
                start = perms[0][i]
                works = True
                for perm in perms:
                    if i+1 in perm:
                        if not perm.index(i+1) in indices:
                            indices.append(perm.index(i+1))
                    if not perm[i] == start:
                        works = False
                indices.sort()
                for j in range(4):
                    if j not in indices:
                        matrix = remove_option(matrix, c, j, i+1)
                if works:
                    matrix = change_matrix(matrix, c, i, start)
        
        solved = True
        for row in matrix:
            for group in row:
                if len(group) > 1:
                    solved = False
    matrix = (tuple(matrix[0][0]+matrix[0][1]+matrix[0][2]+matrix[0][3]),
              tuple(matrix[1][0]+matrix[1][1]+matrix[1][2]+matrix[1][3]),
              tuple(matrix[2][0]+matrix[2][1]+matrix[2][2]+matrix[2][3]),
              tuple(matrix[3][0]+matrix[3][1]+matrix[3][2]+matrix[3][3]))
    return matrix

def inverse(clue):
    
    if clue < 8:
        if clue < 4:
            return 11 - clue
        else:
            return 19 - clue
    else:
        if clue < 12:
            return 11 - clue
        else:
            return 19 - clue

def remove_option(matrix, clue, depth, to):
    global calls
    calls += 1
    if clue < 4:
        row = depth
        col = clue
    elif clue > 3 and clue < 8:
        row = clue%4
        col = 3-depth
    elif clue > 7 and clue < 12:
        row = 3-depth
        col = 3-(clue%4)
    else:
        row = 3-(clue%4)
        col = depth
    if to in matrix[row][col]:
        matrix[row][col].remove(to)
    return matrix

def change_matrix(matrix, clue, depth, to):
    if clue < 4:
        row = depth
        col = clue
    elif clue > 3 and clue < 8:
        row = clue%4
        col = 3-depth
    elif clue > 7 and clue < 12:
        row = 3-depth
        col = 3-(clue%4)
    else:
        row = 3-(clue%4)
        col = depth
    for i in range(4):
        if to in matrix[row][i]:
            matrix[row][i].remove(to)
        if to in matrix[i][col]:
            matrix[i][col].remove(to)
    matrix[row][col] = [to]
    return matrix

def get_rowcol(clue, matrix):
    if clue < 4:
        return [x[clue] for x in matrix]
    elif clue > 3 and clue < 8:
        return matrix[clue%4][::-1]
    elif clue > 7 and clue < 12:
        return [x[3-(clue%4)] for x in matrix][::-1]
    else:
        return matrix[3-(clue%4)]

def generate_possible_perms(clue, inverse, data, all_perms):
    ap = all_perms[:]
    for perm in all_perms[:]:
        perminv = perm[::-1]
        highest = 0
        highestinv = 0
        count = 0
        countinv = 0
        for i in range(4):
            if perm[i] > highest:
                highest = perm[i]
                count += 1
            if perminv[i] > highestinv:
                highestinv = perminv[i]
                countinv += 1
            if not perm[i] in data[i]:
                if perm in ap:
                    ap.remove(perm)
        if not clue == 0 and not count == clue:
            if perm in ap:
                ap.remove(perm)
        if not inverse == 0 and not countinv == inverse:
            if perm in ap:
                ap.remove(perm)
    return ap
  
def heapPermutation(a, size, n, perms):
    if (size == 1):
        perms.append(list(a))
        return
  
    for i in range(size): 
        heapPermutation(a,size-1,n, perms); 
  
        if size&1: 
            a[0], a[size-1] = a[size-1],a[0] 
        else: 
            a[i], a[size-1] = a[size-1],a[i]  

print(solve_puzzle((0, 0, 1, 2, 
                    0, 2, 0, 0,
                    0, 3, 0, 0,
                    0, 1, 0, 0)))
print(calls)