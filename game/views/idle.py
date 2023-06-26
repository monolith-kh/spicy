# -*- coding: utf-8 -*-

import arcade

from game import FONT, FONT_THIN


class IdleView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Cube", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center",
                         font_name=FONT)
        arcade.draw_text("dev", self.window.width / 2, self.window.height / 2-32,
                         arcade.color.GRAY, font_size=15, anchor_x="center",
                         font_name=FONT)
        arcade.draw_text("Monolith", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center",
                         font_name=FONT_THIN)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        ...
