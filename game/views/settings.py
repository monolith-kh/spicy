# -*- coding: utf-8 -*-

import arcade

from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane

from game import FONT, FONT_THIN
from game import app


class SettingsView(arcade.View):

    def __init__(self):
        super().__init__()

        self.settings: app.Settings = self.window.settings

        self.manager = UIManager()
        self.manager.enable()

        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")

        v_box = arcade.gui.UIBoxLayout(vertical=True)

        ui_text_label = arcade.gui.UITextArea(text="Settings",
                                              width=450,
                                              height=100,
                                              font_size=50,
                                              font_name="Kenney Future")
        v_box.add(ui_text_label.with_space_around(bottom=20))

        h_box = arcade.gui.UIBoxLayout(vertical=False)
        h_box.add(
            UITextArea(
                    text='Number of Players',
                    width=450,
                    height=40,
                    font_size=24,
                    font_name="Kenney Future"
            )
        )
        number_of_players = UIInputText(width=100, height=40, font_size=24, text=str(self.settings.number_of_players))
        h_box.add(
            UITexturePane(
                number_of_players,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        v_box.add(h_box.with_space_around(bottom=10))

        h_box = arcade.gui.UIBoxLayout(vertical=False)
        h_box.add(
            UITextArea(
                    text='Basic spawn count',
                    width=450,
                    height=40,
                    font_size=24,
                    font_name="Kenney Future"
            )
        )
        basic_spawn_count = UIInputText(width=100, height=40, font_size=24, text=str(self.settings.basic_spawn_count))
        h_box.add(
            UITexturePane(
                basic_spawn_count,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        v_box.add(h_box.with_space_around(bottom=10))

        h_box = arcade.gui.UIBoxLayout(vertical=False)
        h_box.add(
            UITextArea(
                    text='Auto spawn count',
                    width=450,
                    height=40,
                    font_size=24,
                    font_name="Kenney Future"
            )
        )
        auto_spawn_count = UIInputText(width=100, height=40, font_size=24, text=str(self.settings.auto_spawn_count))
        h_box.add(
            UITexturePane(
                auto_spawn_count,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        v_box.add(h_box.with_space_around(bottom=10))

        h_box = arcade.gui.UIBoxLayout(vertical=False)
        h_box.add(
            UITextArea(
                    text='Auto spawn sec tick',
                    width=450,
                    height=40,
                    font_size=24,
                    font_name="Kenney Future"
            )
        )
        auto_spawn_sec_tick = UIInputText(width=100, height=40, font_size=24, text=str(self.settings.auto_spawn_time))
        h_box.add(
            UITexturePane(
                auto_spawn_sec_tick,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        v_box.add(h_box.with_space_around(bottom=10))

        h_box = arcade.gui.UIBoxLayout(vertical=False)
        h_box.add(
            UITextArea(
                    text='Max spawn count',
                    width=450,
                    height=40,
                    font_size=24,
                    font_name="Kenney Future"
            )
        )
        max_spawn_count = UIInputText(width=100, height=40, font_size=24, text=str(self.settings.max_spawn_count))
        h_box.add(
            UITexturePane(
                max_spawn_count,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        v_box.add(h_box.with_space_around(bottom=20))

        h_box = arcade.gui.UIBoxLayout(vertical=False)

        done_button = arcade.gui.UIFlatButton(text="Done", width=200, style={'font_name': FONT})
        h_box.add(done_button.with_space_around(right=20))

        cancel_button = arcade.gui.UIFlatButton(text="Cancel", width=200, style={'font_name': FONT})
        h_box.add(cancel_button)

        v_box.add(h_box.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=0.0,
                anchor_y="center_y",
                align_y=50.0,
                child=v_box)
        )

        @done_button.event("on_click")
        def on_click_done(event):
            print("Done:", event)
            print(f'{number_of_players.text}, {basic_spawn_count.text}, {auto_spawn_count.text}, {auto_spawn_sec_tick.text}, {max_spawn_count.text}')
            self.settings.number_of_players = int(number_of_players.text)
            self.settings.basic_spawn_count = int(basic_spawn_count.text)
            self.settings.auto_spawn_count = int(auto_spawn_count.text)
            self.settings.auto_spawn_time = float(auto_spawn_sec_tick.text)
            self.settings.max_spawn_count = int(max_spawn_count.text)
            self.window.set_state(app.ArcadeState.menu)

        @cancel_button.event("on_click")
        def on_click_cancel(event):
            print("Cancel:", event)
            self.window.set_state(app.ArcadeState.menu)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_OLIVE_GREEN)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        self.manager.draw()
