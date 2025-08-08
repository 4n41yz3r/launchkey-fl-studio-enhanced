from script.actions import MixerTrackPluginMixChangedAction
from script.constants import ControlChangeType, Encoders
from script.device_independent.util_view.view import View
from script.device_independent.view.control_change_rate_limiter import ControlChangeRateLimiter
from util.deadzone import Deadzone


class MixerTrackPluginMixView(View):
    def __init__(self, action_dispatcher, fl, model, *, control_to_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.model = model
        self.control_to_index = control_to_index
        self.deadzone = Deadzone(maximum=1.0, centre=0.0, width=0.05)
        self.reset_pickup_on_first_movement = False
        self.control_change_rate_limiter = ControlChangeRateLimiter(action_dispatcher)

    def _on_show(self):
        self.reset_pickup_on_first_movement = True
        self.control_change_rate_limiter.start()

    def _on_hide(self):
        self.control_change_rate_limiter.stop()

    def handle_MixerBankChangedAction(self, action):
        self.control_change_rate_limiter.reset()
        self.reset_pickup_on_first_movement = True

    def handle_ControlChangedAction(self, action):
        index = self.control_to_index.get(action.control)
        if index is None or index >= Encoders.Num.value:
            return

        # Get the currently selected mixer track
        selected_track = self.fl.get_selected_mixer_track()
        if selected_track == -1:
            return

        plugin_index = index  # Each encoder controls one plugin slot (0-7)

        is_absolute_control = action.control_change_type == ControlChangeType.Absolute.value
        if is_absolute_control and self.reset_pickup_on_first_movement:
            self.reset_pickup_on_first_movement = False
            self._reset_pickup_for_current_track()

        current_mix_level = self.fl.get_mixer_track_plugin_mix_level(selected_track, plugin_index)
        new_mix_level = self.deadzone(action.control_change_type, action.value, current_mix_level)
        
        if self.control_change_rate_limiter.forward_control_change_event(f"{selected_track}_{plugin_index}", new_mix_level):
            self.fl.set_mixer_track_plugin_mix_level(selected_track, plugin_index, new_mix_level)
            self.action_dispatcher.dispatch(
                MixerTrackPluginMixChangedAction(
                    track=selected_track, 
                    plugin_index=plugin_index, 
                    control=action.control
                )
            )

    def _reset_pickup_for_current_track(self):
        selected_track = self.fl.get_selected_mixer_track()
        if selected_track != -1:
            for plugin_index in range(Encoders.Num.value):
                # FL Studio doesn't have a specific plugin mix pickup reset, 
                # so we'll skip this optimization for now
                pass
