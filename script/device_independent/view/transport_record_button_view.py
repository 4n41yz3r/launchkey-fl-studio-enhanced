from script.actions import TransportRecordStateChangedAction
from script.colours import Colours
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class TransportRecordButtonView(View):
    def __init__(
        self,
        action_dispatcher,
        button_led_writer,
        fl,
        product_defs,
        colour_on=Colours.button_toggle_on,
        colour_off=Colours.off,
    ):
        super().__init__(action_dispatcher)
        self.button_led_writer = button_led_writer
        self.fl = fl
        self.product_defs = product_defs
        self.colour_on = colour_on
        self.colour_off = colour_off

    def _on_show(self):
        self.update_led()

    def _on_hide(self):
        self.turn_off_led()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("TransportToggleRecording"):
            self.fl.transport_toggle_recording()
            self.action_dispatcher.dispatch(TransportRecordStateChangedAction())

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.TransportStatus.value:
            self.update_led()

    def update_led(self):
        recording = self.fl.transport_is_recording()
        self.button_led_writer.set_button_colour(
            self.product_defs.FunctionToButton.get("TransportToggleRecording"),
            self.colour_on if recording else self.colour_off,
        )

    def turn_off_led(self):
        self.button_led_writer.set_button_colour(
            self.product_defs.FunctionToButton.get("TransportToggleRecording"), self.colour_off
        )
