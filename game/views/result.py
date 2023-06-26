# -*- coding: utf-8 -*-

import arcade

from game import FONT, FONT_THIN
from game import app


class ResultView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_SALMON)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Result Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center",
                         font_name=FONT)
        arcade.draw_text("Click to next", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center",
                         font_name=FONT_THIN)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.set_state(app.ArcadeState.menu)
