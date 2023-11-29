import pygame
import random
pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (30, 30, 100)

print("Do you wish to manually scale the display?(y or n)")
input_width_height = 800
input_tile = 20
if input().lower().startswith('y'):
    print("What should be the width or height? (Min 400, Max 1450)")
    input_width_height = int(input())
    if (input_width_height > 1450):
        input_width_height = 1450
    if (input_width_height < 400):
        input_width_height = 400

    print("What should be the size of each tile?")
    input_tile = int(input())

WIDTH, HEIGHT = input_width_height, input_width_height
TILE_SIZE = input_tile
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()


# Pressing "g" will place life across the  board in random places
def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


# This function draws the grid (initialisation)
def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, BLUE, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


# input in all live cells in the current generation
def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    # iterate through all live cells and find their neighbors
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        # only gives us alve cells out of neighbors
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    # check neighbors of neighbors to make cells alive
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or y + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))

    return neighbors


def main():
    drawing = False
    running = True
    playing = False
    count = 0
    update_freq = 40

    positions = set()
    positions.add((10, 10))
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # This event add/removes life by a single mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)
                if event.type == pygame.MOUSEBUTTONUP:
                    break

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            # Start drawing when the mouse button is pressed and held
            # play will be paused once started drawing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                playing = False

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False
            # Draw continuously while the left mouse button is held down
            elif event.type == pygame.MOUSEMOTION and drawing:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos not in positions:
                    positions.add(pos)

            # Play and pause feature (Press space_bar)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2, 5) * GRID_WIDTH)

        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
