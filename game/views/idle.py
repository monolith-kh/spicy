# -*- coding: utf-8 -*-

import arcade

from game import FONT, FONT_THIN


class IdleView(arcade.View):

    def __init__(self):
        super().__init__()
        # self.logo_sprite = arcade.Sprite('./game/resources/images/logo-white-mono.png', 1.0)
        # self.logo_sprite.center_x = self.window.width / 2
        # self.logo_sprite.center_y = self.window.height / 2-75

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        # self.logo_sprite.draw()
        arcade.draw_text("Cube", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center",
                         font_name=FONT)
        arcade.draw_text("dev", self.window.width / 2, self.window.height / 2-32,
                         arcade.color.GRAY, font_size=15, anchor_x="center",
                         font_name=FONT)
        arcade.draw_text("Monolith", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center",
                         font_name=FONT_THIN)
