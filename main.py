# import pygame
# import pyautogui
# import math
# import random
# import sys

# # Initialize pygame
# pygame.init()

# # Set up window
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# width, height = screen.get_size()
# clock = pygame.time.Clock()

# # Spider attributes
# spider_pos = [width // 2, height // 2]
# history = []
# max_history = 100
# legs = 12

# # Main loop
# running = True
# while running:
#     screen.fill((0, 0, 0))  # Black background

#     # Get mouse position
#     mx, my = pyautogui.position()
#     mx = min(mx, width)
#     my = min(my, height)

#     # Smooth movement
#     spider_pos[0] += (mx - spider_pos[0]) * 0.1
#     spider_pos[1] += (my - spider_pos[1]) * 0.1

#     # Save movement history
#     history.append(tuple(spider_pos))
#     if len(history) > max_history:
#         history.pop(0)

#     # Draw spider legs
#     for i in range(legs):
#         index = int(i * (len(history) / legs))
#         if index < len(history):
#             hx, hy = history[index]
#             pygame.draw.line(screen, (255, 255, 255), (spider_pos[0], spider_pos[1]), (hx, hy), 1)

#     # Draw spider body
#     pygame.draw.circle(screen, (255, 255, 255), (int(spider_pos[0]), int(spider_pos[1])), 4)

#     pygame.display.flip()
#     clock.tick(60)  # 60 FPS

#     # Quit on ESC
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             running = False

# pygame.quit()
# sys.exit()



# import pygame
# import pyautogui
# import math
# import random
# import os
# import sys

# # Setup
# pygame.init()
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# width, height = screen.get_size()
# clock = pygame.time.Clock()

# # Load spider image
# spider_img = pygame.image.load("spider.png").convert_alpha()
# spider_img = pygame.transform.scale(spider_img, (80, 80))

# # Star background generator (optional)
# stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(150)]

# # Spider motion
# spider_pos = [width // 2, height // 2]
# trail = []
# trail_length = 80
# legs = 12

# # Main loop
# running = True
# while running:
#     screen.fill((0, 0, 0))

#     # Draw stars
#     for star in stars:
#         pygame.draw.circle(screen, (255, 255, 255), star, 1)

#     # Get mouse position
#     mx, my = pyautogui.position()

#     # Smooth follow
#     spider_pos[0] += (mx - spider_pos[0]) * 0.1
#     spider_pos[1] += (my - spider_pos[1]) * 0.1

#     # Save trail
#     trail.append(tuple(spider_pos))
#     if len(trail) > trail_length:
#         trail.pop(0)

#     # Draw web trails (legs)
#     for i in range(legs):
#         idx = int(i * (len(trail) / legs))
#         if idx < len(trail):
#             hx, hy = trail[idx]
#             pygame.draw.line(screen, (255, 255, 255), spider_pos, (hx, hy), 1)

#     # Draw spider
#     rotated = pygame.transform.rotate(spider_img, 0)  # Could rotate to face cursor
#     rect = rotated.get_rect(center=spider_pos)
#     screen.blit(rotated, rect.topleft)

#     pygame.display.flip()
#     clock.tick(60)

#     # Quit
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             running = False

# pygame.quit()
# sys.exit()




import pygame
import sys
import math
import random

# Setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spider Cursor Animation")
clock = pygame.time.Clock()

# Load spider image
spider_img = pygame.image.load("spider.png").convert_alpha()
spider_img = pygame.transform.scale(spider_img, (60, 60))

# Load click sound
shoot_sound = pygame.mixer.Sound("shoot.wav")

# Trail settings
trail = []
trail_max_len = 20

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Main loop
spider_pos = [width // 2, height // 2]

while True:
    screen.fill((0, 0, 0))

    # Get cursor position
    cursor_pos = pygame.mouse.get_pos()

    # Spider movement
    dx = cursor_pos[0] - spider_pos[0]
    dy = cursor_pos[1] - spider_pos[1]
    speed = min(10, distance(spider_pos, cursor_pos) / 10)
    angle = math.atan2(dy, dx)
    spider_pos[0] += speed * math.cos(angle)
    spider_pos[1] += speed * math.sin(angle)

    # Append to trail
    trail.append(tuple(spider_pos))
    if len(trail) > trail_max_len:
        trail.pop(0)

    # Draw fading trail
    for i in range(len(trail) - 1):
        alpha = int(255 * (i / len(trail)))
        color = (255, 255, 255, alpha)
        pygame.draw.line(screen, color[:3], trail[i], trail[i + 1], 2)

    # Simulate web stretching
    if speed > 4:
        for i in range(8):
            angle_offset = i * (math.pi / 4)
            x = spider_pos[0] + random.randint(30, 50) * math.cos(angle_offset)
            y = spider_pos[1] + random.randint(30, 50) * math.sin(angle_offset)
            pygame.draw.line(screen, (255, 255, 255), spider_pos, (x, y), 1)

    # Draw spider
    spider_rect = spider_img.get_rect(center=spider_pos)
    screen.blit(spider_img, spider_rect)

    # Click = shoot
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shoot_sound.play()

    pygame.display.flip()
    clock.tick(60)
