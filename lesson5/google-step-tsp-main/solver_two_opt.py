#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_output
import solver_greedy


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calc_distances(cities):
    N = len(cities)
    distances = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            distances[i][j] = distances[j][i] = distance(cities[i], cities[j])
    return distances

# |tour|: 道順
# 道順に対する総距離
def calc_sum_of_dist(distances, tour, start_city = 0):
    prev_city = 0
    sum_of_distances = 0
    for id in range (1, len(tour)):
        sum_of_distances += distances[prev_city][tour[id]]
        prev_city = tour[id]
    sum_of_distances += distances[prev_city][start_city]
    return sum_of_distances

def solve_two_opt(cities, dist, tour, start_city):
    N = len(cities)

    sum_distance = calc_sum_of_dist(dist, tour, start_city)

    is_updated = True
    prev_i = -1

    tour.append(0)
    while(is_updated):
        is_updated = False
        # for i in range(prev_i+1, N-2):
        for i in range(prev_i+1, N-2):
            for j in range(i+2, N): 
                # [0, tour[1] , ... , tour[i], tour[i+1], ... , tour[j], tour[j+1], ..., tour[N-1], 0] となっているtour（道順）の配列を
                # [0, tour[1] , ... , tour[i], tour[j], ... , tour[i+1], tour[j+1], ..., tour[N-1], 0] と変えて、総距離の変化diffに注目する
                # 総距離が減るならば新しいtourにアップデートする
                diff = (dist[tour[i]][tour[j]] + dist[tour[j+1]][tour[i+1]]) - (dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]])
                if(diff < 0):
                    sum_distance += diff
                    part_of_list = tour[i+1:j+1]
                    part_of_list.reverse()
                    tour = tour[:i+1] + part_of_list + tour[j+1:]
                    is_updated = True
            if(is_updated == False):
                prev_i = i

    print("final sum =",sum_distance)
    return tour[:N]

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    distances = calc_distances(cities)
    tour = solver_greedy.solve(cities, distances)
    tour = solve_two_opt(cities, distances, tour)
    print_tour(tour)
    write_output(sys.argv[2], tour)
