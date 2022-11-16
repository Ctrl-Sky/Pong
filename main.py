import pygame
import sys
import random


class Rect:
    def __init__(self, width, height, speed_x, speed_y):
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y


class Button:
    def __init__(self, x_pos, y_pos, text_input, font, colour, hovering_colour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.font = font
        self.colour = colour
        self.hovering_colour = hovering_colour
        self.text = self.font.render(self.text_input, True, self.colour)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.text, self.rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_colour(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.colour)


pygame.init()

# Screen info
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colours
bg_colour = pygame.Color('grey12')
light_grey = (200, 200, 200)
white = (255, 255, 255)

# Creating objects
clock = pygame.time.Clock()
ball_rect = Rect(30, 30, 7, 7)
player_rect = Rect(10, 140, 7, 0)
opponent_rect = Rect(10, 140, 6, 6)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Printing scores
player_score = 0
opponent_score = 0

score_time = True
multiplayer = False
pause = False


def get_font(size):
    return pygame.font.Font("freesansbold.ttf", size)


def ball_animations():
    global player_score, opponent_score, score_time

    # Ball movement
    ball.x += ball_rect.speed_x
    ball.y += ball_rect.speed_y

    # Prevent ball from leaving screen
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_rect.speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_rect.speed_x *= -1

    # Collision with player and opponent

    if ball.colliderect(player):
        if abs(ball.right - player.left) < 10 and ball_rect.speed_x > 0:
            ball_rect.speed_x *= -1
        if abs(ball.top - player.bottom) < 10 and ball_rect.speed_y < 0:
            ball_rect.speed_y *= -1
        if abs(ball.bottom - player.top) < 10 and ball_rect.speed_y > 0:
            ball_rect.speed_y *= -1

    if ball.colliderect(opponent):
        if abs(ball.left - opponent.right) < 10 and ball_rect.speed_x < 0:
            ball_rect.speed_x *= -1
        if abs(ball.top - opponent.bottom) < 10 and ball_rect.speed_y < 0:
            ball_rect.speed_y *= -1
        if abs(ball.bottom - opponent.top) < 10 and ball_rect.speed_y > 0:
            ball_rect.speed_y *= -1

    # If player or opponent scores point
    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()


def player_animations():
    global pause

    if not pause:
        player.y += player_rect.speed_y
    if player.top <= 0:
        player.top = 0
    if player.bottom >= 960:
        player.bottom = 960


def opponent_animations():
    global multiplayer, pause

    # Opponent moves by following ball
    if multiplayer:
        if not pause:
            opponent.y += opponent_rect.speed_y
    else:
        if opponent.y > ball.y:
            opponent.y -= opponent_rect.speed_y
        if opponent.y < ball.y:
            opponent.y += opponent_rect.speed_y

    # Prevent opponent from exiting screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= 960:
        opponent.bottom = 960


def ball_restart():
    global score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    # Countdown before ball begins moving
    if current_time - score_time < 700:
        number_three = get_font(32).render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = get_font(32).render("2", False, light_grey)
        screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = get_font(32).render("1", False, light_grey)
        screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

    # Counter before ball begins moving
    if current_time - score_time < 2100:
        ball_rect.speed_x, ball_rect.speed_y = 0, 0
    else:
        ball_rect.speed_x = 7 * random.choice((1, -1))
        ball_rect.speed_y = 7 * random.choice((1, -1))
        score_time = None


def game():
    global multiplayer, pause
    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_rect.speed_y += 7
                if event.key == pygame.K_UP:
                    player_rect.speed_y -= 7

                if event.key == pygame.K_ESCAPE:
                    counter = counter + 1

                    if counter % 2 == 0:
                        ball_rect.speed_y = temp_speed_y
                        ball_rect.speed_x = temp_speed_x
                        if multiplayer:
                            opponent_rect.speed_y = 0
                        else:
                            opponent_rect.speed_y = temp_opponent_speed
                        pause = False
                    else:
                        temp_speed_y = ball_rect.speed_y
                        temp_speed_x = ball_rect.speed_x
                        temp_opponent_speed = opponent_rect.speed_y
                        ball_rect.speed_y = 0
                        ball_rect.speed_x = 0
                        opponent_rect.speed_y = 0
                        pause = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_rect.speed_y -= 7
                if event.key == pygame.K_UP:
                    player_rect.speed_y += 7

                if event.type == pygame.K_ESCAPE:
                    ball_rect.speed_y = 0
                    ball_rect.speed_x = 0
                    player_rect.speed_y = 0
                    opponent_rect.speed_y = 0

            if multiplayer:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        opponent_rect.speed_y += 7
                    if event.key == pygame.K_w:
                        opponent_rect.speed_y -= 7

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        opponent_rect.speed_y -= 7
                    if event.key == pygame.K_w:
                        opponent_rect.speed_y += 7

        ball_animations()
        player_animations()
        opponent_animations()

        # Draw to screen
        screen.fill(bg_colour)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

        if score_time:
            ball_restart()

        player_text = get_font(32).render(f"{player_score}", False, light_grey)
        screen.blit(player_text, (660, 470))

        opponent_text = get_font(32).render(f"{opponent_score}", False, light_grey)
        screen.blit(opponent_text, (600, 470))

        pygame.display.flip()
        clock.tick(60)


def menu():
    global multiplayer, score_time

    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        screen.fill(bg_colour)
        title_text = get_font(100).render("Pong", False, light_grey)
        title_text_rect = title_text.get_rect(center=(screen_width/2, screen_height/2 - 110))

        one_player_button = Button(x_pos=screen_width/2, y_pos=screen_height/2, text_input="1 Player", font=get_font(50), colour=light_grey, hovering_colour=white)
        two_player_button = Button(x_pos=screen_width/2, y_pos=screen_height/2 + 75, text_input="2 Player", font=get_font(50), colour=light_grey, hovering_colour=white)

        for button in [one_player_button, two_player_button]:
            button.change_colour(play_mouse_pos)
            button.update()
        screen.blit(title_text, title_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if one_player_button.check_for_input(play_mouse_pos):
                    multiplayer = False
                    score_time = pygame.time.get_ticks()
                    game()
                if two_player_button.check_for_input(play_mouse_pos):
                    opponent_rect.speed_y = 0
                    multiplayer = True
                    score_time = pygame.time.get_ticks()
                    game()

        pygame.display.flip()
        clock.tick(60)

menu()
