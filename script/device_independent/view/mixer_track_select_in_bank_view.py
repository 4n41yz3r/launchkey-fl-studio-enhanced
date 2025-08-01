from script.actions import MixerTrackSelectedAction
from script.colour_utils import clamp_brightness, scale_colour
from script.colours import Colours
from script.constants import LedLightingType
from script.device_independent.util_view import View
from script.fl_constants import RefreshFlags


class MixerTrackSelectInBankView(View):
    button_functions = [
        "TrackSelect_1",
        "TrackSelect_2",
        "TrackSelect_3",
        "TrackSelect_4",
        "TrackSelect_5",
        "TrackSelect_6",
        "TrackSelect_7",
        "TrackSelect_8",
    ]

    def __init__(self, action_dispatcher, product_defs, fl, model, button_led_writer):
        super().__init__(action_dispatcher)
        self.action_dispatcher = action_dispatcher
        self.product_defs = product_defs
        self.button_led_writer = button_led_writer
        self.fl = fl
        self.model = model
        self.bright_colour_min_brightness = 100
        self.dim_colour_scale_factor = 0.25

    def _on_show(self):
        self.update_leds()

    def _on_hide(self):
        self.turn_off_leds()

    @property
    def button_to_track_index(self):
        tracks_in_bank = self.model.mixer_tracks_in_active_bank
        return {
            self.product_defs.FunctionToButton.get(function): track
            for function, track in zip(self.button_functions, tracks_in_bank)
        }

    def handle_ButtonPressedAction(self, action):
        if action.button in self.button_to_track_index:
            track_index = self.button_to_track_index[action.button]
            self._select_track(track_index)

    def handle_MixerBankChangedAction(self, action):
        self.update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.LedUpdate.value:
            self.update_leds()

    def get_colour_for_track(self, track_index):
        if self.fl.is_mixer_track_selected(track_index):
            return self.bright_track_colour(self.fl.get_mixer_track_colour(track_index))
        return self.dim_track_colour(self.fl.get_mixer_track_colour(track_index))

    def update_leds(self):
        self.turn_off_leds()
        mute_button = self.product_defs.FunctionToButton.get("TrackSelect")
        self.button_led_writer.set_button_colour(mute_button, Colours.mixer_track_select)
        for button, track_index in self.button_to_track_index.items():
            colour = self.get_colour_for_track(track_index)
            self.button_led_writer.set_button_colour(button, colour, lighting_type=LedLightingType.RGB)

    def turn_off_leds(self):
        mute_button = self.product_defs.FunctionToButton.get("TrackSelect")
        self.button_led_writer.set_button_colour(mute_button, Colours.off)
        for function in self.button_functions:
            button = self.product_defs.FunctionToButton.get(function)
            self.button_led_writer.set_button_colour(button, Colours.off)

    def dim_track_colour(self, base_colour):
        return scale_colour(base_colour, self.dim_colour_scale_factor)

    def bright_track_colour(self, base_colour):
        return clamp_brightness(base_colour, minimum=self.bright_colour_min_brightness)

    def _select_track(self, track_index):
        if not self.fl.is_mixer_track_selected(track_index):
            self.fl.select_mixer_track_exclusively(track_index)
            self.action_dispatcher.dispatch(MixerTrackSelectedAction())
