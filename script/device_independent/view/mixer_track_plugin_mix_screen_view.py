from script.constants import Encoders
from script.device_independent.util_view.view import View


class MixerTrackPluginMixScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, fl):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.fl = fl

    def handle_MixerTrackPluginMixChangedAction(self, action):
        self.display_plugin_mix(action.control, action.track, action.plugin_index)

    def handle_MixerTrackPluginMixPreviewedAction(self, action):
        if action.track is None:
            self.screen_writer.display_parameter(action.control, title="", name="Not Used", value="")
        else:
            self.display_plugin_mix(action.control, action.track, action.plugin_index)

    def display_plugin_mix(self, control, track, plugin_index):
        # Get plugin mix level (0.0 to 1.0)
        mix_level = self.fl.get_mixer_track_plugin_mix_level(track, plugin_index)
        
        # Convert to percentage
        mix_percentage = int(mix_level * 100)
        
        # Get track name and format display
        track_name = self.fl.get_mixer_track_name(track)
        plugin_name = self.fl.get_plugin_for_selected_mixer_track(plugin_index)
        title = track_name if track_name else f"Track {track}"
        name = (plugin_name if plugin_name else f"Slot {plugin_index + 1} Mix")
        value = f"{mix_percentage}%"
        
        self.screen_writer.display_parameter(control, title=title, name=name, value=value)
