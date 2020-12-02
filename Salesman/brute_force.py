import matr_create as m_c

def brute_force(city_num=5, rd_seed=1, verbose=False):
    if city_num > 26 or city_num < 2:
        raise ValueError("city_num > 26 or city_num < 2")

    city_names = {i:chr(i+65) for i in range(city_num)}

    paths_matrix = m_c.create_sym_matr(city_num, rd_seed=rd_seed)
    if verbose:
        m_c.sym_matrix_print(paths_matrix, city_num)
    
    best_route_len = 999999999
    current_route_len = 0
    
    best_route_cities = str()

    cities_to_visit = list(range(city_num))

    for route in permute(cities_to_visit):
        for i in range(1, city_num):
            city_FROM = route[i-1]
            city_TO = route[i]
            current_route_len += paths_matrix[city_FROM][city_TO]
        if current_route_len < best_route_len:
            best_route_len = current_route_len
            best_route_cities = '->'.join([city_names[j] for j in route])
        current_route_len = 0
    
    return (best_route_len, best_route_cities)

def permute(lst):
    if not lst:
        yield lst
    else:
        for i in range(len(lst)):
            rest = lst[:i] + lst[i+1:]
            for x in permute(rest):
                yield lst[i:i+1] + x


if __name__ == '__main__':
    print("="*20)
    print("Module demonstration\n")
    print("Input matrix size: ")
    size = int(input())
    brute_force(city_num=size)
    print("="*20)