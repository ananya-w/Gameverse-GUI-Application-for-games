import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox


# Nearest Neighbor Algorithm code here...


def distance(city1, city2):
    """
    Calculate the Euclidean distance between two cities.
    """
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def nearest_neighbor(start, unvisited_cities):
    """
    Find the nearest unvisited city to the given city.
    """
    min_distance = float('inf')
    nearest_city = None
    for city in unvisited_cities:
        dist = distance(start, city)
        if dist < min_distance:
            min_distance = dist
            nearest_city = city
    return nearest_city, min_distance

def tsp_nearest_neighbor(cities):
 
    current_city = cities[0]
    unvisited_cities = set(cities[1:])
    tour = [current_city]
    total_distance = 0
    plt.figure()
    
    # Plotting the initial cities
    for i, city in enumerate(cities):
        plt.plot(city[0], city[1], marker='o', markersize=10, color='Purple')
        plt.text(city[0], city[1], f'{i}')
    
    while unvisited_cities:
        next_city, distance_to_next = nearest_neighbor(current_city, unvisited_cities)
        tour.append(next_city)
        unvisited_cities.remove(next_city)
        total_distance += distance_to_next
        plt.plot([current_city[0], next_city[0]], [current_city[1], next_city[1]], marker='o', linestyle='-', color='#ffdaa2', linewidth=4)
        current_city = next_city
        plt.text(current_city[0], current_city[1], f'{len(tour)}')
        plt.pause(0.5)  # Pause for visualization
    tour.append(tour[0]) # Return to the starting city to complete the tour
    total_distance += distance(tour[-1], tour[0])
    plt.plot([current_city[0], tour[0][0]], [current_city[1], tour[0][1]], marker='o', linestyle='-', color='#ffdaa2', linewidth=4)  # Connect back to starting city
    plt.title('Optimal Tour Progress')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

    return tour, total_distance
def get_cities_from_input(num_cities):
    """
    Prompt the user to input coordinates for all cities.
    """
    cities = []
    for i in range(num_cities):
        coordinates = simpledialog.askstring("City Coordinates", f"Enter coordinates for city {i+1} (x y):")
        if coordinates is None:
            return None  # If the user cancels, return None
        try:
            x, y = map(int, coordinates.split())
            cities.append((x, y))
        except ValueError:
            print("Invalid input format. Please enter coordinates as 'x y'.")
            return None
    return cities

if __name__ == "__main__":
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Get the number of cities from the user using a dialogue box
    num_cities = simpledialog.askinteger("Number of Cities", "Enter the number of cities:")

    # Get the coordinates of all cities from the user using a single input
    cities = get_cities_from_input(num_cities)
    if cities is None:
        print("City input canceled.")
    else:
        # Solve TSP using nearest neighbor algorithm
        tour, total_distance = tsp_nearest_neighbor(cities)

        # Display tour and total distance in a dialogue box
        tour_str = '\n'.join([f'City {i}: {city}' for i, city in enumerate(tour)])
        messagebox.showinfo("Optimal Tour", f"Optimal Tour:\n{tour_str}\nTotal Distance: {total_distance}")
