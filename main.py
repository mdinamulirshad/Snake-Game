import sys, random
import pygame
from pygame.locals import *

def run_game():
    #initialize the game and create the window.
    pygame.init()

    #Screen Settings
    screen_width = 600
    screen_height = 500

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")

    #Set the background color
    bg_color = (220,220,220)

    # Set the snake
    snake_x = 45
    snake_y = 45
    snake_width = 15
    snake_height = 15
    speed_x = 0
    speed_y = 0
    vel = 8

    #Increasing length Snake
    snake_list = []
    snake_length = 1

    #Set Food
    food_width = 15
    food_height = 15
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)

    #Set Score
    score = 0

    #set FPS
    clock = pygame.time.Clock()
    fps = 30

    #Set Score Text
    font = pygame.font.SysFont(None, 30)
    fontstyle = pygame.font.SysFont(None, 60)

    #Set High Score
    with open("high_score.txt", "r") as hs:
        Highscore = hs.read()

    #set new high score
    with open("new_high_score.txt", "r") as nhs:
        NewHighScore = nhs.read()

    #Flag
    game_over = False

    # Show text on the screen
    def text_score(text, color, x, y):
        screen_text = font.render(text, True, color)
        screen.blit(screen_text,(x, y))

    # Show the New High score
    def new_high_score(text, color, x,y):
        new_h_score = fontstyle.render(text, True, color)
        screen.blit(new_h_score,(x,y))

    #Make Snake
    def make_snake(screen, snake_list, snake_width, snake_height):
        for x,y in snake_list:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, snake_width, snake_height))

    #Starting the main loop for the game
    while True:

        #Watch keyboard and mouse event.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #set Key Pressed
            if event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT:
                    speed_x = vel
                    speed_y = 0
                if event.key == K_LEFT:
                    speed_x = -vel
                    speed_y = 0
                if event.key == K_UP:
                    speed_y = -vel
                    speed_x = 0
                if event.key == K_DOWN:
                    speed_y = vel
                    speed_x = 0
                if event.key == K_RETURN:
                    run_game()

        snake_x += speed_x
        snake_y += speed_y

        if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
            score += 10
            food_x = random.randint(20, screen_width / 2)
            food_y = random.randint(20, screen_height / 2)
            snake_length += 2
            if score > int(Highscore):
                Highscore = score

            if int(Highscore) > int(NewHighScore):
                NewHighScore = Highscore

        # Redraw the screen during each pass through the loop
        screen.fill(bg_color)

        #Draw Score
        text_score("Score: " + str(score) + "  High Score: " + str(Highscore),(255, 255, 255), 10, 10)

        # Make Food
        pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, food_width, food_height))

        #Draw Snake
        #pygame.draw.rect(screen, (0,255,0),(snake_x, snake_y, snake_width, snake_height))
        make_snake(screen, snake_list, snake_width, snake_height)

        head = []
        head.append(snake_x)
        head.append(snake_y)
        snake_list.append(head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        if head in snake_list[:-1]:
            game_over = True

        if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
            game_over = True

        if game_over:
            screen.fill(bg_color)
            with open("high_score.txt", "w") as hs:
                hs.write(str(Highscore))
            with open("new_high_score.txt", "w") as nhs:
                nhs.write(str(NewHighScore))

            #Printing New High Score
            if score == int(NewHighScore):
                new_high_score("New High Score: " + str(NewHighScore), (0,0,255), 100, 160)

            text_score("Game Over!", (255,0,0), 240, 220)
            text_score("PRESS ENTER TO PLAY AGAIN", (0, 255, 0), 150, 250)

        #Set FPS
        clock.tick(fps)

        #Make the most recent call to the screen.
        pygame.display.flip()

run_game()
