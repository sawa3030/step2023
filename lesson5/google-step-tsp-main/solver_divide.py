#!/usr/bin/env python3

import sys
import math
import random
import numpy

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

def solver_greedy_with_id(cities, dist, start_city):
    N = len(cities)

    current_city = start_city
    unvisited_cities = set(city for city in cities)
    unvisited_cities.remove(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


def divide(cities):
    distances = calc_distances(cities)

    average = numpy.mean(cities, axis=0)
    city_groups = [[] for i in range (4)]

    for i in range(len(cities)):
        if(cities[i][0] <= average[0] and cities[i][1] <= average[1]):
            city_groups[0].append(i)
        elif(cities[i][0] <= average[0] and cities[i][1] > average[1]):
            city_groups[1].append(i)
        elif(cities[i][0] > average[0] and cities[i][1] > average[1]):
            city_groups[2].append(i)
        else:
            city_groups[3].append(i)

    tour = []

    for i in range (4):
        start_city = random.choice(city_groups[i])
        tour += solver_greedy_with_id(city_groups[i], distances, start_city)
    
    zero_id = tour.index(0)
    tour = tour[zero_id:] + tour[:zero_id]

    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1

    cities = read_input(sys.argv[1])
    distances = calc_distances(cities)

    best_tour = []
    best_sum_of_dist = 1000000000

    for i in range(10):
        tour = divide(cities)
        tour = solver_two_opt.solve_two_opt(cities, tour)
        sum_of_dist = calc_sum_of_dist(distances, tour)

        if(best_sum_of_dist > sum_of_dist):
            best_tour = tour
            best_sum_of_dist = sum_of_dist

    print("best sum =", best_sum_of_dist)
    write_output(sys.argv[2], best_tour)
