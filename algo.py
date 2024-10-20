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

def main():
    if len(sys.argv) < 2:
        print("No file path")
        return
    elif len(sys.argv) > 2:
        print("Too many arguments, one file only needed")
        return

    input_file = sys.argv[1]
    coordinates, start, goal, adjacency_matrix = read_file(input_file)
    
    print("Parameters succesfully parsed")
    print(f"Coordinates: {coordinates}, \n Start: {start}, Goal: {goal}, \n Adjacency Matrix: {adjacency_matrix}")


if __name__ == "__main__":
    main()