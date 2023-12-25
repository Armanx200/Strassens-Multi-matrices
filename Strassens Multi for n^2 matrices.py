from math import ceil, log
from optparse import OptionParser


def read(filename):
    lines = open(filename).read().splitlines()
    A = []
    B = []
    matrix = A
    for line in lines:
        if line != "":
            matrix.append([int(el) for el in line.split("\t")])
        else:
            matrix = B
    return A, B


def print_matrix(matrix):
    for line in matrix:
        print("\t".join(map(str, line)))


def ikj_matrix_product(A, B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def add(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] + B[i][j]
    return C


def subtract(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def strassenR(A, B):
    n = len(A)

    if n <= LEAF_SIZE:
        return ikj_matrix_product(A, B)
    else:
        new_size = n // 2
        a11 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        a12 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        a21 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        a22 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]

        b11 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        b12 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        b21 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        b22 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]

        aResult = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        bResult = [[0 for j in range(0, new_size)] for i in range(0, new_size)]

        for i in range(0, new_size):
            for j in range(0, new_size):
                a11[i][j] = A[i][j] 
                a12[i][j] = A[i][j + new_size]
                a21[i][j] = A[i + new_size][j]
                a22[i][j] = A[i + new_size][j + new_size]

                b11[i][j] = B[i][j]
                b12[i][j] = B[i][j + new_size]
                b21[i][j] = B[i + new_size][j]
                b22[i][j] = B[i + new_size][j + new_size]

        aResult = add(a11, a22)
        bResult = add(b11, b22)
        p1 = strassenR(aResult, bResult) 

        aResult = add(a21, a22)
        p2 = strassenR(aResult, b11)

        bResult = subtract(b12, b22)
        p3 = strassenR(a11, bResult)

        bResult = subtract(b21, b11)
        p4 = strassenR(a22, bResult)

        aResult = add(a11, a12)
        p5 = strassenR(aResult, b22)

        aResult = subtract(a21, a11)
        bResult = add(b11, b12)
        p6 = strassenR(aResult, bResult)

        aResult = subtract(a12, a22)
        bResult = add(b21, b22)
        p7 = strassenR(aResult, bResult)

        c12 = add(p3, p5)
        c21 = add(p2, p4) 

        aResult = add(p1, p4)
        bResult = add(aResult, p7)
        c11 = subtract(bResult, p5)

        aResult = add(p1, p3)
        bResult = add(aResult, p6)
        c22 = subtract(bResult, p2)

        C = [[0 for j in range(0, n)] for i in range(0, n)]
        for i in range(0, new_size):
            for j in range(0, new_size):
                C[i][j] = c11[i][j]
                C[i][j + new_size] = c12[i][j]
                C[i + new_size][j] = c21[i][j]
                C[i + new_size][j + new_size] = c22[i][j]
        return C


def strassen(A, B):
    assert type(A) == list and type(B) == list
    assert len(A) == len(A[0]) == len(B) == len(B[0])

    nextPowerOfTwo = lambda n: 2 ** int(ceil(log(n, 2)))
    n = len(A)
    m = nextPowerOfTwo(n)
    APrep = [[0 for i in range(m)] for j in range(m)]
    BPrep = [[0 for i in range(m)] for j in range(m)]
    for i in range(n):
        for j in range(n):
            APrep[i][j] = A[i][j]
            BPrep[i][j] = B[i][j]
    CPrep = strassenR(APrep, BPrep)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = CPrep[i][j]
    return C


#---------------Main---------------#
parser = OptionParser()
parser.add_option(
    "-i",
    dest="filename",
    default="2000.in",
    help="input file with two matrices",
    metavar="FILE",
)
parser.add_option(
    "-l",
    dest="LEAF_SIZE",
    default="8",
    help="when do you start using ikj",
    metavar="LEAF_SIZE",
)
(options, args) = parser.parse_args()

LEAF_SIZE = int(options.LEAF_SIZE)


    
A = [[1,2,3,4]
    ,[5,6,7,8]
    ,[9,10,11,12]
    ,[13,14,15,16]]

B = [[1,2,3]
    ,[1,2,3]
    ,[1,2,3]]
C = strassen(B, B)
print_matrix(C)
