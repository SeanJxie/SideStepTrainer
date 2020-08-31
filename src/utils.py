from math import dist, degrees, atan2

import pyglet
from arcade import draw_text, draw_line

from src import objects

"""

Helpful Functions

"""


def detect_collision(player, other):
    """Detect collision between player and all projectiles"""
    if type(other) == objects.RandomTargetPoint:
        if within_radius(player.get_pos(), other.get_pos(), player.get_radius() + other.get_radius()):
            return True

        else:
            return False

    else:
        for o in other:
            if within_radius(player.get_pos(), o.get_pos(), player.get_radius() + o.get_radius()):
                return True

            else:
                return False


def within_radius(p1, p2, r):
    """Check if 2 points in dict form are within a given radius of one another"""
    return True if dist(p1.values(), p2.values()) <= r else False


def get_deg_between(p1, p2):
    """Get the angle between 2 points in dict form"""
    dx = p2['x'] - p1['x']
    dy = p2['y'] - p1['y']

    return degrees(atan2(dy, dx))


def render_score(score):
    ht = get_display_size()[1]
    size = ht / 30
    draw_text(f'Score: {score}', 0, ht - 2 * size, (255, 255, 255), size)


def render_fs_disclaimer():
    wt, ht = get_display_size()
    size = ht / 30

    draw_text(f'This game is meant to be played in full screen mode. Press F to toggle full screen.', wt / 6, ht - 2 * size,
              (255, 255, 255), size)


def render_mouse_target(pos, size=10):
    if pos != {}:
        top = pos['x'], pos['y'] + size / 2
        bot = pos['x'], pos['y'] - size / 2
        left = pos['x'] - size / 2, pos['y']
        right = pos['x'] + size / 2, pos['y']

        draw_line(top[0], top[1], bot[0], bot[1], (255, 255, 255), size / 4)
        draw_line(left[0], left[1], right[0], right[1], (255, 255, 255), size / 4)


"""Copied directly from arcade 2.4 documentation for compilation convenience"""


def get_display_size(screen_id: int = 0):
    """Return the width and height of a monitor.

    The size of the primary monitor is returned by default.

    :param int screen_id: The screen number
    :return: Tuple containing the width and height of the screen
    :rtype: tuple
    """
    display = pyglet.canvas.Display()
    screen = display.get_screens()[screen_id]
    return screen.width, screen.height
