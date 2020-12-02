import brute_force as bf
import ants

def ants_runner(city_num_start, city_num_stop,
                alpha_start, alpha_stop,
                rho_start, rho_stop,
                delta=25):
    results = []
    res_header = "alpha|rho|days|matrix_size|ants_best|brute_force|delta"
    results.append(res_header)
    for city_num in range(city_num_start, city_num_stop):
        print("NEW ITERATION. Matrix size:", city_num)
        standard, _ = bf.brute_force(city_num)
        for days in [20, 50, 100, 150, 200]:
            print("\t {} DAYS iteration".format(days))
            for alpha in range(alpha_start*100, alpha_stop*100+25, delta):
                alpha = alpha/100
                for rho in range(rho_start*100, rho_stop*100+25, delta):
                    rho = rho/100
                    best_route_len, _ = ants.ants_path(
                        city_num, days=days, alpha=alpha, beta=(1-alpha), rho=rho
                    )
                    res_str = "{:.2f}|{:.2f}|{:d}|{:d}|{:d}|{:d}|{:d}".format(alpha, rho, days, city_num, best_route_len, standard, abs(standard-best_route_len))
                    results.append(res_str.replace('.', ','))
    return results