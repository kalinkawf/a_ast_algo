import sys

def read_file(file_path):
    """ Function to get parameters from input file """

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Get Coordinates by structure of the input file
    coordinates = []
    coords_line = lines[0].strip().split(') (')
    coords_line[0] = coords_line[0].replace('(', '').replace(')', '')
    coords_line[-1] = coords_line[-1].replace(')', '')
    for coord in coords_line:
        x, y = map(float, coord.replace(',', '.').strip().split())
        coordinates.append((x, y))
    
    # Get start and goal
    start, goal = map(int, lines[1].strip().split())
    if not start:
        print("Check if there is start in second line of input file")
    elif not goal:
        print("Check if there is goal in second line of input file")
    else:
        pass
    
    # Get adjacency matrix
    adjacency_matrix = []
    for line in lines[2:]:
        row = list(map(float, line.strip().split()))
        adjacency_matrix.append(row)

    return coordinates, start, goal, adjacency_matrix

def euclidean_distance(p, q):
    """ https://en.wikipedia.org/wiki/Euclidean_distance """
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5

def a_star_algo(coordinates, start, goal, adjacency_matrix):
    """ A-star https://pl.wikipedia.org/wiki/Algorytm_A* """
    # Lista open_set do przechowywania wierzchołków do przetworzenia
    open_set = [(start, 0)]  # Zainicjalizowana początkowym wierzchołkiem (wierzchołek, f_score)

    # Koszt dojścia do wierzchołków, inicjalizowany inf
    g_score = {i: float('inf') for i in range(len(coordinates))}
    g_score[start] = 0

    # Koszt estymowany (g_score + heurestyka)
    f_score = {i: float('inf') for i in range(len(coordinates))}
    f_score[start] = euclidean_distance(coordinates[start], coordinates[goal])

    # Ścieżka - mapuje wierzchołki poprzednie na aktualne
    came_from = {}

    while open_set:
        # Znajdź wierzchołek z najniższym f_score
        current = min(open_set, key=lambda x: x[1])[0]
        open_set = [item for item in open_set if item[0] != current]

        # Jeśli dotarliśmy do celu, zrekonstruuj ścieżkę
        if current == goal:
            path = []
            while current in came_from:
                path.append(current + 1)
                current = came_from[current]
            path.append(start + 1)

            cost_to_goal = g_score[goal] # koszt
            return cost_to_goal, " ".join(map(str, path[::-1]))  # Zwracamy ścieżkę od startu do celu

        # Przeglądanie sąsiadów
        for neighbor, weight in enumerate(adjacency_matrix[current]):
            if weight == 0:
                continue  # Brak krawędzi

            tentative_g_score = g_score[current] + weight

            # Jeśli znaleźliśmy lepszą ścieżkę do sąsiada
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(coordinates[neighbor], coordinates[goal]) # heurestyka
                
                # Dodaj do open_set, jeśli nie ma
                if neighbor not in [item[0] for item in open_set]:
                    open_set.append((neighbor, f_score[neighbor]))

    return "-", "Brak"  # Brak ścieżki między startem a metą

def main():
    if len(sys.argv) < 2:
        print("No file path")
        return
    elif len(sys.argv) > 2:
        print("Too many arguments, one file only needed")
        return

    file_path = sys.argv[1]
    coordinates, start, goal, adjacency_matrix = read_file(file_path)
    start = start - 1 # indeksowanie taablic od 0
    goal = goal - 1

    # print(f"Coordinates: {coordinates}, \n Start: {start}, Goal: {goal}, \n Adjacency Matrix: {adjacency_matrix}")

    cost, result = a_star_algo(coordinates, start, goal, adjacency_matrix)
    print(f"{file_path[6:]}   Koszt: {cost}   Trasa: {result}") # printuje się jak w odpowiedziach

if __name__ == "__main__":
    main()