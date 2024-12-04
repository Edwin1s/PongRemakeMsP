import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
p2_paddle = pygame.Vector2(screen.get_width(), screen.get_height() / 2)
p1_paddle = pygame.Vector2(screen.get_width() - screen.get_width(), screen.get_height() / 2)
paddle_width = 50
paddle_height = 250
ball_radius = 10
previous_pos = pygame.Vector2(ball_pos.x, ball_pos.y)
ball_path = []
ball_path_num = 0
ball_speed = 1
angles = []

for num in range(0, 360):
    angles.append(num)

ball_angle = random.choice(angles)
print(f"The ball_angle is: {ball_angle}")


class Ball:
    def update(self: pygame.Vector2, distance: float):
        angle_rad = math.radians(ball_angle)
        self.x += distance * math.cos(angle_rad)
        self.y += distance * math.sin(angle_rad)
        return self

    def touching_paddle(paddle):
        if paddle == 1:
            if pygame.Rect.colliderect(ball_rect, p1_rect):
                return True
        elif paddle == 2:
            if pygame.Rect.colliderect(ball_rect, p2_rect):
                return True
        return False
    
    def touching_edge():
        if ball_pos.y >= screen.get_height():
            return True
        elif ball_pos.y <= 0:
            return True
        return False

class Paddle:
    def stop_on_edge(paddle): # 1 or 2
        if paddle == 1:
            if p1_paddle.y >= screen.get_height() - paddle_height / 2:
                p1_paddle.y = screen.get_height() - paddle_height / 2
            if p1_paddle.y <= screen.get_height() - screen.get_height() + paddle_height / 2:
                p1_paddle.y = screen.get_height() - screen.get_height() + paddle_height / 2
        elif paddle == 2:
            if p2_paddle.y >= screen.get_height() - paddle_height / 2:
                p2_paddle.y = screen.get_height() - paddle_height / 2
            if p2_paddle.y <= screen.get_height() - screen.get_height() + paddle_height / 2:
                p2_paddle.y = screen.get_height() - screen.get_height() + paddle_height / 2


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("red")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        Ball.update(ball_pos, ball_speed * 2)
    if keys[pygame.K_UP]:
        p2_paddle.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        p2_paddle.y += 300 * dt
    if keys[pygame.K_w]:
        p1_paddle.y -= 300 * dt
    if keys[pygame.K_s]:
        p1_paddle.y += 300 * dt

    # Paddle and ball Rects for detecting collisions
    p2_rect = pygame.Rect(p2_paddle.x - paddle_width / 2, p2_paddle.y - paddle_height / 2, paddle_width, paddle_height)
    p1_rect = pygame.Rect(p1_paddle.x - paddle_width / 2, p1_paddle.y - paddle_height / 2, paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_pos.x - 10 , ball_pos.y - 10, ball_radius * 2, ball_radius * 2)

    # Stopping paddles from going off the screen
    Paddle.stop_on_edge(1)
    Paddle.stop_on_edge(2)

    if Ball.touching_paddle(1):
        if ball_speed == 1:
            incidence_angle = ball_angle
            ball_angle = 270 - ball_angle * 2
            ball_speed = 2
            print(f"Collision with paddle 1, Event: speed 1, Current Speed: {ball_speed}, Entering angle: {incidence_angle}, Angle: {ball_angle}, Code: Paddle1;E.Speed:1")
        elif ball_speed == 2:
            incidence_angle = ball_angle
            ball_angle = 270 + ball_angle * 2
            print(f"Collision with paddle 1, Event: speed 2, Current Speed: {ball_speed}, Entering angle: {incidence_angle}, Angle: {ball_angle}, Code: Paddle1;E.Speed:2")
    elif Ball.touching_paddle(2):
        if ball_speed == 1:
            incidence_angle = ball_angle
            ball_angle = 270 - ball_angle * 2
            ball_speed = 2
            print(f"Collision with paddle 2, Event: speed 1, Current Speed: {ball_speed}, Entering angle: {incidence_angle}, Angle: {ball_angle}, Code: Paddle2;E.Speed:1")
        elif ball_speed == 2:
            incidence_angle = ball_angle
            ball_angle = 270 + ball_angle / 2
            print(f"Collision with paddle 2, Event: speed 2, Current Speed: {ball_speed}, Entering angle: {incidence_angle}, Angle: {ball_angle}, Code: Paddle2;E.Speed:2")
    
    if Ball.touching_edge():
        ball_angle = -ball_angle

    current_pos = pygame.Vector2(ball_pos.x, ball_pos.y)
    if int(previous_pos.x) != int(current_pos.x):
        if int(previous_pos.y) != int(current_pos.y):
            ball_path.append(current_pos)

    pygame.draw.rect(screen, "black", p2_rect)
    pygame.draw.rect(screen, "black", p1_rect)
    pygame.draw.rect(screen, "black", pygame.Rect(screen.get_width() - 10 / 2, screen.get_height(), 10, screen.get_height()))
    for pos in ball_path:
        pygame.draw.circle(screen, "purple", pos, ball_radius / 2)
    pygame.draw.circle(screen, "white", ball_pos, ball_radius)

    if ball_angle > 360:
        ball_angle = 360
    elif ball_angle < -360:
        ball_angle = -360

    Ball.update(ball_pos, ball_speed)
    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit