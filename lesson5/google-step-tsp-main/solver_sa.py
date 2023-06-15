#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input, write_output
from solver_greedy import two_opt
import solver_random

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calc_distances(cities):
    N = len(cities)
    distances = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            distances[i][j] = distances[j][i] = distance(cities[i], cities[j])
    return distances

def calc_sum_of_dist(distances, tour):
    prev_city = 0
    sum_of_distances = 0
    for id in range (1, len(tour)):
        sum_of_distances += distances[prev_city][tour[id]]
        prev_city = tour[id]
    sum_of_distances += distances[prev_city][0]
    return sum_of_distances

# |t|: 初期温度
# |c|: 冷却率 
def solve_sa(distances, tour, t, c):
    tour.append(0)
    N = len(cities)
    tour_next = tour
    sum_of_dist = calc_sum_of_dist(distances, tour)
    sum_of_dist_next = sum_of_dist
    random.seed(1)

    i = 0
    while (t > 10):
        # print(i)
        
        a = random.randint(0, N-3)
        b = random.randint(a+2, N-1)

        part_of_list = tour[a+1:b+1]
        part_of_list.reverse()
        tour_next = tour[:a+1] + part_of_list + tour[b+1:]
        sum_of_dist_next = sum_of_dist - (distances[tour[a]][tour[a+1]] + distances[tour[b]][tour[b+1]]) + (distances[tour[a]][tour[b]] + distances[tour[b+1]][tour[a+1]])
        d = sum_of_dist_next - sum_of_dist

        # print(d, t)
        # print(math.e ** (-d / t))

        if(d <= 0):
            tour = tour_next
            sum_of_dist = sum_of_dist_next
            # print("better solution was found", sum_of_dist)
        elif random.random() < math.e ** (-d / t):
            tour = tour_next
            sum_of_dist = sum_of_dist_next
            # print("moved to worse solution", sum_of_dist)
        # else:
            # print("no change", sum_of_dist)
        # print(sum_of_dist)
        t = c * t
        i += 1
    
    return tour[:N]

if __name__ == '__main__':
    assert len(sys.argv) > 1

    cities = read_input(sys.argv[1])
    distances = calc_distances(cities)
    tour = solver_random.solve(cities)
    tour = solve_sa(distances, tour, 10000, 0.9)
    tour = two_opt(cities, tour)
    # print_tour(tour)
    write_output(sys.argv[2], tour)
