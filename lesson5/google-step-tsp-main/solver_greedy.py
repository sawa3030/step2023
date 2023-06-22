#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_output


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calc_distances(cities):
    N = len(cities)
    distances = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            distances[i][j] = distances[j][i] = distance(cities[i], cities[j])
    return distances

def solve(cities, dist, start_city = 0):
    N = len(cities)

    current_city = start_city
    unvisited_cities = set(range(0, N))
    print(start_city)
    unvisited_cities.remove(start_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    distances = calc_distances(cities)
    tour = solve(cities, distances)
    print_tour(tour)
    write_output(sys.argv[2], tour)
