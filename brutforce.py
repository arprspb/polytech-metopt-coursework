from functools import lru_cache
import itertools
import json
from concurrent.futures import ProcessPoolExecutor, as_completed

with open('points_500.json', 'r') as file:
    data = json.load(file)

for key in data:
    data[key] = [tuple(point) for point in data[key]]

start_point = (0, 0)

elements = data.keys()

best_route = None
min_square_distance = float('inf')

@lru_cache(maxsize=None)
def square_distance(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2

def calculate_route_distance(perm):
    local_best_route = None
    local_min_square_distance = float('inf')
    current_point = start_point

    for entries in itertools.product(*[data[contour_name] for contour_name in perm]):
        current_square_distance = square_distance(current_point, entries[0])

        for i in range(1, len(entries)):
            current_square_distance += square_distance(entries[i - 1], entries[i])

        if current_square_distance < local_min_square_distance:
            local_min_square_distance = current_square_distance
            local_best_route = entries

    return local_min_square_distance, local_best_route

def main():
    global best_route, min_square_distance
    total_permutations = list(itertools.permutations(elements))
    total_count = len(total_permutations)  # Подсчет всех перестановок

    count = 0

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(calculate_route_distance, perm): perm for perm in total_permutations}
        
        for future in as_completed(futures):
            distance, route = future.result()
            count += 1
            # Выводим прогресс
            print(f'Processed {count}/{total_count} permutations')
            
            if distance < min_square_distance:
                min_square_distance = distance
                best_route = route

    print(best_route)
    print(min_square_distance)

if __name__ == "__main__":
    main()
