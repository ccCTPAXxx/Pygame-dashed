import math
import random

import pygame

pygame.init()
clock = pygame.time.Clock()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dashed Line")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def dashed_draw_line(surface, color, start, end, width=1, dash_length=10,
                     gap_length=5):
    try:
        dx, dy = end[0] - start[0], end[1] - start[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        angle = math.atan2(dy, dx)
        step = dash_length + gap_length

        for dist in range(0, int(distance), step):
            x = start[0] + dist * math.cos(angle)
            y = start[1] + dist * math.sin(angle)
            x_dash = x + dash_length * math.cos(angle)
            y_dash = y + dash_length * math.sin(angle)
            pygame.draw.line(surface, color, (int(x), int(y)),
                             (int(x_dash), int(y_dash)), width)

        pygame.draw.line(surface, color, (int(x_dash), int(y_dash)), end, width)
    except Exception:
        return Exception


def dashed_draw_aaline(surface, color, start_pos, end_pos, blend):
    # ???????????7
    pygame.draw.aaline(surface, color, start_pos, end_pos, blend)


def dashed_draw_lines(surface, color, closed, pointlist, width=1,
                      dash_length=10, gap_length=5):
    try:
        for i in range(len(pointlist) - 1):
            dashed_draw_line(surface, color, pointlist[i], pointlist[i + 1],
                             width,
                             dash_length, gap_length)
        if closed:
            dashed_draw_line(surface, color, pointlist[-1], pointlist[0], width,
                             dash_length, gap_length)
    except Exception:
        return Exception


def draw_dashed_circle(surface, color, center, radius, width=1, dash_length=10,
                       gap_length=5):
    try:
        x, y = center
        num_points = int(2 * math.pi * radius)
        points = [(x + int(radius * math.cos(2 * math.pi * i / num_points)),
                   y + int(radius * math.sin(2 * math.pi * i / num_points))) for
                  i in range(num_points)]

        for i in range(0, len(points), dash_length + gap_length):
            end_index = min(i + dash_length, len(points))
            pygame.draw.lines(surface, color, False, points[i:end_index], width)
    except Exception:
        return Exception


def dashed_draw_ellipse(surface, color, rect, width=1, dash_length=10,
                        gap_length=5):
    try:
        dash_length *= 2
        gap_length *= 2
        x, y, width_h, height = rect
        if width_h < 1 or height < 1:
            return

        points = []
        num_points = int(2 * max(width_h, height) * math.pi)
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x_point = x + width_h / 2 + int(width_h / 2 * math.cos(angle))
            y_point = y + height / 2 + int(height / 2 * math.sin(angle))
            points.append((x_point, y_point))

        for i in range(0, len(points), dash_length + gap_length):
            pygame.draw.lines(surface, color, False, points[i:i + dash_length],
                              width=width)
    except Exception:
        return Exception


def dashed_draw_arc(surface, color, rect, start_angle, stop_angle, width=1,
                    dash_length=10, gap_length=5):
    try:
        x, y, width_h, height = rect
        if width_h < 1 or height < 1:
            return

        num_points = int(
            abs(stop_angle - start_angle) * max(width_h, height) * 0.5)
        points = []
        for i in range(num_points):
            angle = start_angle + (stop_angle - start_angle) * i / num_points
            x_point = x + width_h / 2 + int(width_h / 2 * math.cos(angle))
            y_point = y + height / 2 + int(height / 2 * math.sin(angle))
            points.append((x_point, y_point))

        for i in range(0, len(points), dash_length + gap_length):
            end_index = min(i + dash_length, len(points))
            pygame.draw.lines(surface, color, False, points[i:end_index], width)
    except Exception:
        return Exception


def dashed_draw_polygon(surface, color, pointlist, width=1, dash_length=10,
                        gap_length=5):
    try:
        for i in range(len(pointlist)):
            start = pointlist[i]
            end = pointlist[(i + 1) % len(pointlist)]
            dashed_draw_line(surface, color, start, end, width, dash_length,
                             gap_length)
    except Exception:
        return Exception


def dashed_draw_rect(surface, color, rect, width=1, dash_length=10,
                     gap_length=5):
    try:
        x, y, w, h = rect
        pointlist = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        dashed_draw_polygon(surface, color, pointlist, width, dash_length,
                            gap_length)
    except Exception:
        return Exception


colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
          (255, 0, 255)]
window = screen
FPS = 1


def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        for _ in range(50):
            color = random.choice(colors)
            shape = random.choice(
                ['rect', 'circle', 'polygon', 'ellipse', 'arc', 'line'])
            size = random.randint(20, 100)
            pos_x = random.randint(0, width - size)
            pos_y = random.randint(0, height - size)

            if shape == 'rect':
                dashed_draw_rect(window, color, (pos_x, pos_y, size, size),
                                 random.randint(1, 5))
            elif shape == 'circle':
                draw_dashed_circle(window, color, (pos_x, pos_y), size // 2,
                                   random.randint(1, 5))
            elif shape == 'polygon':
                points = [(pos_x, pos_y), (pos_x + size, pos_y),
                          (pos_x + size // 2, pos_y + size)]
                dashed_draw_polygon(window, color, points, random.randint(1, 5))
            elif shape == 'ellipse':
                dashed_draw_ellipse(window, color,
                                    (pos_x, pos_y, size, size // 2),
                                    random.randint(1, 5))
            elif shape == 'arc':
                dashed_draw_arc(window, color, (pos_x, pos_y, size, size), 0,
                                math.radians(random.randint(0, 360)),
                                random.randint(1, 5))
            elif shape == 'line':
                end_x = random.randint(0, width)
                end_y = random.randint(0, height)
                dashed_draw_line(window, color, (pos_x, pos_y), (end_x, end_y),
                                 3)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


main()
