from math import dist, degrees, atan2
from src import objects
from arcade import draw_text, get_display_size

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
    size = ht / 20
    draw_text(f'Score: {score}', 0,  ht - 2 * size, (255, 255, 255,), size)
