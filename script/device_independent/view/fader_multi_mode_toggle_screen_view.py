from script.constants import FaderMultiMode
from script.device_independent.util_view.view import View


class FaderMultiModeToggleScreenView(View):
    def __init__(self, action_dispatcher, screen_writer):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def handle_MultiModeFaderStateChangedAction(self, action):
        if action.mode == FaderMultiMode.MixerTrackVolumeMute:
            self.screen_writer.display_notification("Mixer Mode", "Volume / Mute")
        elif action.mode == FaderMultiMode.MixerTrackVolumeArm:
            self.screen_writer.display_notification("Mixer Mode", "Volume / Arm")
        elif action.mode == FaderMultiMode.ChannelVolumeMute:
            self.screen_writer.display_notification("Channel Mode", "Volume / Mute")
        else:
            self.screen_writer.display_notification("Unknown Mode", "Unknown")
