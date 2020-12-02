import matr_create as m_c

def ants_path(city_num,
              days=20,
              alpha=0.5,
              beta=0.5,
              rho=0.5,
              rd_seed=1,
              verbose=False):
    if city_num > 26 or city_num < 2:
        raise ValueError("city_num > 26 or city_num < 2")

    city_names = {i:chr(i+65) for i in range(city_num)}

    paths_matrix = m_c.create_sym_matr(city_num, rd_seed=rd_seed)
    if verbose:
        m_c.sym_matrix_print(paths_matrix, city_num)
    pheromones_matrix = m_c.create_sym_matr(city_num, rd_seed=rd_seed, mode='pher')
    delta_pheromones_matrix = m_c.create_sym_matr(city_num, rd_seed=rd_seed, mode='delta_pher')

    best_route_len = 999999999
    current_route_len = 0

    best_route_cities = str()

    edge_num = (city_num**2 - city_num)/2
    Q = pheromone_quantity(city_num, paths_matrix, edge_num)
    
    route = []
    route_len = []
    cities_to_visit = list(range(city_num))
    ants_on_start = list(range(city_num))
    ants_at_the_end = []

    for day in range(1, days+1):
        if verbose:
            print("DAY {:3d} STARTS!".format(day))
        #дневной цикл по муравьям. Считаем, что номер муравья совпадает с номером города, из которого начинается его маршрут
        for ant in ants_on_start:
            first_city = ant
            cities_to_visit.pop(cities_to_visit.index(first_city)) #исключаем из непосещенных городов город, из которого начали движение
            route.append(first_city) #устанавливаем город, из которого начинаем движение, как первый город маршрута
            #цикл по непройденным городам
            while len(route) < city_num:
                if verbose:
                    print("ANT: {:d},".format(first_city), "route", route, "cities_to_visit", cities_to_visit)
                city_destination, edge_len = ant_choice(route[-1], cities_to_visit, paths_matrix, pheromones_matrix, alpha, beta)
                cities_to_visit.pop(cities_to_visit.index(city_destination)) #исключаем из непосещенных городов город, в который перемещается муравей
                route.append(city_destination) #добавляем город к маршруту за день
                route_len.append(edge_len) #сохраняем длину ребра маршрута между городами
                #вычисляем прирост феромона на пройденном ребре и сохраняем в матрицу дневного прироста
                delta_pheromones_matrix[route[-1]][city_destination] = delta_pheromones_matrix[city_destination][route[-1]] =  leave_some_pheromone(Q, sum(route_len))
            #проверяем длину маршрута
            current_route_len = sum(route_len)
            if verbose:
                print("current_route_len", current_route_len)
            if current_route_len < best_route_len:
                best_route_len = current_route_len
                best_route_cities = '->'.join([city_names[j] for j in route])
            ants_at_the_end.append(route[-1]) #сохраняем конечное положение муравья в конце дня
            current_route_len = 0 #обнуляем длину маршрута
            cities_to_visit = list(range(city_num)) #заново инициализируем массив с непосещенными городами
            route = [] #обнуляем список посещенных городов
            route_len = [] #обнуляем список с длиной пройденных ребер
        ants_on_start = ants_at_the_end #для нового дня передаем сведения о конечных точках маршрута муравьев в список, по которому проходит цикл по муравьям
        ants_at_the_end = []        
        #Ночной цикл по ребрам - испариение феромона, обнуление приращения феромонов за день
        for i in range(city_num):
            for j in range(city_num):
                if i<j:
                    pheromones_matrix[i][j] = pheromones_matrix[j][i] = pheromone_after_vaporization(
                        pheromones_matrix[i][j], rho, delta_pheromones_matrix[i][j], day
                    )
                    delta_pheromones_matrix[i][j] = delta_pheromones_matrix[j][i] = 0
        
    return (best_route_len, best_route_cities)


def pheromone_quantity(city_num, paths_matrix, edge_num):
    Q = 0
    for i in range(city_num):
        for j in range(city_num):
            if i<j:
                Q += paths_matrix[i][j]
    return Q/edge_num


def ant_choice(current_city,
               cities_to_visit,
               paths_matrix,
               pheromones_matrix,
               alpha, beta):
    city_destination = 0
    res_probability = m_c.random.random()
    temp_probability = 0

    denominator = sum(
        (((1/paths_matrix[current_city][city_to_visit])**alpha) * ((pheromones_matrix[current_city][city_to_visit])**beta))
        for city_to_visit in cities_to_visit
    )

    for city_possible_choice in cities_to_visit:
        numerator = (1/paths_matrix[current_city][city_possible_choice])**alpha * (pheromones_matrix[current_city][city_possible_choice])**beta
        temp_probability += numerator / denominator
        if temp_probability > res_probability:
            city_destination = city_possible_choice
            break
    
    return city_destination, paths_matrix[current_city][city_destination]


def leave_some_pheromone(pheromone_quantity, route_length):
    return pheromone_quantity/route_length


def pheromone_after_vaporization(pheromone_on_edge, rho, pheromone_increment, day):
    result = pheromone_on_edge*rho + pheromone_increment
    if result:
        return result
    else:
        #print("pheromone evaporated! day: ", day)
        return m_c.random.random()/1000000
