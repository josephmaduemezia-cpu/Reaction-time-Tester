import pygame
import random
import time
import sys

pygame.init()

WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reaction Time Tester")

font_big = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

STATE_INSTRUCTIONS = 0
STATE_WAITING = 1
STATE_SIGNAL = 2
STATE_RESULT = 3

state = STATE_INSTRUCTIONS
fastest_time = None
start_time = None
wait_until = None


def draw_text(text, y, font, color=(255, 255, 255)):
    text_image = font.render(text, True, color)
    text_position = text_image.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_image, text_position)


running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == STATE_INSTRUCTIONS:
                wait_until = time.time() + random.uniform(2, 5)
                state = STATE_WAITING

            elif state == STATE_SIGNAL:
                reaction_time = int((time.time() - start_time) * 1000)
                if fastest_time is None or reaction_time < fastest_time:
                    fastest_time = reaction_time
                last_result = reaction_time
                state = STATE_RESULT

            elif state == STATE_RESULT:
                wait_until = time.time() + random.uniform(2, 5)
                state = STATE_WAITING

    if state == STATE_INSTRUCTIONS:
        draw_text("Reaction Time Tester", 120, font_big, (255, 200, 0))
        draw_text("Click to begin.", 250, font_small)
        draw_text("Wait for the screen to turn GREEN,", 320, font_small)
        draw_text("then click as fast as you can.", 360, font_small)

    elif state == STATE_WAITING:
        draw_text("Get ready...", 250, font_big)
        draw_text("Don't click until the screen turns GREEN.", 330, font_small)
        if time.time() >= wait_until:
            start_time = time.time()
            state = STATE_SIGNAL

    elif state == STATE_SIGNAL:
        screen.fill((0, 180, 0))
        draw_text("CLICK NOW!", HEIGHT // 2, font_big)

    elif state == STATE_RESULT:
        draw_text(f"Your reaction time: {last_result} ms", 220, font_big, (0, 200, 255))
        if fastest_time is not None:
            draw_text(f"Fastest this session: {fastest_time} ms", 300, font_small)
        draw_text("Click to try again.", 380, font_small)

    pygame.display.flip()

pygame.quit()
sys.exit()
