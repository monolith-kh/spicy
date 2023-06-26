# -*- coding: utf-8 -*-

import arcade
import arcade.gui

from twisted.internet import reactor

from game import FONT, FONT_THIN
from game import app


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        
        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="Menu",
                                              width=450,
                                              height=100,
                                              font_size=50,
                                              font_name="Kenney Future")
        self.v_box.add(ui_text_label.with_space_around(bottom=20))
        
        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200, style={'font_name': FONT})
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200, style={'font_name': FONT})
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200, style={'font_name': FONT})
        self.v_box.add(quit_button.with_space_around(bottom=20))

        @start_button.event("on_click")
        def on_click_start(event):
            print("Start:", event)
            self.window.set_state(app.ArcadeState.ready)

        @settings_button.event("on_click")
        def on_click_settings(event):
            print("Settings:", event)
            self.window.set_state(app.ArcadeState.settings)

        @quit_button.event("on_click")
        def on_click_quit(event):
            print("quit:", event)
            arcade.exit()
            reactor.callFromThread(reactor.stop)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.csscolor.CHOCOLATE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        ...
