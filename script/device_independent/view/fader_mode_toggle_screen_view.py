from script.constants import FaderArmMuteMode
from script.device_independent.util_view.view import View


class FaderModeToggleScreenView(View):
    def __init__(self, action_dispatcher, screen_writer):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def handle_ArmSelectStateChangedAction(self, action):
        if action.mode == FaderArmMuteMode.Mute:
            self.screen_writer.display_notification("Mixer Mode", "Volume / Mute")
        elif action.mode == FaderArmMuteMode.Arm:
            self.screen_writer.display_notification("Mixer Mode", "Volume / Arm")
        elif action.mode == FaderArmMuteMode.ChannelVolume:
            self.screen_writer.display_notification("Channel Mode", "Volume / Mute")
        else:
            self.screen_writer.display_notification("Unknown Mode", "Unknown")
