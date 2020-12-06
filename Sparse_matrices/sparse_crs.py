import matr_create as m_c

class SparceCRS():
    def __init__(self):
        self.AN = [] #массив ненулевых элементов
        self.JA = [] #столбцовые координаты ненулевых элементов в исходной матрице
        self.JR = [] #модифицированный массив точек входа в строку по массиву AN
        self.cols = None #сохраняем число элементов в строке исходной матрицы
    
    def _set_pointers(self,  res):
        FLAG_IsRow = res
        if not FLAG_IsRow:
            FLAG_IsRow = True
            self.JR.append(len(self.AN))
        return FLAG_IsRow

    def print_info(self):
        print("AN:", self.AN)
        print("JA:", self.JA)
        print("JR:", self.JR)
        print("cols", self.cols)

    def pack(self, matrix):
        FLAG_IsRow = False
        rows = len(matrix)
        cols = len(matrix[0])

        for i in range(rows):
            for j in range(cols):
                if not FLAG_IsRow:
                    FLAG_IsRow = True
                    self.JR.append(len(self.AN))
                if matrix[i][j] != 0:
                    self.AN.append(matrix[i][j])
                    self.JA.append(j)
            FLAG_IsRow = False
        self.JR.append(len(self.AN))
        self.cols = cols

    def unpack(self, verbose=False):
        rows = len(self.JR)-1
        cols = self.cols
        unpack_matrix = [[0 for i in range(cols)] for j in range(rows)] #инициализируем распакованную матрицу элементами 0
        
        for i in range(len(self.JR)-1):
            for j in range(self.JR[i], self.JR[i+1]):
                if j >= len(self.AN):
                    continue
                if verbose:
                    print("i: {}, j: {}, self.JR[i]: {}, self.JR[i+1]: {}".format(i, j, self.JR[i], self.JR[i+1]))
                unpack_matrix[i][self.JA[j]] = self.AN[j]
        
        if verbose:
            m_c.sym_matrix_print(unpack_matrix, rows)

        return unpack_matrix

    def addition(self, matrix):
        rows = len(self.JR) - 1
        if (rows != len(matrix.JR)-1) or (self.cols != matrix.cols): #проверяем размерность
            raise ValueError("(self.JR != matrix.JR) or (self.CR != matrix.CR)")

        res_matrix = SparceCRS()
        res_matrix.cols = self.cols

        FLAG_IsRow = False

        for i in range(rows):
            FIRST_row = self.JR[i]
            SECOND_row = matrix.JR[i]
            if FIRST_row == self.JR[i+1] and SECOND_row == matrix.JR[i+1]: #совпадение индексов означает, что строки пустые
                res_matrix.JR.append(len(res_matrix.AN))
                continue
            while FIRST_row < self.JR[i+1] or SECOND_row < matrix.JR[i+1]: #если строки не пустые, то входим в цикл и рассматриваем строку (строки) до ее (их) окончание
                if SECOND_row < matrix.JR[i+1] and FIRST_row < self.JR[i+1]: #обе строки содержат ненулевые элементы
                    if self.JA[FIRST_row] == matrix.JA[SECOND_row]: #если х-координаты совпадают
                        FLAG_IsRow = res_matrix._set_pointers(FLAG_IsRow)
                        if self.AN[FIRST_row] + matrix.AN[SECOND_row] != 0:
                            res_matrix.AN.append(self.AN[FIRST_row] + matrix.AN[SECOND_row])
                            res_matrix.JA.append(matrix.JA[SECOND_row])
                        FIRST_row += 1
                        SECOND_row += 1
                    elif self.JA[FIRST_row] > matrix.JA[SECOND_row]: #если во второй матрице элемент в строке стоит "левее"
                        FLAG_IsRow = res_matrix._set_pointers(FLAG_IsRow)
                        res_matrix.AN.append(matrix.AN[SECOND_row])
                        res_matrix.JA.append(matrix.JA[SECOND_row])
                        SECOND_row += 1
                    elif self.JA[FIRST_row] < matrix.JA[SECOND_row]: #если в первой матрице элемент в строке стоит "левее"
                        FLAG_IsRow = res_matrix._set_pointers(FLAG_IsRow)
                        res_matrix.AN.append(self.AN[FIRST_row])
                        res_matrix.JA.append(self.JA[FIRST_row])
                        FIRST_row += 1
                elif SECOND_row < matrix.JR[i+1]: #если ненулевая - только строка первой матрицы
                    FLAG_IsRow = res_matrix._set_pointers(FLAG_IsRow)
                    res_matrix.AN.append(matrix.AN[SECOND_row])
                    res_matrix.JA.append(matrix.JA[SECOND_row])
                    SECOND_row += 1
                elif FIRST_row < self.JR[i+1]: #если ненулевая - только строка второй матрицы
                    FLAG_IsRow = res_matrix._set_pointers(FLAG_IsRow)
                    res_matrix.AN.append(self.AN[FIRST_row])
                    res_matrix.JA.append(self.JA[FIRST_row])
                    FIRST_row += 1
            FLAG_IsRow = False

        res_matrix.JR.append(len(res_matrix.AN))

        return res_matrix


    def multiplication(self, matrix):
        if self.cols != len(matrix.JR)-1:
            raise ValueError("self.cols != len(matrix.JR)-1")

        res_matrix = SparceCRS()
        res_matrix.cols = matrix.cols

        res_matrix.JR.append(0)

        for i in range(len(self.JR)-1):
            index = self.JR[i]
            vals = [0 for i in range(matrix.cols)]

            while index < self.JR[i+1]:
                for j in range(len(matrix.JR)-1):
                    if j == self.JA[index] and index < self.JR[i+1]:
                        for k in range(matrix.JR[j], matrix.JR[j+1]):
                            vals[matrix.JA[k]] += self.AN[index] * matrix.AN[k]
                        index += 1
                    if index >= self.JR[i+1]:
                        break
            
            for m in range(len(vals)):
                if vals[m] != 0:
                    res_matrix.AN.append(vals[m])
                    res_matrix.JA.append(m)
            
            res_matrix.JR.append(len(res_matrix.AN))
        
        return res_matrix