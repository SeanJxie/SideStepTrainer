from arcade import start_render, Window, run, MOUSE_BUTTON_RIGHT, key, set_background_color
from src import settings, objects, utils

"""

A program for League of Legends style side step training 

"""


class SideStepTrainerProgram(Window):  # Child class of arcade's Window class with a bunch of helpful methods
    def __init__(self):
        super().__init__(settings.WINDOW['WIDTH'], settings.WINDOW['HEIGHT'], settings.WINDOW['TITLE'], fullscreen=True)
        set_background_color(settings.WINDOW['BG_COL'])

        # Initialize player
        self.controlled_player = objects.Player(
            {'x': settings.PLAYER['SPAWN_POS'][0], 'y': settings.PLAYER['SPAWN_POS'][1]},
            settings.PLAYER['MOVE_SPEED'],
            settings.PLAYER['RADIUS'],
            settings.PLAYER['COL']
        )
        # Initialize projectile emitter
        self.projectile_emitter = objects.ProjectileEmitter()
        self.target = objects.RandomTargetPoint()

        self.mouse_pos = {}  # Mouse position starts empty
        self.frame_count = 0  # Frame counter for timing logic
        self.fire_interval = settings.GAME['INIT_PROJECTILE_FIRE_FRAME_INTERVAL']  # Initial projectile fire timing
        self.points = 0  # Player points

    def reset(self):
        # Reset all values to initial ones
        self.controlled_player.set_pos({'x': settings.PLAYER['SPAWN_POS'][0], 'y': settings.PLAYER['SPAWN_POS'][1]})
        self.projectile_emitter.clear_projectile_list()
        self.mouse_pos = {}
        self.frame_count = 0
        self.fire_interval = settings.GAME['INIT_PROJECTILE_FIRE_FRAME_INTERVAL']
        self.points = 0
        self.target.set_random_pos()

    def on_draw(self):  # Main render loop
        start_render()
        # Player is rendered "under" projectiles so that the player is consumed by the projectile and not the other ways around
        self.target.render()
        self.controlled_player.render()
        self.projectile_emitter.render_existing_projectiles()

        utils.render_mouse_target(self.mouse_pos, size=settings.GUI['CURSOR_TARGET_SIZE'])
        utils.render_score(self.points)
        utils.render_fs_disclaimer()

    def on_update(self, delta_time: float):  # Main update loop
        if utils.detect_collision(self.controlled_player, self.projectile_emitter.get_projectile_list()):
            self.reset()

        if self.target.detect_collision(self.controlled_player):
            self.points += 1

            if self.fire_interval > settings.GAME['MIN_INIT_PROJECTILE_FIRE_FRAME_INTERVAL']:
                self.fire_interval -= settings.GAME['FIRE_FRAME_INTERVAL_STEP']

        self.controlled_player.move_to(self.mouse_pos, delta_time)  # Move to the current clicked mouse position
        self.projectile_emitter.move_existing_projectiles(delta_time)  # Move all existing projectiles

        # When frame count reaches a given number, fire a projectile at the player and reset frame count
        if self.frame_count == self.fire_interval:
            self.projectile_emitter.fire_projectile_from_random_side(self.controlled_player.get_pos())
            self.frame_count = -1

        # Iterate frames
        self.frame_count += 1

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == MOUSE_BUTTON_RIGHT:  # Set new mouse click position on right button click
            self.mouse_pos.update({'x': x, 'y': y})

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.F:  # Toggle full screen
            self.set_fullscreen(not self.fullscreen)


# Run program
if __name__ == '__main__':
    SideStepTrainerProgram()
    run()
