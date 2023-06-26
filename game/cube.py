# -*- coding: utf-8 -*-

import arcade

from game import SCREEN_WIDTH, SCREEN_HEIGHT

class Cube(arcade.Sprite):

    def __init__(self, uid, _type, sprite_scaling):
        img = f'./game/resources/images/cube_{_type}.png'
        super().__init__(img, sprite_scaling)

        self.uid = uid
        self._type = _type
        self.change_x = 0
        self.change_y = 0
        
    def update(self):
        
        # move the cube
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1
