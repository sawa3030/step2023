#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_output


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

def two_opt(cities, tour):
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
    print(sum_distance)
    """ for i in range(N-1):
        for j in range(i+1, N-1): 
            #print("i=", i, "j=", j)
            # print(dist[tour[i]][tour[j]])
            # print(dist[tour[j+1]][tour[i+1]])
            # print(dist[tour[i]][tour[i+1]])
            # print(dist[tour[j]][tour[j+1]])
            #print(tour)
            if(dist[tour[i]][tour[j]] + dist[tour[j+1]][tour[i+1]] < dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]]):
                part_of_list = tour[i+1:j+1]
                part_of_list.reverse()
                tour = tour[0:i+1] + part_of_list + tour[j+1:N]
                new_sum_distance = new_sum_distance - (dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]]) + (dist[tour[i]][tour[j]] + dist[tour[j+1]][tour[i+1]])
    print(new_sum_distance) """

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
                    print(sum_distance)

    print("final=",sum_distance)
    return tour[:N+1]


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    tour = two_opt(read_input(sys.argv[1]), tour)
    print_tour(tour)
    write_output(sys.argv[2], tour)
