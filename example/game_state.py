from os                         import path

from pygame                     import Rect, Surface
from pygame.locals              import (QUIT, K_DOWN, K_ESCAPE, K_LEFT, 
                                            K_UP, K_RIGHT, KEYDOWN, KEYUP)
from pygame.sprite              import Sprite, RenderUpdates

from boilerplate.image_loading  import load_image
from boilerplate.game_state_abc import GameStateABC
from boilerplate.movable_sprite import MovableSprite


class GameState(GameStateABC):
    """
    """
    
    GHOST_ANIMATION_LENGTH = 5      # in frames
    GRAVITY = (0, 256)
    VELOCITY = 128
    JUMP_VELOCITY = VELOCITY * 2

    IMG_DIR = path.join("example", "assets")

    def __init__(self, fps):
        super().__init__(fps)

        self.ghost = self._create_ghost()
        self.ghost_group = RenderUpdates(self.ghost)

        walls = self._create_walls()
        self.wall_group = RenderUpdates(*walls)

    def get_all_groups(self):
        return [self.ghost_group, self.wall_group]

    def get_collide_groups(self):
        return [self.wall_group]

    def _create_ghost(self):
        ghost_path = path.join(self.IMG_DIR, "boo_spritesheet.png")
        sprite_sheet = load_image(ghost_path)
        ghost =  MovableSprite(sprite_sheet, (32, 32), 
                                self.GHOST_ANIMATION_LENGTH, True)
        ghost.rect.midtop = (384, 304)
        ghost.change_acceleration(self.GRAVITY)
        return ghost

    def _create_walls(self):
        screen_width = 800
        screen_height = 640
        square_size = 32

        wall_path = path.join(self.IMG_DIR, "wood_panel_tile.png")
        wall_tile = load_image(wall_path)

        bottom = Surface((screen_width, square_size))
        left = Surface((square_size, screen_height))
        right = Surface((square_size, screen_height))

        platform = Surface((square_size * 5, square_size))

        rect = Rect(0, 0, 0, 0)
        for i in range(screen_width // square_size):
            rect.left = i * square_size
            bottom.blit(wall_tile, rect)

        rect.left = 0
        for i in range(screen_height // square_size):
            rect.top = i * square_size
            left.blit(wall_tile, rect)
            right.blit(wall_tile, rect)

        rect.top = 0
        for i in range(5):
            rect.left = i * square_size
            platform.blit(wall_tile, rect)

        bot_sprite = Sprite()
        bot_sprite.image = bottom
        bot_sprite.rect = bot_sprite.image.get_rect()
        bot_sprite.rect.topleft = (0, screen_height - square_size)

        left_sprite = Sprite()
        left_sprite.image = left
        left_sprite.rect = left_sprite.image.get_rect()
        left_sprite.rect.topleft = (0, 0)

        right_sprite = Sprite()
        right_sprite.image = right
        right_sprite.rect = right_sprite.image.get_rect()
        right_sprite.rect.topleft = (screen_width - square_size, 0)

        platform_sprite = Sprite()
        platform_sprite.image = platform
        platform_sprite.rect = platform_sprite.image.get_rect()
        platform_sprite.rect.topleft = (screen_width // 2 - square_size * 2.5,
                                            screen_height * 4 // 5)

        return [bot_sprite, left_sprite, right_sprite, platform_sprite]

    def handle_events(self, event_list):
        for event in event_list:
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                self.done = True

            if event.type == KEYDOWN and event.key == K_DOWN:
                self.ghost.change_velocity((0, self.VELOCITY))
            elif event.type == KEYUP and event.key == K_DOWN:
                self.ghost.change_velocity((0, -self.VELOCITY))

            elif (event.type == KEYDOWN and event.key == K_UP 
                    and not self.ghost.jumping):
                self.ghost.change_velocity((0, -self.JUMP_VELOCITY))
                self.ghost.jumping = True
                
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.ghost.change_velocity((self.VELOCITY, 0))
            elif event.type == KEYUP and event.key == K_RIGHT:
                self.ghost.change_velocity((-self.VELOCITY, 0))

            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.ghost.change_velocity((-self.VELOCITY, 0))
            elif event.type == KEYUP and event.key == K_LEFT:
                self.ghost.change_velocity((self.VELOCITY, 0))