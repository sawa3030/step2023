#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input, write_output
import solver_two_opt
import solver_random

# 2点間の距離の計算
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# 全ての2点間の距離を計算する
# 返り値は全ての2点間の距離を持つ二次配列
def calc_distances(cities):
    N = len(cities)
    distances = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            distances[i][j] = distances[j][i] = distance(cities[i], cities[j])
    return distances

# |tour|: 道順
# 道順に対する総距離
def calc_sum_of_dist(distances, tour):
    prev_city = 0
    sum_of_distances = 0
    for id in range (1, len(tour)):
        sum_of_distances += distances[prev_city][tour[id]]
        prev_city = tour[id]
    sum_of_distances += distances[prev_city][0]
    return sum_of_distances

# 焼きなまし法による実装
# |t|: 初期温度
# |c|: 冷却率 
def solve_sa(distances, tour, t, c):
    tour.append(0)
    N = len(cities)

    sum_of_dist = calc_sum_of_dist(distances, tour)

    random.seed(1)

    i = 0
    while (t > 10): # 総距離の変化は100程度のオーダーが多い。t>10となれば総距離が短くなる方向への変化のみを許す2opt法と実質的には変わらず、2opt法をとればよいと考えた
        # [0, tour[1] , ... , tour[a], tour[a+1], ... , tour[b], tour[b+1], ..., tour[N-1], 0] となっているtour（道順）の配列を
        # [0, tour[1] , ... , tour[a], tour[b], ... , tour[b+1], tour[a+1], ..., tour[N-1], 0] と変えたとした時を考える
        a = random.randint(0, N-3)
        b = random.randint(a+2, N-1)

        diff = (distances[tour[a]][tour[b]] + distances[tour[b+1]][tour[a+1]]) - (distances[tour[a]][tour[a+1]] + distances[tour[b]][tour[b+1]])

        if(diff <= 0): # 総距離が短くなっているならば、新しい道順にアップデート
            part_of_list = tour[a+1:b+1]
            part_of_list.reverse()
            tour = tour[:a+1] + part_of_list + tour[b+1:]
            sum_of_dist += diff
        elif random.random() < math.e ** (-diff / t): # 総距離が長くなっている場合でも、ある確率で新しい道順にアップデート
            part_of_list = tour[a+1:b+1]
            part_of_list.reverse()
            tour = tour[:a+1] + part_of_list + tour[b+1:]
            sum_of_dist += diff
            
        t = c * t
        i += 1
    
    return tour[:N]

if __name__ == '__main__':
    assert len(sys.argv) > 1

    cities = read_input(sys.argv[1])
    distances = calc_distances(cities)
    tour = solver_random.solve(cities)
    tour = solve_sa(distances, tour, 10000, 0.9)
    tour = solver_two_opt.solve_two_opt(cities, tour)
    write_output(sys.argv[2], tour)
