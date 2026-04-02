import pygame

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Disconnected')
clock = pygame.time.Clock()

x_velocity = 5
y_velocity = 8
bg_x = 0
bg_y = 0
robot_x = 0
robot_y = 230
spike_x = 550
spike_y = 230
score = 99

font = pygame.font.SysFont('Arial', 25)
font_end = pygame.font.SysFont('Arial', 50)

bg = pygame.image.load('background.jpg')
robot = pygame.image.load('robot.png')
spike = pygame.image.load('spike.png')

jump = False
pausing = True
status = True

while status:
    clock.tick(60)
    screen.fill((255, 255, 255))

    bg_rect1 = screen.blit(bg, (bg_x, bg_y))
    bg_rect2 = screen.blit(bg, (bg_x + 600, bg_y))
    score_text = font.render('Diem so: ' + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if not pausing:
        bg_x -= x_velocity
        if bg_x + 600 <= 0:
            bg_x = 0
        spike_x -= x_velocity
        if spike_x <= -20:
            spike_x = 550
            score += 1

    # Nhảy
    if 230 >= robot_y >= 80:
        if jump:
            robot_y -= y_velocity
    else:
        jump = False

    if robot_y < 230:
        if not jump:
            robot_y += y_velocity

    robot_rect = screen.blit(robot, (robot_x, robot_y))
    spike_rect = screen.blit(spike, (spike_x, spike_y))

    # Va chạm
    if robot_rect.colliderect(spike_rect):
        pausing = True
        x_velocity = 0
        y_velocity = 0
        end_text = font_end.render('THUA', True, (0, 0, 0))
        screen.blit(end_text, (200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pausing:
                    x_velocity = 5
                    y_velocity = 8
                    bg_x = 0
                    bg_y = 0
                    robot_x = 0
                    robot_y = 230
                    spike_x = 550
                    spike_y = 230
                    score = 99
                    pausing = False
                else:
                    if robot_y == 230:
                        jump = True

    pygame.display.flip()

pygame.quit()
