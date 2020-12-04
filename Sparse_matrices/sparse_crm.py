import matr_create as m_c

class SparseCRM():
    def __init__(self):
        self.AN = [] #массив ненулевых элементов
        self.NR = [] #массив индексов по AN следующих элекментов каждой строки
        self.NC = [] #массив индексов по AN следующих элекментов каждого столбца
        self.JR = [] #массив индексов по AN первых элементов строк
        self.JC = [] #массив индексов по AN первых элементов стобцов
    
    def _find_y_coord(self, ind_from_AN): #метод для поиска строковой координаты по индексу из AN
        if ind_from_AN in self.JR:
            y = self.JR.index(ind_from_AN)
        else:
            while ind_from_AN not in self.JR:
                ind_from_AN = self.NR[ind_from_AN]
            y = self.JR.index(ind_from_AN)
        return y
    
    def _find_x_coord(self, ind_from_AN): #метод для поиска столбцовой координаты по индексу из AN
        if ind_from_AN in self.JC:
            x = self.JC.index(ind_from_AN)
        else:
            while ind_from_AN not in self.JC:
                ind_from_AN = self.NC[ind_from_AN]
            x = self.JC.index(ind_from_AN)
        return x

    def print_info(self):
        print("AN:", self.AN)
        print("NR:", self.NR)
        print("NC:", self.NC)
        print("JR:", self.JR)
        print("JC:", self.JC)

    def pack(self, matrix):
        flag_JR = False
        rows = len(matrix)
        cols = len(matrix[0])
        temp_row_index = [] #создаем временный массив для хранения координат по AN значений в строках матрицы
        temp_col_matrix = [[-1 for i in range(rows)] for j in range(cols)] #создаем временную матрицу для хранения координат по AN значений в столбцах - построчно
        flags_JC = [False for i in range(cols)] #создаем список с флагами для фиксации первых элементов в столбцах
        self.JC = [-1 for i in range(cols)]
        for i in range(rows):
            flag_JR = False
            for j in range(cols):
                elem = matrix[i][j]
                if elem == 0:
                    continue #пропускаем нулевые элементы
                else:
                    self.AN.append(elem)
                    AN_index = len(self.AN)-1
                    temp_row_index.append(AN_index)
                    temp_col_matrix[j][i] = AN_index
                    if not flag_JR: #заносим индекс по AN первого элемента строки в JR
                        self.JR.append(AN_index)
                        flag_JR = True
                    if not flags_JC[j]: #заносим индекс по AN первого элемента столбца в JC
                        flags_JC[j] = True
                        self.JC[j] = AN_index
            temp_row_index = temp_row_index[1:]+temp_row_index[:1] #закольцовываем ссылки на каждый последующий элемент строки
            self.NR.extend(temp_row_index)
            temp_row_index = []
            if not flag_JR: #если в строке нет ненулевых элементов, заносим в JR -1
                self.JR.append(-1)

        self.NC = [-1 for i in range(len(self.NR))] #заполняем массив self.NC
        for col_elem_index_lst in temp_col_matrix:
            col_elem_index_lst = [index for index in col_elem_index_lst if index != -1]
            tmp_col_elem_index_lst = col_elem_index_lst[1:]+col_elem_index_lst[:1]
            for enm, ind in enumerate(col_elem_index_lst):
                self.NC[ind] = tmp_col_elem_index_lst[enm]

    def unpack(self, verbose=False):
        rows = len(self.JR)
        cols = len(self.JC)
        unpack_matrix = [[0 for i in range(cols)] for j in range(rows)] #инициализируем распакованную матрицу элементами 0
        for ind in range(len(self.AN)):
            y = self._find_y_coord(ind)
            x = self._find_x_coord(ind)
            unpack_matrix[y][x] = self.AN[ind]
        if verbose: #вывести матрицу на печать
            m_c.sym_matrix_print(unpack_matrix, rows)
        return unpack_matrix

    def addition_fail2(self, matrix):
        res_matrix = SparseCRM()
        if (len(self.JR) != len(matrix.JR)) or (len(self.JC) != len(matrix.JC)): #проверяем размерность
            raise ValueError("(self.JR != matrix.JR) or (self.CR != matrix.CR)")
        res_matrix.JR = [-1 for i in self.JR] #инициализируем массив с индексами первых элементов строк значением -1
        res_matrix.JC = [-1 for i in self.JC] #инициализируем массив с индексами первых элементов столбцов значением -1
        kStrok = len(self.JR) #записываем количество строк
        kStolb = len(self.JC) #записываем количество столбцов
        N_1 = len(self.AN) #записываем количество ненулевых элементов матрицы-первого слагаемого (self)
        N_2 = len(matrix.AN) #записываем количество ненулевых элементов матрицы-второго слагаемого (matrix)
        N_res = 0 #счетчик числа элементов в res_matrix.AN и одновременно указатель на последний элемент
        kB = 0 #указатель на индекс массива AN матрицы-первого слагаемого (self)
        kC = 0 #указатель на индекс массива AN матрицы-второго слагаемого (matrix)

        for i in range(kStrok): #цикл по строкам от 0 до kStrok-1
            y1 = self._find_y_coord(kB)
            y2 = matrix._find_y_coord(kC)
            y1_new = None
            y2_new = None
            while True:
                print("="*8)
                x1 = self._find_x_coord(kB)
                x2 = matrix._find_x_coord(kC)
                print("x1: {}\ty1: {}\ty1_new: {}\nx2: {}\ty2: {}\ty2_new: {}\nkB: {}\nkC: {}\nres_matrix.AN: {}".format(x1,y1, y1_new,x2,y2,y2_new,kB,kC,res_matrix.AN))
                print()
                if x1 != x2: #ЗДЕСЬ ПЕРВАЯ ЗВЕЗДОЧКА!!!
                    print("=> x1 != x2", end="  ")
                    if x2 > x1: #перепишем элемент из self.AN, на который указывает kB, в res_matrix.AN, поскольку он оказалеся непарным и "стоит левее"
                        print("x2 > x1")
                        res_matrix.AN.append(self.AN[kB])
                        kB += 1
                    elif x1 > x2: #перепишем элемент из matrix.AN, на который указывает kC, в res_matrix.AN, поскольку он оказалеся непарным и "стоит левее"
                        print("x1 > x2")
                        res_matrix.AN.append(matrix.AN[kC])
                        kC += 1
                else:
                    print("=> x1 == x2")
                    elem_sum = self.AN[kB] + matrix.AN[kC]
                    if elem_sum: #если сумма элементов ненулевая
                        res_matrix.AN.append(elem_sum) #ЗДЕСЬ ВТОРАЯ ЗВЕЗДОЧКА!!!!
                    kB += 1
                    kC += 1
                y1_new = self._find_y_coord(kB)
                y2_new = matrix._find_y_coord(kC)
                print()
                print("x1: {}\ty1: {}\ty1_new: {}\nx2: {}\ty2: {}\ty2_new: {}\nkB: {}\nkC: {}\nres_matrix.AN: {}".format(x1,y1, y1_new,x2,y2,y2_new,kB,kC,res_matrix.AN))
                if (y1 != y1_new and y2 != y2_new):#if (kB == self.JR[i] and kC == matrix.JR[i]): #if (i != kStrok-1) and (kB == self.JR[i+1] and kC == matrix.JR[i+1]):
                    print("BREAK rowborder")
                    break
                elif kB == N_1 and kC == N_2:
                    print("BREAK matrixend")
                    break
            print("NEW ROW")
            #while (kB != self.JR[i] and kC != matrix.JR[i]) and (kB != N_1 or kC != N_2):
        
        print()
        
        res_matrix.print_info()

    def addition_fail(self, matrix):
        res_matrix = SparseCRM()
        if (len(self.JR) != len(matrix.JR)) or (len(self.JC) != len(matrix.JC)): #проверяем размерность
            raise ValueError("(self.JR != matrix.JR) or (self.CR != matrix.CR)")
        res_matrix.JR = [-1 for i in self.JR] #инициализируем массив с индексами первых элементов строк значением -1
        res_matrix.JC = [-1 for i in self.JC] #инициализируем массив с индексами первых элементов столбцов значением -1
        kStrok = len(self.JR) #записываем количество строк
        kStolb = len(self.JC) #записываем количество столбцов
        N_1 = len(self.AN) #записываем количество ненулевых элементов матрицы-первого слагаемого (self)
        N_2 = len(matrix.AN) #записываем количество ненулевых элементов матрицы-второго слагаемого (matrix)
        N_res = 0 #счетчик числа элементов в res_matrix.AN и одновременно указатель на последний элемент
        kB = 0 #указатель на индекс массива AN матрицы-первого слагаемого (self)
        kC = 0 #указатель на индекс массива AN матрицы-второго слагаемого (matrix)

        for i in range(kStrok): #цикл по строкам от 0 до kStrok-1
            while (kB != self.JR[i] and kC != matrix.JR[i]) and (kB != N_1 or kC != N_2):
                x1 = self._find_x_coord(kB)
                x2 = matrix._find_x_coord(kC)
                if x1 != x2: #ЗДЕСЬ ПЕРВАЯ ЗВЕЗДОЧКА!!!
                    print("=> x1 != x2")
                    if x2 > x1: #перепишем эелмент из self.AN, на который указывает kB, в res_matrix.AN, поскольку он оказалеся непарным и "стоит левее"
                        res_matrix.AN.append(self.AN[kB])
                        kB += 1
                    elif x1 > x2: #перепишем эелмент из matrix.AN, на который указывает kC, в res_matrix.AN, поскольку он оказалеся непарным и "стоит левее"
                        res_matrix.AN.append(matrix.AN[kC])
                        kC += 1
                else:
                    print("=> x1 == x2")
                    elem_sum = self.AN[kB] + matrix.AN[kC]
                    if elem_sum: #если сумма элементов ненулевая
                        res_matrix.AN.append(elem_sum) #ЗДЕСЬ ВТОРАЯ ЗВЕЗДОЧКА!!!!
                    kB += 1
                    kC += 1
                print("x1: {}\nx2: {}\nkB: {}\nkC: {}\nres_matrix.AN: {}".format(x1,x2,kB,kC,res_matrix.AN))
            print("NEW ROW")
        
        print()
        
        res_matrix.print_info()
    
    def addition_try_3(self, matrix):
        res_matrix = SparseCRM()
        if (len(self.JR) != len(matrix.JR)) or (len(self.JC) != len(matrix.JC)): #проверяем размерность
            raise ValueError("(self.JR != matrix.JR) or (self.CR != matrix.CR)")
        res_matrix.JR = [-1 for i in self.JR] #инициализируем массив с индексами первых элементов строк значением -1
        res_matrix.JC = [-1 for i in self.JC] #инициализируем массив с индексами первых элементов столбцов значением -1
        kStrok = len(self.JR) #записываем количество строк
        kStolb = len(self.JC) #записываем количество столбцов
        N_1 = len(self.AN) #записываем количество ненулевых элементов матрицы-первого слагаемого (self)
        N_2 = len(matrix.AN) #записываем количество ненулевых элементов матрицы-второго слагаемого (matrix)
        N_res = 0 #счетчик числа элементов в res_matrix.AN и одновременно указатель на последний элемент
        kB = 0 #указатель на индекс массива AN матрицы-первого слагаемого (self)
        kC = 0 #указатель на индекс массива AN матрицы-второго слагаемого (matrix)

        for i in range(kStrok): #цикл по строкам от 0 до kStrok-1
            row_index1 = self.JR[i+1]
            row_index2 = matrix.JR[i+1]
            while True:
                print()
                print("="*8)
                print("row_index1: {}, row_index2: {}".format(row_index1, row_index2))
                x1 = self._find_x_coord(kB)
                x2 = matrix._find_x_coord(kC)
                print("x1: {}\nx2: {}\nkB: {}\nkC: {}\nres_matrix.AN: {}".format(x1,x2,kB,kC,res_matrix.AN))
                if x1 != x2: #ЗДЕСЬ ПЕРВАЯ ЗВЕЗДОЧКА!!!
                    print("=> x1 != x2", end="   ")
                    if x2 > x1: #перепишем эелмент из self.AN, на который указывает kB, в res_matrix.AN, поскольку он оказалеся непарным и "стоит левее"
                        print("x2 > x1 FROM B")
                        res_matrix.AN.append(self.AN[kB])
                        kB += 1
                    elif x1 > x2: #перепишем эелмент из matrix.AN, на который указывает kC, в res_matrix.AN, поскольку он оказалеся непарным и "стоит левее"
                        print("x1 > x2 FROM C")
                        res_matrix.AN.append(matrix.AN[kC])
                        kC += 1
                else:
                    print("=> x1 == x2")
                    elem_sum = self.AN[kB] + matrix.AN[kC]
                    if elem_sum: #если сумма элементов ненулевая
                        res_matrix.AN.append(elem_sum) #ЗДЕСЬ ВТОРАЯ ЗВЕЗДОЧКА!!!!
                    kB += 1
                    kC += 1
                print()
                print("x1: {}\nx2: {}\nkB: {}\nkC: {}\nres_matrix.AN: {}".format(x1,x2,kB,kC,res_matrix.AN))
                print("="*8)
                if kB == row_index1 and kC < row_index2:#(i < kStrok-1) and (kB == row_index1): # and kC == row_index2):
                    while True:
                        res_matrix.AN.append(matrix.AN[kC])
                        print("\tkB STOP, iterate kC. kC: {}, res_matrix.AN: {}".format(kC, res_matrix.AN))
                        kC += 1
                        if kC == row_index2:
                            break
                if kC == row_index2 and kB < row_index1:#(i < kStrok-1) and (kC == row_index2):
                    while True:
                        res_matrix.AN.append(self.AN[kB])
                        print("\tkC STOP, iterate kB. kB: {}, res_matrix.AN: {}".format(kB, res_matrix.AN))
                        kB += 1
                        if kB == row_index1:
                            break
                if kB == row_index1 and kC == row_index2:
                    print("BREAK rowborder")
                    break
                elif (kB == N_1 and kC == N_2):
                    print("BREAK matrixend")
                    break
            print("NEW ROW")
        
        print()
        
        res_matrix.print_info()
    
    def addition(self, matrix):
        res_matrix = SparseCRM()
        if (len(self.JR) != len(matrix.JR)) or (len(self.JC) != len(matrix.JC)): #проверяем размерность
            raise ValueError("(self.JR != matrix.JR) or (self.CR != matrix.CR)")
        res_matrix.JR = [-1 for i in self.JR] #инициализируем массив с индексами первых элементов строк значением -1
        res_matrix.JC = [-1 for i in self.JC] #инициализируем массив с индексами первых элементов столбцов значением -1
        kStrok = len(self.JR) #записываем количество строк
        kStolb = len(self.JC) #записываем количество столбцов
        N_1 = len(self.AN) #записываем количество ненулевых элементов матрицы-первого слагаемого (self)
        N_2 = len(matrix.AN) #записываем количество ненулевых элементов матрицы-второго слагаемого (matrix)
        N_res = 0 #счетчик числа элементов в res_matrix.AN и одновременно указатель на последний элемент
        kB = 0 #указатель на индекс массива AN матрицы-первого слагаемого (self)
        kC = 0 #указатель на индекс массива AN матрицы-второго слагаемого (matrix)
        print("N_1: {}, N_2: {}".format(N_1, N_2))

        for i in range(kStrok): #цикл по строкам от 0 до kStrok-1
            y1 = y1_temp = self._find_y_coord(kB)
            y2 = y2_temp = matrix._find_y_coord(kC)
            print("kStrok: {}, y1: {}, y2: {}".format(i, y1, y2))
            if y1 == y2: #если на одинаковых строках матриц есть элементы, то входим в ветку
                print("\tBRANCH 1 --- y1 == y2")
            elif y1 != y2: #если какая-либо из матриц не имеет элементов на строке, то входим в ветку
                print("\tBRANCH 2 --- y1 != y2")
                if y2 > y1:
                    print("\t\tBRANCH 2.1 --- y2 > y1")
                    while y2 > y1:#(y2 > y1 and kB < N_1):
                        print("\t\t\tBRANCH 2.1 --- I --- kB: {}, y1: {}, y2: {}, res_matrix: {}".format(kB, y1, y2, res_matrix.AN))
                        res_matrix.AN.append(self.AN[kB])
                        if kB+1 < N_1:
                            kB += 1
                            y1 = self._find_y_coord(kB)
                        else:
                            y1 = N_1
                            break
                        print("\t\t\tBRANCH 2.1 --- O --- kB: {}, y1: {}, y2: {}, res_matrix: {}".format(kB, y1, y2, res_matrix.AN))
                elif y1 > y2:
                    print("\t\tBRANCH 2.2 --- y1 > y2")
                    while y1 > y2:#(y1 > y2 and kC < N_2):
                        print("\t\t\tBRANCH 2.2 --- I ---  kC: {}, y1: {}, y2: {}, res_matrix: {}".format(kC, y1, y2, res_matrix.AN))
                        res_matrix.AN.append(matrix.AN[kC])
                        if kC+1 < N_2:
                            kC += 1
                            y2 = matrix._find_y_coord(kC)
                        else:
                            y2 = N_2
                            break
                        print("\t\t\tBRANCH 2.2 --- O ---  kC: {}, y1: {}, y2: {}, res_matrix: {}".format(kC, y1, y2, res_matrix.AN))
                print()

        print()
        
        res_matrix.print_info()

    def multiplication(self, matrix):
        pass

    '''
    if res_matrix.JR[i] == -1:
        res_matrix.JR[i] = N_res
        res_matrix.NR.append(N_res)
    '''