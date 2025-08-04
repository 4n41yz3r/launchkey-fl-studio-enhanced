from script.action_generators.surface_action_generator.surface_actions import MultiModeFaderStateChangedAction
from script.constants import ChannelNavigationMode, FaderMultiMode, Faders
from script.device_independent.view import (
    ChannelMuteToggleView,
    ChannelRackVolumeScreenView,
    ChannelRackVolumeView,
    FaderMultiModeToggleScreenView,
    MixerMuteView,
    MixerTrackRecordArmToggleView,
    MixerVolumeView,
    MixerVolumeScreenView,
)
from util.control_to_index import make_control_to_index


class MultiModeFaderLayoutManager:
    def __init__(
        self,
        action_dispatcher,
        command_dispatcher,
        fl,
        model,
        fl_window_manager,
        product_defs,
        button_led_writer,
        screen_writer,
    ):
        self.action_dispatcher = action_dispatcher
        self.fl_window_manager = fl_window_manager
        self.command_dispatcher = command_dispatcher
        self.product_defs = product_defs
        self.model = model
        self.button_led_writer = button_led_writer
        self.screen_writer = screen_writer
        
        # Create control to index mapping for faders
        control_to_index = make_control_to_index(Faders.FirstControlIndex.value, Faders.NumRegularFaders.value)
        
        # Common views
        self.fader_mode_toggle_screen_view = FaderMultiModeToggleScreenView(action_dispatcher, screen_writer)

        # Mixer-related views
        self.mixer_fader_view = MixerVolumeView(action_dispatcher, fl, model, control_to_index=control_to_index)
        self.mixer_volume_screen_view = MixerVolumeScreenView(action_dispatcher, screen_writer, fl)
        self.mixer_record_arm_view = MixerTrackRecordArmToggleView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.mixer_mute_view = MixerMuteView(action_dispatcher, model, product_defs, fl, button_led_writer)
        
        # Channel-related views
        self.channel_fader_view = ChannelRackVolumeView(action_dispatcher, fl, model, control_to_index=control_to_index)
        self.channel_volume_screen_view = ChannelRackVolumeScreenView(action_dispatcher, screen_writer, fl)
        self.channel_mute_view = ChannelMuteToggleView(action_dispatcher, product_defs, fl, model, button_led_writer)

    @property
    def current_mode(self):
        return getattr(self.model, 'mixer_arm_mute_mode', FaderMultiMode.MixerTrackVolumeArm)

    @property
    def views(self):
        """Return the appropriate views based on current mode"""
        if self.current_mode == FaderMultiMode.ChannelVolumeMute:
            # Channel volume mode: faders control channels, buttons toggle channel mute
            return {
                self.channel_fader_view,
                self.channel_volume_screen_view,
                self.channel_mute_view,
                self.fader_mode_toggle_screen_view,
            }
        else:
            # Mixer modes: faders control mixer tracks
            button_view = self.mixer_record_arm_view if self.is_mixer_record_arm_view_enabled else self.mixer_mute_view
            return {
                self.mixer_fader_view,
                self.mixer_volume_screen_view,
                self.fader_mode_toggle_screen_view,
                button_view,
            }

    @property
    def is_mixer_record_arm_view_enabled(self):
        return self.current_mode == FaderMultiMode.MixerTrackVolumeArm

    def show(self):
        self.action_dispatcher.subscribe(self)
        self.model.channel_rack.navigation_mode = ChannelNavigationMode.Bank
        for view in self.views:
            view.show()

    def hide(self):
        self.action_dispatcher.unsubscribe(self)
        for view in self.views:
            view.hide()

    def focus_windows(self):
        self.fl_window_manager.hide_last_focused_plugin_window()
        if self.current_mode == FaderMultiMode.ChannelVolumeMute:
            self.fl_window_manager.focus_channel_window()
        else:
            self.fl_window_manager.focus_mixer_window()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("ArmSelect"):
            self._cycle_fader_mode()

    def _cycle_fader_mode(self):
        self.hide()
        
        if self.current_mode == FaderMultiMode.MixerTrackVolumeArm:
            new_mode = FaderMultiMode.ChannelVolumeMute
        elif self.current_mode == FaderMultiMode.ChannelVolumeMute:
            new_mode = FaderMultiMode.MixerTrackVolumeMute
        else:  # Mute
            new_mode = FaderMultiMode.MixerTrackVolumeArm
        
        # Update the model
        self.model.mixer_arm_mute_mode = new_mode
        
        # Show views and focus appropriate window
        self.show()
        self.focus_windows()
        
        # Dispatch the mode change action
        self.action_dispatcher.dispatch(MultiModeFaderStateChangedAction(mode=new_mode))
