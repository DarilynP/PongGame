import pygame
import random

# === CONSTANTS ===
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def main():
    # === GAME SETUP ===
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    # paddles
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 7, 100)
    paddle_1_move = 0
    paddle_2_move = 0

    # ball
    ball_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 25, 25)
    ball_accel_x = random.choice([-1, 1]) * 0.2
    ball_accel_y = random.choice([-1, 1]) * 0.2


    # start screen
    started = False

    # === GAME LOOP ===
    while True:
        delta_time = clock.tick(60)

        screen.fill(COLOR_BLACK)

        # start screen
        if not started:
            font = pygame.font.SysFont('Consolas', 36)
            text = font.render('Press SPACE to Start', True, COLOR_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = True
            continue  # skip rest of loop until started

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    paddle_1_move = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    paddle_2_move = 0

        # move paddles
        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time

        # keep paddles on screen
        paddle_1_rect.top = max(0, min(paddle_1_rect.top, SCREEN_HEIGHT - paddle_1_rect.height))
        paddle_2_rect.top = max(0, min(paddle_2_rect.top, SCREEN_HEIGHT - paddle_2_rect.height))

        # move ball
        ball_rect.left += ball_accel_x * delta_time
        ball_rect.top += ball_accel_y * delta_time

        # bounce off walls
        if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
            ball_accel_y *= -1

        # bounce off paddles
        if paddle_1_rect.colliderect(ball_rect) and ball_accel_x < 0:
            ball_accel_x *= -1
            ball_rect.left = paddle_1_rect.right + 5
        if paddle_2_rect.colliderect(ball_rect) and ball_accel_x > 0:
            ball_accel_x *= -1
            ball_rect.right = paddle_2_rect.left - 5

        # check if ball goes off screen
        if ball_rect.left <= 0 or ball_rect.right >= SCREEN_WIDTH:
            pygame.quit()
            return

        # draw everything
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)
        pygame.display.update()

if __name__ == "__main__":
    main()
