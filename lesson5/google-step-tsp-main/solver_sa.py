#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input, write_output
import solver_two_opt
import solver_random
import solver_greedy


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
# |random_seed|: 繰り返しごとのrandom.seedに与える値
def solve_sa(distances, tour, t, c, random_seed):
    tour.append(0)
    N = len(cities)

    sum_of_dist = calc_sum_of_dist(distances, tour)
    random.seed(random_seed)

    count_better = 0
    count_worse = 0
    count_no_change = 0

    i = 10
    while (i < 100): 
    # tが十分小さくなれば総距離が短くなる方向への変化のみを許す2opt法と実質的には変わらない。よってtが十分小さくなった時点で2opt法へ移行する
    # diffの平均値は0, 標準偏差は500程度になった。よって、t<10となれば下記の条件分岐におけるmath.e ** (-diff / t)が十分0に近くなり、tが十分小さくなったと考えられる
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
            count_better += 1
            print("count_better")
        elif random.random() < math.e ** (-diff / (0.5 ** (i / 100)) / 500): # 総距離が長くなっている場合でも、ある確率で新しい道順にアップデート
            part_of_list = tour[a+1:b+1]
            part_of_list.reverse()
            tour = tour[:a+1] + part_of_list + tour[b+1:]
            sum_of_dist += diff
            count_worse += 1
            print("count_worse")
        else:
            count_no_change += 1
            print("no_change")

        i += 1
    
    print("count_better:", count_better)
    print("count_worse:", count_worse)
    print("count_no_change:", count_no_change)
    return tour[:N]


if __name__ == '__main__':
    assert len(sys.argv) > 1

    cities = read_input(sys.argv[1])
    distances = calc_distances(cities)

    best_tour = solver_random.solve(cities)
    best_sum_of_dist = calc_sum_of_dist(distances, best_tour)

    for i in range(10):
        # tour = solver_random.solve(cities)
        tour = solver_greedy.solve(cities)
        tour = solve_sa(distances, tour, 10000, 0.9, i)
        tour = solver_two_opt.solve_two_opt(cities, tour)
        sum_of_dist = calc_sum_of_dist(distances, tour)

        if(best_sum_of_dist > sum_of_dist):
            best_tour = tour
            best_sum_of_dist = sum_of_dist

    print("best sum =", best_sum_of_dist)
    write_output(sys.argv[2], best_tour)
