"""

Settings for the game

"""

WINDOW = {
    'WIDTH': 800,
    'HEIGHT': 800,
    'TITLE': 'SideStep Trainer'
}

PLAYER = {
    'SPAWN_POS': (WINDOW['WIDTH'] / 2, WINDOW['HEIGHT'] / 2),
    'MOVE_SPEED': 5,
    'RADIUS': 25,
    'COL': (0, 255, 0),  # Green
    'MOVE_TO_RADIUS': 3
}

PROJECTILE = {
    'RADIUS_RANGE': (20, 50),
    'SPEED_RANGE': (20, 40),
    'DEG_OFFSET_RANGE': (-2, 2),  # The smaller the range, the more accurate the projectiles
    'COL': (255, 0, 0)  # Red
}

TARGET = {
    'RADIUS': 10,
    'COL': (0, 0, 255)  # Blue
}

GAME = {
    'INIT_PROJECTILE_FIRE_FRAME_INTERVAL': 500,
    'MIN_INIT_PROJECTILE_FIRE_FRAME_INTERVAL': 50,
    'FIRE_FRAME_INTERVAL_STEP': 10
}
