import svgpathtools
import numpy as np

# Загрузим SVG файл
paths, attributes = svgpathtools.svg2paths('images/black.svg')

# Функция для дискретизации пути с заданным шагом max_distance
def discretize_path(path, max_distance):
    total_length = path.length()
    print(f"{total_length=}")
    num_points = int(total_length // max_distance) + 1  # Количество точек, включая конец пути
    print(f"{num_points=}")
    # Генерируем равномерно распределенные точки с шагом max_distance
    points = [path.point(path.ilength(i * max_distance)) for i in range(num_points)]

    return points

# Пример использования: разбиваем каждый path на точки с шагом h
h = 1000  # шаг между точками
all_discretized_points = []

for path in paths:
    points = discretize_path(path, max_distance=h)
    all_discretized_points.append(points)

# Выводим координаты точек для каждого пути
with open(f'points_{h}.json', 'w') as res:
  res.write("{\n")
  for i, points in enumerate(all_discretized_points):
      res.write((f"\"Path {i}\": ["))
      for j, point in enumerate(points):
        if j == len(points) - 1:  # Если это последняя точка
            res.write((f"[{int(point.real/10)}, {int(point.imag/10)}]"))
        else:
            res.write((f"[{int(point.real/10)}, {int(point.imag/10)}],"))
      if i == len(all_discretized_points) -1:
          res.write("]\n")
      else:
          res.write("],\n")
  res.write("}\n")

