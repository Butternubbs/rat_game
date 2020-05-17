calls = 0

def solve_puzzle (clues):
    matrix = [[[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]],
              [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]],
              [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]],
              [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]],
              [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]],
              [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]]]
    all_perms = []
    heapPermutation([1,2,3,4,5,6], 6, 6, all_perms)
    solved = False
    while not solved:
        for c in range(len(clues)):
            perms = generate_possible_perms(clues[c], clues[inverse(c)], get_rowcol(c, matrix), all_perms)
            for i in range(6):
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
                for j in range(6):
                    if j not in indices:
                        matrix = remove_option(matrix, c, j, i+1)
                if works:
                    matrix = change_matrix(matrix, c, i, start)
        
        solved = True
        for row in matrix:
            for group in row:
                if len(group) > 1:
                    solved = False
        print(matrix[0])
        print(matrix[1])
        print(matrix[2])
        print(matrix[3])
        print(matrix[4])
        print(matrix[5])
    matrix = (tuple(matrix[0][0]+matrix[0][1]+matrix[0][2]+matrix[0][3]+matrix[0][4]+matrix[0][5]),
              tuple(matrix[1][0]+matrix[1][1]+matrix[1][2]+matrix[1][3]+matrix[1][4]+matrix[1][5]),
              tuple(matrix[2][0]+matrix[2][1]+matrix[2][2]+matrix[2][3]+matrix[2][4]+matrix[2][5]),
              tuple(matrix[3][0]+matrix[3][1]+matrix[3][2]+matrix[3][3]+matrix[3][4]+matrix[3][5]),
              tuple(matrix[4][0]+matrix[4][1]+matrix[4][2]+matrix[4][3]+matrix[4][4]+matrix[4][5]),
              tuple(matrix[5][0]+matrix[5][1]+matrix[5][2]+matrix[5][3]+matrix[5][4]+matrix[5][5]))
    return matrix

def inverse(clue):
    if clue < 12:
        if clue < 6:
            return 17 - clue
        else:
            return 29 - clue
    else:
        if clue < 18:
            return 17 - clue
        else:
            return 29 - clue

def remove_option(matrix, clue, depth, to):
    
    if clue < 6:
        row = depth
        col = clue
    elif clue > 5 and clue < 12:
        row = clue%6
        col = 5-depth
    elif clue > 11 and clue < 18:
        row = 5-depth
        col = 5-(clue%6)
    else:
        row = 5-(clue%6)
        col = depth
    if to in matrix[row][col]:
        matrix[row][col].remove(to)
    return matrix

def change_matrix(matrix, clue, depth, to):
    if clue < 6:
        row = depth
        col = clue
    elif clue > 5 and clue < 12:
        row = clue%6
        col = 5-depth
    elif clue > 11 and clue < 18:
        row = 5-depth
        col = 5-(clue%6)
    else:
        row = 5-(clue%6)
        col = depth
    for i in range(6):
        if to in matrix[row][i]:
            matrix[row][i].remove(to)
        if to in matrix[i][col]:
            matrix[i][col].remove(to)
    matrix[row][col] = [to]
    return matrix

def get_rowcol(clue, matrix):
    if clue < 6:
        return [x[clue] for x in matrix]
    elif clue > 5 and clue < 12:
        return matrix[clue%6][::-1]
    elif clue > 11 and clue < 18:
        return [x[5-(clue%6)] for x in matrix][::-1]
    else:
        return matrix[5-(clue%6)]

def generate_possible_perms(clue, inverse, data, all_perms):
    ap = all_perms[:]
    for perm in all_perms[:]:
        perminv = perm[::-1]
        highest = 0
        highestinv = 0
        count = 0
        countinv = 0
        for i in range(6):
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

print(solve_puzzle(( 0, 3, 0, 5, 3, 4, 
          0, 0, 0, 0, 0, 1,
          0, 3, 0, 3, 2, 3,
          3, 2, 0, 3, 1, 0)))
print(calls)