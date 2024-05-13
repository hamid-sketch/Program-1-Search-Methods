import csv
import heapq
import timeit
import math
import sys

# Read the coordinates.csv file and create a dictionary of cities with their coordinates
city_coordinates = {}
with open('coordinates.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        city_name, lat, lon = row
        city_coordinates[city_name] = (float(lat), float(lon))

# Read the Adjacencies.txt file and create a graph representation
adjacency_graph = {}
with open('Adjacencies.txt', 'r') as file:
    for line in file:
        city1, city2 = line.strip().split()
        if city1 not in adjacency_graph:
            adjacency_graph[city1] = []
        if city2 not in adjacency_graph:
            adjacency_graph[city2] = []
        adjacency_graph[city1].append(city2)
        adjacency_graph[city2].append(city1)

# Function to calculate the Haversine distance between two coordinates
def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    radius = 6371  # Earth's radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return radius * c

# Check for valid cities
def check_valid_city(city):
    if city in city_coordinates:
        return True
    else:
        print(f"{city} is not a valid city. Please enter a valid city name.")
        return False

# Calculate memory used by data structures
def calculate_memory():
    memory_used = 0
    memory_used += sys.getsizeof(city_coordinates)
    memory_used += sys.getsizeof(adjacency_graph)
    return memory_used

# Breadth-first search
def bfs(start, end):
    visited = set()
    queue = [(start, [])]

    while queue:
        current, path = queue.pop(0)
        if current == end:
            return path + [current]
        if current not in visited:
            visited.add(current)
            for neighbor in adjacency_graph.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [current]))
    return None

# Depth-first search
def dfs(start, end):
    visited = set()
    stack = [(start, [])]

    while stack:
        current, path = stack.pop()
        if current == end:
            return path + [current]
        if current not in visited:
            visited.add(current)
            for neighbor in adjacency_graph.get(current, []):
                if neighbor not in visited:
                    stack.append((neighbor, path + [current]))
    return None

# ID-DFS search (Iterative Deepening Depth-First Search)
def id_dfs(start, end):
    depth = 0
    while True:
        result = dfs_recursive(start, end, [], depth)
        if result is not None:
            return result
        depth += 1

def dfs_recursive(current, end, path, depth):
    if current == end:
        return path + [current]
    if depth == 0:
        return None
    for neighbor in adjacency_graph.get(current, []):
        if neighbor not in path:
            result = dfs_recursive(neighbor, end, path + [current], depth - 1)
            if result is not None:
                return result
    return None

# Best-first search (Greedy search)
def best_first_search(start, end):
    visited = set()
    heap = [(haversine(city_coordinates[start], city_coordinates[end]), start, [])]

    while heap:
        _, current, path = heapq.heappop(heap)
        if current == end:
            return path + [current]
        if current not in visited:
            visited.add(current)
            for neighbor in adjacency_graph.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(heap, (haversine(city_coordinates[neighbor], city_coordinates[end]), neighbor, path + [current]))
    return None

# A* search
def astar_search(start, end):
    visited = set()
    heap = [(0, haversine(city_coordinates[start], city_coordinates[end]), start, [])]

    while heap:
        _, _, current, path = heapq.heappop(heap)
        if current == end:
            return path + [current]
        if current not in visited:
            visited.add(current)
            for neighbor in adjacency_graph.get(current, []):
                if neighbor not in visited:
                    g = len(path) + 1  # Cost from start to current node
                    h = haversine(city_coordinates[neighbor], city_coordinates[end])  # Heuristic cost
                    f = g + h  # Total cost (f = g + h)
                    heapq.heappush(heap, (f, h, neighbor, path + [current]))
    return None

# Main program
while True:
    start_city = input("Enter the starting town: ")
    end_city = input("Enter the ending town: ")

    if not (check_valid_city(start_city) and check_valid_city(end_city)):
        continue

    while True:  # Loop for method selection
        print("Select a search method:")
        print("1. Breadth-first search")
        print("2. Depth-first search")
        print("3. ID-DFS search")
        print("4. Best-first search")
        print("5. A* search")

        method = int(input("Enter the method number (1-5): "))

        if method == 1:
            path = bfs(start_city, end_city)
            time_taken = timeit.timeit(lambda: bfs(start_city, end_city), number=1)
        elif method == 2:
            path = dfs(start_city, end_city)
            time_taken = timeit.timeit(lambda: dfs(start_city, end_city), number=1)
        elif method == 3:
            path = id_dfs(start_city, end_city)
            time_taken = timeit.timeit(lambda: id_dfs(start_city, end_city), number=1)
        elif method == 4:
            path = best_first_search(start_city, end_city)
            time_taken = timeit.timeit(lambda: best_first_search(start_city, end_city), number=1)
        elif method == 5:
            path = astar_search(start_city, end_city)
            time_taken = timeit.timeit(lambda: astar_search(start_city, end_city), number=1)
        else:
            print("Invalid method selection. Please enter a valid method number (1-5).")
            continue
        
        if path is not None:
            print(f"Route found: {' -> '.join(path)}")
            print(f"Time taken: {time_taken:.5f} seconds")
        else:
            print("No route found.")

        choice = input("Do you want to search again with a different method? (yes/no): ")
        if choice.lower() != 'yes':
            break  # Exit the method selection loop if the user does not want to search again

    choice = input("Do you want to perform another search? (yes/no): ")
    if choice.lower() != 'yes':
        break  # Exit the main loop if the user does not want to perform another search
