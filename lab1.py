import numpy as np
from numpy.linalg import inv
import math



###values###
A = np.array([  [   3,  2,  1,  0   ],
                [   -3, 2,  0,  1   ]   ])
c = np.array([  0,  1,  0,  0   ])
b = np.array([  6,  0  ])
###values###



def fast_inversion(A_inv, x, i):
    
# first step
    l = np.dot(A_inv, x)

    if l[i] == 0:
        raise Exception("Matrix is not inversible")
    
# second - third step
    tmp = l[i]
    l[i] = -1
    l *= -1 / tmp

# fourth - fifth step
    result = np.empty(A_inv.shape)
    for (rowIndex, row) in enumerate(A_inv):
        for (colIndex, element) in enumerate(row):
            result[rowIndex, colIndex] = A_inv[i, colIndex] * l[rowIndex]
            if rowIndex != i:
                result[rowIndex, colIndex] += element
    
    return result


#основная фаза симплекс метода
def method(A, c, x, B):

# first step
    Ab = A[:, B]

    try:
        Ab_inv = inv(Ab)
    except np.linalg.LinAlgError:
        raise Exception("Problem is infeasable!")

    while True:
        
    # second step
        cb = c[B]

    # third step
        u = np.dot(cb, Ab_inv)

    # fourth step
        Delta = np.dot(u, A) - c

    # fifth step
        if (Delta >= 0).all():
            return x, B
        
    # sixth step
        j0 = np.argwhere(Delta < 0)[0, 0]

    # seventh step
        z = np.dot(Ab_inv, A[:, j0])

    # eigth step
        Tetta = x[B] / z
        Tetta[z <= 0] = np.inf

    # ninth - thirteenth step
        k = np.argmin(Tetta)
        Tetta0 = Tetta[k]

        if Tetta0 == np.inf:
            return None

        for i, j in enumerate(B):
            x[j] -= Tetta0 * z[i]

        B[k] = j0
        x[j0] = Tetta0

    # first step
        new_col = A[:, j0]
        Ab[:, k] = new_col
        Ab_inv = fast_inversion(Ab_inv, new_col, k)


#начальная фаза симплекс метода
def starting_method(A, b):
    n = A.shape[1]
    m = A.shape[0]

    # first step
    A[b < 0] = -A[b < 0]

    # second - third step
    tmp_c = np.concatenate((np.zeros(n), np.full(m, -1)))
    tmp_A = np.concatenate((A, np.identity(m)), 1)
    tmp_x = np.concatenate((np.zeros(n), b))
    tmp_B = np.array(range(n, n + m))

    # fourth step
    tmp_x, tmp_B = method(tmp_A, tmp_c, tmp_x, tmp_B)

    # fifth step
    if (tmp_x[n:] != 0).any():
        raise Exception("Problem is infeasable!")

    # sixth step
    x = tmp_x[:n]

    AB_inv = inv(tmp_A[:,tmp_B])
    new_A = A
    new_b = b

    while True:
        jk_index = np.argmax(tmp_B)
        jk = tmp_B[jk_index]
        i = jk - n

        # seventh step
        if jk < n:
            return x, tmp_B, new_A, new_b
        
        l = np.dot(AB_inv, new_A)
        nonzero_indexes = np.nonzero(l[jk_index,:])[0]
        nonzero_indexes = np.setdiff1d(nonzero_indexes[nonzero_indexes < n], tmp_B)

        if nonzero_indexes.size == 0:

            # nineth step
            new_A = np.delete(new_A, i, 0)
            new_b = np.delete(new_b, i, 0)
            tmp_B = np.delete(tmp_B, jk_index, 0)
            tmp_A = np.delete(tmp_A, i, 0)
            AB_inv = inv(tmp_A[:,tmp_B])

        else:

            # tenth step
            j = nonzero_indexes[0]
            tmp_B[jk_index] = j
            fast_inversion(AB_inv, new_A[:,j], jk_index)


def simplex(A, c, b):
    x, B, A, b = starting_method(A, b)
    return method(A, c, x, B)


def brace_function(value):
    return value - int(value)


def generate_gom(A, x, B):
    for index, component in enumerate(x):
        if int(component) != component:
            k = np.where(B == index)[0]

            Ab_inv = inv(A[:, B])
            NotB = np.array([_ for _ in filter(lambda x : x not in B, np.arange(x.size))])
            Q = np.dot(Ab_inv, A[:, NotB])
            l = Q[k]

            brace_function = lambda x: x - math.floor(x)

            result = np.zeros(x.size + 1)
            result[NotB] = np.array([_ for _ in map(brace_function, l[0])])
            result[-1] = -1

            return result, brace_function(component)
    
    return None


def main():
    simplex_result = simplex(A, c, b)
    
    if (simplex_result is None):
        print("Problem has no bounds")

    gom = generate_gom(A, *simplex_result)

    if (gom is None):
        print(f"Result: {simplex_result[0]}")

    print(*gom)


if __name__ == "__main__":
    main()