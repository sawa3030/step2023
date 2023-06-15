#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_output
import solver_greedy


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve_two_opt(cities, tour):
    N = len(cities)
    
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    sum_distance = 0
    prev_city = 0
    for id in range (1, len(tour)):
        sum_distance += dist[prev_city][tour[id]]
        prev_city = tour[id]
    sum_distance += dist[prev_city][0]

    is_updated = True

    tour.append(0)
    while(is_updated):
        is_updated = False
        for i in range(N):
            for j in range(i+1, N): 
                if((dist[tour[i]][tour[j]] + dist[tour[j+1]][tour[i+1]]) < (dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]])):
                    sum_distance = sum_distance - (dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]]) + (dist[tour[i]][tour[j]] + dist[tour[j+1]][tour[i+1]])
                    part_of_list = tour[i+1:j+1]
                    part_of_list.reverse()
                    tour = tour[:i+1] + part_of_list + tour[j+1:]
                    is_updated = True
                    # print(sum_distance)

    print("final sum =",sum_distance)
    return tour[:N]

def solve(cities):
    tour = solver_greedy.solve_greedy(cities)
    tour = solve_two_opt(cities, tour)
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)
