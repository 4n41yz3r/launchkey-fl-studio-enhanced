from script.actions import MixerTrackPluginMixPreviewedAction
from script.constants import Encoders
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class MixerTrackPluginMixPreviewView(View):
    def __init__(self, action_dispatcher, fl):
        super().__init__(action_dispatcher)
        self.fl = fl

    def _on_show(self):
        self._update_previews()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.MixerControls.value:
            self._update_previews()

    def handle_MixerBankChangedAction(self, action):
        self._update_previews()

    def handle_MixerTrackSelectionChangedAction(self, action):
        self._update_previews()

    def _update_previews(self):
        selected_track = self.fl.get_selected_mixer_track()
        
        if selected_track == -1:
            # No track selected, show empty for all encoders
            for control in range(Encoders.Num.value):
                self.action_dispatcher.dispatch(
                    MixerTrackPluginMixPreviewedAction(track=None, plugin_index=control, control=control)
                )
        else:
            # Show plugin mix levels for the selected track
            for plugin_index in range(Encoders.Num.value):
                self.action_dispatcher.dispatch(
                    MixerTrackPluginMixPreviewedAction(
                        track=selected_track, 
                        plugin_index=plugin_index, 
                        control=plugin_index
                    )
                )
