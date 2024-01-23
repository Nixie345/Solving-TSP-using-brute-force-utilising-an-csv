import csv
import math
import time



# Function to calculate the Haversine distance between two coordinates
def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Function to create a distance matrix based on Haversine distances between coordinates
def create_distance_matrix(coordinates):
    num_cities = len(coordinates)
    matrix = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = haversine_distance(coordinates[i], coordinates[j])
            matrix[i][j] = matrix[j][i] = distance

    return matrix

# Function to calculate the total distance of a given path in the TSP
def total_distance(path, distance_matrix):
    total_dist = 0
    for i in range(len(path) - 1):
        total_dist += distance_matrix[path[i]][path[i + 1]]
    total_dist += distance_matrix[path[-1]][path[0]]  # Return to the starting city
    return total_dist

# Recursive function to solve the Traveling Salesman Problem using backtracking
def traveling_salesman_backtrack(num_cities, coordinates):
    best_path = None
    min_distance = float('inf')
    current_path = [0]  # Start with the first city (index 0)

    distance_matrix = create_distance_matrix(coordinates)  # Moved inside the function

    def backtrack(current_path, start_time):
        nonlocal best_path, min_distance

        # Base case: If all cities are visited, calculate the distance and update the best path
        if len(current_path) == num_cities:
            distance = total_distance(current_path, distance_matrix)
            if distance < min_distance:
                min_distance = distance
                best_path = current_path.copy()
            return

        # Iterate through all cities and recursively explore possible paths
        for city in range(num_cities):
            if city not in current_path:
                current_path.append(city)

                # Check if 5 seconds have passed and print elapsed time
                if time.time() - start_time >= 5:
                    elapsed_time = time.time() - start_time
                    hours, remainder = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    print("\rElapsed Time: {:.0f} hours, {:.0f} minutes, and {:.2f} seconds".format(hours, minutes, seconds), end="")
                    start_time = time.time()

                backtrack(current_path, start_time)
                current_path.pop()

    # Start the backtracking process
    print("Elapsed Time: 0 hours, 0 minutes, and 0.00 seconds", end="")
    start_time = time.time()
    backtrack(current_path, start_time)

    return best_path, min_distance

# Function to read coordinates from a CSV file
def read_coordinates_from_csv(file_path):
    coordinates = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')  # Use commas as delimiters
        for row in reader:
            lat, lon = map(float, row)
            coordinates.append((lat, lon))
    return coordinates

if __name__ == "__main__":
    # User input to get the path to the CSV file containing city coordinates
    while True:
        try:
            file_path = input("Enter the path to the CSV file: ")
            cities_coordinates = read_coordinates_from_csv(file_path)
            num_cities = len(cities_coordinates)
            if num_cities > 0:
                break
            else:
                print("Invalid input. The number of cities must be greater than 0.")
        except FileNotFoundError:
            print("File not found. Check the path and try again.")

    # Solve the TSP using backtracking and record the runtime
    best_path, min_distance = traveling_salesman_backtrack(num_cities, cities_coordinates)
    
    end = time.time()
    elapsed_time = end-start
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Display the results
    print("\n""\033[34m", "\033[4m", "Best Path:", "\033[37m", "\033[24m", "      ", best_path)
    print("\n""\033[34m", "\033[4m", "Minimum Distance:", "\033[37m", "\033[24m", min_distance, "km")
    print("\n""\033[34m", "\033[4m", "Total Elapsed Time:", "\033[37m", "\033[24m", "{:.0f} uur, {:.0f} minuten, and {:.2f} seconden".format(hours, minutes, seconds))