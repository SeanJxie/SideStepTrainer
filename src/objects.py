from math import sin, cos, atan2, degrees, radians
from arcade import draw_circle_filled
from random import choice, randint
from src import settings, utils

"""

Classes for in game objects

"""


class Player:
    def __init__(self, init_pos, move_speed, radius, col):
        self.pos = init_pos
        self.move_speed = move_speed
        self.radius = radius
        self.col = col

        self.deg = 0

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def move_to(self, pos, dt):
        if pos != {}:
            if not utils.within_radius(pos, self.pos, r=settings.PLAYER['MOVE_TO_RADIUS']):  # Gets rid of "shaking" bug
                dx = pos['x'] - self.pos['x']
                dy = pos['y'] - self.pos['y']

                rad = atan2(dy, dx)
                self.deg = degrees(rad)

                self.pos['x'] += self.move_speed * cos(rad) * dt * 60  # Convert to seconds
                self.pos['y'] += self.move_speed * sin(rad) * dt * 60

    def flash(self):
        pass

    def render(self):
        draw_circle_filled(self.pos['x'], self.pos['y'], self.radius, self.col)


class Projectile:
    def __init__(self, init_pos, init_deg, move_speed, radius):
        self.pos = init_pos
        self.deg = init_deg  # Using degrees because it's easier for me to read :D
        self.move_speed = move_speed
        self.radius = radius

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def move(self, dt):
        rad = radians(self.deg)

        self.pos['x'] += self.move_speed * cos(rad) * dt * 60  # Convert to seconds
        self.pos['y'] += self.move_speed * sin(rad) * dt * 60

    def render(self):
        draw_circle_filled(self.pos['x'], self.pos['y'], self.radius, settings.PROJECTILE['COL'])


class ProjectileEmitter:
    """

    Using the Projectile class

    """

    def __init__(self):
        self.projectile_list = []
        self.full_wt, self.full_ht = utils.get_display_size()

    def get_projectile_list(self):
        return self.projectile_list

    def clear_projectile_list(self):
        self.projectile_list.clear()

    def fire_projectile_from_random_side(self, player_pos):
        # Create a random projectile located around the viewport

        # Input vars to the Projectile class which will be randomly selected
        # Radius and speed are the same for every edge so they are defined here
        radius = randint(settings.PROJECTILE['RADIUS_RANGE'][0], settings.PROJECTILE['RADIUS_RANGE'][1])
        speed = randint(settings.PROJECTILE['SPEED_RANGE'][0], settings.PROJECTILE['SPEED_RANGE'][1])

        # Position and degree are different for every edge of the screen so they'll be chosen based on the edge selection
        pos = {'x': 0, 'y': 0}

        random_side = choice((1, 2, 3, 4))  # Pick a side

        if random_side == 1:  # Left
            pos.update({'x': -radius / 2, 'y': randint(0, self.full_ht)})

        elif random_side == 2:  # Right
            pos.update({'x': self.full_wt + radius / 2, 'y': randint(0, self.full_ht)})

        elif random_side == 3:  # Bottom
            pos.update({'x': randint(0, self.full_wt), 'y': -radius / 2})

        elif random_side == 4:  # Top
            pos.update({'x': randint(0, self.full_wt), 'y': self.full_ht + radius / 2})

        random_deg_offset = randint(settings.PROJECTILE['DEG_OFFSET_RANGE'][0], settings.PROJECTILE['DEG_OFFSET_RANGE'][1])
        self.projectile_list.append(Projectile(pos, utils.get_deg_between(pos, player_pos) + random_deg_offset, speed, radius))

    def move_existing_projectiles(self, dt):
        for p in self.projectile_list:
            p.move(dt)

            in_x_range = -p.get_radius() / 2 <= p.get_pos()['x'] <= self.full_wt + p.get_radius() / 2
            in_y_range = -p.get_radius() / 2 <= p.get_pos()['y'] <= self.full_ht + p.get_radius() / 2

            if not in_x_range or not in_y_range:
                # Removing instance p by redefining the list with the instance p excluded
                self.projectile_list = [projectile for projectile in self.projectile_list if projectile != p]

    def render_existing_projectiles(self):
        for p in self.projectile_list:
            p.render()


class RandomTargetPoint:
    def __init__(self):
        self.full_wt, self.full_ht = utils.get_display_size()
        self.pos = {'x': randint(0, self.full_wt), 'y': randint(0, self.full_ht)}

    @staticmethod
    def get_radius():
        return settings.TARGET['RADIUS']

    def get_pos(self):
        return self.pos

    def set_random_pos(self):
        self.pos = {'x': randint(0, self.full_wt), 'y': randint(0, self.full_ht)}

    def render(self):
        draw_circle_filled(self.pos['x'], self.pos['y'], settings.TARGET['RADIUS'], settings.TARGET['COL'])

    def detect_collision(self, player):
        if utils.detect_collision(player, self):
            self.set_random_pos()
            return True
