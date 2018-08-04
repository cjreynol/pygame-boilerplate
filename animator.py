from pygame         import Rect
from pygame.math    import Vector2

from image_loading  import split_surface


class Animator:
    """
    Keeps track of the information needed to animate a Sprite and returns any 
    new images during updates.
    """
    
    def __init__(self, sprite_sheet, size, frame_length, loop):
        """
        Initialize data used for animating the sprite.

        sprite_sheet    - sprite sheet surface, assumes the animation 
                            frames are all in a single row
        size            - width and height of a single image in the sprite_sheet
        frame_length    - number of frames per image in the animation
        loop            - boolean indicating if the animation should restart 
                            at end
        """
        self.frame_length = frame_length
        self.loop = loop
        self.frame_count = 0

        self.images = split_surface(sprite_sheet, size)
        self.image_index = 0

    def update(self, *args):
        """
        Update the frame count and return a new image if the frame length has 
        been reached.
        """
        new_image = None
        if self.frame_count >= self.frame_length:
            self.frame_count = 0

            self.image_index += 1
            if self.image_index >= len(self.images):
                if self.loop:
                    self.image_index = 0
                    new_image = self.get_image()
                else:   # keeps image_index from growing endlessly
                    self.image_index -= 1
            else:
                new_image = self.get_image()

        self.frame_count += 1
        return new_image

    def get_image(self):
        """
        Return the current image.
        """
        return self.images[self.image_index]
