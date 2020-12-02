import random

def create_sym_matr(size, def_d_val=None, rd_seed=1, mode="dist"):
    numerator = random.random()
    options = {
        "dist": lambda: random.randint(1,10),
        "pher": lambda: numerator/1000000,
        "delta_pher": lambda: 0
    }
    random.seed(rd_seed)
    matr = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            if i<j:
                matr[i][j] = matr[j][i] = options[mode]()
            elif i==j:
                matr[i][i] = def_d_val
    return matr


def create_matrix_with_sparse_vals(rows, cols, upper_border, population_percentage, rd_seed=1):
    random.seed(rd_seed)
    if population_percentage > 0.5 or population_percentage < 0.01:
        raise ValueError("population_percentage > 0.5 or population_percentage < 0.01")

    matr = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            matr[i][j] = random.randint(-upper_border, upper_border)

    absolute_num = round((1-population_percentage)*rows*cols)
    y = random.randint(0, rows-1)
    x = random.randint(0, cols-1)
    visited_coords = set()
    for i in range(absolute_num):
        while (x, y) in visited_coords:
            y = random.randint(0, rows-1)
            x = random.randint(0, cols-1)
        matr[y][x] = 0
        visited_coords.add((x, y))
    
    sym_matrix_print(matr, rows)

    return matr


def sym_matrix_print(matrix, size):
    print("[")
    for row in range(size):
        print("\t", matrix[row])
    print("]")

if __name__ == '__main__':
    print("="*20)
    print("Module demonstration\n")
    print("Input matrix size: ")
    size = int(input())
    default = input("Input default matrix main diagonal value: ")
    m = create_sym_matr(size, default)
    print("\n[")
    for i in range(size): print("\t", m[i])
    print("]\n")
    print("="*20)