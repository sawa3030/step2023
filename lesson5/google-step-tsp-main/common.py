def read_input(filename):
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


def format_tour(tour):
    return 'index\n' + '\n'.join(map(str, tour))


def print_tour(tour):
    print(format_tour(tour))

def write_output(filename, tour):
    f = open(filename, 'w')
    f.write('index\n')
    for city in tour:
        f.writelines(str(city)+'\n')
    f.close()
    return