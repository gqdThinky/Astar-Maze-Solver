import pygame, heapq, os

# Load the maze image
maze_image = pygame.image.load('maze.png') # Make sure your file is named like that.
width, height = maze_image.get_size()

# Initialize the pygame screen
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))  # Set white background
pygame.display.set_caption('A* Maze Solver')  # Set window caption

# Convert the image into a list of tuples (x, y, color)
maze_data = list(pygame.image.tostring(maze_image, 'RGBA'))

# Define the wall color
WALL_COLOR = (0, 0, 0, 255)

# Define possible directions (up, down, left, right)
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Deletes the file "maze_path.png" if it already exists
if os.path.exists("maze_path.png"):
    os.remove("maze_path.png")
    print("The file 'maze_path.png' has correctly been deleted.")

# Function to check if a position is valid in the maze
def is_valid(x, y):
    return 0 <= x < width and 0 <= y < height

# Function to detect the location of walls in the maze
def detect_walls():
    walls = set()
    for y in range(height):
        for x in range(width):
            pixel_index = (y * width + x) * 4
            color = tuple(maze_data[pixel_index: pixel_index + 4])
            if color == WALL_COLOR:
                walls.add((x, y))
    return walls

# Implement the A* algorithm
def astar(start, end, walls):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in directions:
            new_x, new_y = current[0] + dx, current[1] + dy
            neighbor = (new_x, new_y)
            if is_valid(new_x, new_y) and neighbor not in walls:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (tentative_g_score + heuristic(neighbor, end), neighbor))

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Find the entrance and exit of the maze
start, end = None, None
walls = detect_walls()
for y in range(height):
    for x in range(width):
        if (x, y) not in walls:
            if start is None:
                start = (x, y)
            else:
                end = (x, y)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 1)  # Draw maze path points

# Solve the maze using the A* algorithm
path = astar(start, end, walls)

# Display the found path on the screen in red
if path:
    pygame.draw.lines(screen, (255, 0, 0), False, [(x + 0.5, y + 0.5) for x, y in path], 1)

# Function to save current Pygame window image
def save_image():
    pygame.image.save(screen, 'maze_path.png')
    print("The image was saved as 'maze_path.png'.")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if a mouse click occurred
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            # Check if the mouse click is on the button (bottom right)
            if width - 110 <= x <= width - 10 and height - 40 <= y <= height - 10:
                save_image()  # Save the image when the button is clicked
                
    pygame.draw.rect(screen, (0, 255, 0), (width - 110, height - 40, 100, 30))  # Green rectangle for the button
    font = pygame.font.Font(None, 36)  # Font
    text = font.render("Save", True, (0, 0, 0))  # Button text
    screen.blit(text, (width - 100, height - 35))  # Display text on the button

    pygame.display.flip()

# When the loop ends, quit pygame
pygame.quit()
