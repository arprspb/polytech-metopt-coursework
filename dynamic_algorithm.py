import json
import math
import numpy as np
from functools import lru_cache

import matplotlib.pyplot as plt

# Чтение данных из JSON
filename = 'points_200'
with open(f'{filename}.json', 'r') as f:
    clusters = json.load(f)


for cluster, points in clusters.items():
    clusters[cluster] = [tuple(point) for point in points]


start_point = (900, 500)
clusters["V1"] = [start_point]  

all_points = {1: start_point}  
point_counter = 2

for cluster, points in clusters.items():
    for point in points:
        all_points[point_counter] = tuple(point)
        point_counter += 1




def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

distances = {}


for i in all_points:
    distances[i] = {}
    for j in all_points:
        if i != j: 
            distances[i][j] = euclidean_distance(all_points[i], all_points[j])

from functools import lru_cache
        

@lru_cache
def get_point_index(point):
    return [i for i, p in all_points.items() if p == point][0]


@lru_cache(None)
def g(current_point, remaining_clusters):
    if not remaining_clusters:  # Если все кластеры посещены, возвращаем 0 и пустой маршрут
        return 0, []

    min_dist = float('inf')
    best_route = []

    for cluster in remaining_clusters:
        for point in clusters[cluster]:
            point_index = get_point_index(point)

            dist, route = g(point_index, tuple(c for c in remaining_clusters if c != cluster))  # Преобразуем оставшиеся кластеры в кортеж
            total_dist = distances[current_point][point_index] + dist
            
            if total_dist < min_dist:
                min_dist = total_dist
                best_route = [(point, cluster)] + route  # Сохраняем текущую точку и маршрут дальше

    return min_dist, best_route


remaining_clusters = tuple(set(clusters.keys()) - {"V1"})  # Преобразуем в кортеж

# Пример вызова функции
optimal_distance, optimal_route = g(1, remaining_clusters)  # Начинаем с точки 1
optimal_route = [(start_point, 'V1')] + optimal_route

print("Оптимальная длина пути:", optimal_distance)
print("Оптимальный маршрут:", optimal_route)



# Генерация цветов для каждого кластера
colors = plt.cm.get_cmap('hsv', len(clusters))  # Получаем цветовую карту

# Создание графика
plt.figure(figsize=(10, 8))

route_points = np.array([point[0] for point in optimal_route])  # Извлекаем только координаты
plt.plot(route_points[:, 0], route_points[:, 1], color='red', linestyle='--', linewidth=1, markersize=5, label='Optimal Route')

for i, (cluster, points) in enumerate(clusters.items()):
    if cluster != 'V1':
        points_array = np.array(points)
        plt.scatter(points_array[:, 0], points_array[:, 1], color=colors(i), label=f'Cluster {cluster}', alpha=1)
    else:
        points_array = np.array(points)
        plt.scatter(points_array[:, 0], points_array[:, 1], marker='x', s=200, color=colors(i), label=f'Start point', alpha=1)

# Настройки графика
plt.title(f'{filename} L = {optimal_distance}')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)
plt.show()