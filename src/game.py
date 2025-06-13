"""
Snake Eater
Made with PyGame
"""

from typing import List, TypedDict
import pathlib
import pygame
import sys
import json
import time
import random
import textwrap

FONT = "consolas"
DOWN = "DOWN"
UP = "UP"
LEFT = "LEFT"
RIGHT = "RIGHT"
PIX = 10


class Story(TypedDict):
    title: str
    steps: List[str]


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 15

# Window size
frame_size_x = 720
frame_size_y = 480


# Main logic
def main(story: Story, background_path: pathlib.Path):
    print(background_path)

    # Checks for errors encountered
    check_errors = pygame.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print(f"[!] Had {check_errors[1]} errors when initialising game, exiting...")
        sys.exit(-1)
    else:
        print("[+] Game successfully initialised")

    # Initialise game window
    pygame.display.set_caption("Snake: Reawakening")
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
    background = pygame.transform.scale(
        pygame.image.load(background_path).convert(), (frame_size_x, frame_size_y)
    )
    my_font = pygame.font.SysFont(FONT, 30)

    # Colors (R, G, B)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100 - PIX, 50], [100 - (2 * PIX), 50]]

    food_pos = [
        random.randrange(1, (frame_size_x // PIX)) * PIX,
        random.randrange(1, (frame_size_y // PIX)) * PIX,
    ]
    food_spawn = True

    direction = RIGHT
    change_to = direction

    score = 0

    def on_eat_food():
        print(story)
        title = story["title"]
        current_step = story["steps"][score % len(story["steps"])]
        show_dialogue(f"'{title}' - {current_step}")

    def draw_text_box(text):
        wrapped_text = textwrap.fill(text, 39)
        print(wrapped_text)
        box_rect = pygame.Rect(50 / PIX, 450 / PIX, 720 / PIX, 480 / PIX)
        pygame.draw.rect(game_window, (0, 0, 0), box_rect)
        pygame.draw.rect(game_window, (255, 255, 255), box_rect, 2)
        line_height = my_font.get_height()
        for i, line in enumerate(wrapped_text.splitlines()):
            rendered_line = my_font.render(line, True, (255, 255, 255))
            game_window.blit(
                rendered_line, (box_rect.x + 10, box_rect.y + 10 + i * line_height)
            )

    def show_dialogue(text):
        clock = pygame.time.Clock()
        displayed_text = ""
        index = 0
        last_time = time.time()
        finished_typing = False

        while True:
            overlay = pygame.Surface((frame_size_x, frame_size_y))
            overlay.set_alpha(128)  # 0 = fully transparent, 255 = fully opaque
            overlay.fill((30, 30, 30))  # Gray color

            game_window.blit(overlay, (0, 0))

            # game_window.fill(
            #     (30, 30, 30)
            # )  # Replace with background/game frame if needed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and finished_typing:
                    return  # Exit after full text is typed

            # Typing animation
            now = time.time()
            if not finished_typing and now - last_time > 1 / 30:
                if index < len(text):
                    index += 1
                    displayed_text = text[:index]
                    last_time = now
                else:
                    finished_typing = True

            draw_text_box(displayed_text)
            pygame.display.flip()
            clock.tick(60)

    # Game Over
    def game_over():
        game_over_surface = my_font.render("você perdeu! :(", True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        show_score(0, red, FONT, 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    # Score
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render("Pontuação: " + str(score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x / PIX, 15)
        else:
            score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
        game_window.blit(score_surface, score_rect)
        # pygame.display.flip()

    on_eat_food()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord("w"):
                    change_to = UP
                if event.key == pygame.K_DOWN or event.key == ord("s"):
                    change_to = DOWN
                if event.key == pygame.K_LEFT or event.key == ord("a"):
                    change_to = LEFT
                if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    change_to = RIGHT
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == UP and direction != DOWN:
            direction = UP
        if change_to == DOWN and direction != UP:
            direction = DOWN
        if change_to == LEFT and direction != RIGHT:
            direction = LEFT
        if change_to == RIGHT and direction != LEFT:
            direction = RIGHT

        # Moving the snake
        if direction == UP:
            snake_pos[1] -= PIX
        if direction == DOWN:
            snake_pos[1] += PIX
        if direction == LEFT:
            snake_pos[0] -= PIX
        if direction == RIGHT:
            snake_pos[0] += PIX

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
            on_eat_food()
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [
                random.randrange(1, (frame_size_x // PIX)) * PIX,
                random.randrange(1, (frame_size_y // PIX)) * PIX,
            ]
        food_spawn = True

        # GFX
        game_window.blit(
            background,
            (0, 0),
        )
        pygame.display.flip()

        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], PIX, PIX))

        # Snake food
        pygame.draw.rect(
            game_window, white, pygame.Rect(food_pos[0], food_pos[1], PIX, PIX)
        )

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - PIX:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - PIX:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, FONT, 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)


if __name__ == "__main__":
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    RESOURCE_DIR = BASE_DIR / "resources"
    INDEX = RESOURCE_DIR / "index.json"
    JSON_PATH = RESOURCE_DIR / "adventures.json"
    BACKGROUND_DIR = RESOURCE_DIR / "img" / "backgrounds"

    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            stories: List[Story] = json.load(file)
        with open(INDEX, "r", encoding="utf-8") as file:
            index = json.load(file)
            backgrounds = index["backgrounds"]
    except FileNotFoundError:
        print("File not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)
    main(
        random.choice(stories),
        RESOURCE_DIR / random.choice(backgrounds),
    )
