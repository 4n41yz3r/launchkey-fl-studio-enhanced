from script.device_dependent.LaunchkeyMk4.volume_fader_layout_manager import VolumeFaderLayoutManager
from script.device_dependent.LaunchkeyMk4Range import (
    ChannelRackPadLayoutManager,
    DrumPadLayoutManager,
    GenericEncoderLayoutManager,
    MixerEncoderLayoutManager,
    PluginEncoderLayoutManager,
    SendsEncoderLayoutManager,
    TransportEncoderLayoutManager,
    MomentaryEncoderLayoutManager,
    SequencerPadLayoutManager,
)
from script.device_independent.fl_gui.fl_window_manager import FLWindowManager
from script.device_independent.view import (
    DumpScoreLogButtonView,
    MetronomeButtonView,
    MixerBankScreenView,
    MixerMasterVolumeView,
    MixerTrackSelectedScreenView,
    MixerTrackSelectView,
    MixerVolumeScreenView,
    QuantiseButtonView,
    RedoButtonView,
    ShowHighlightsView,
    ToggleLoopRecordButtonView,
    TransportPlayPauseButtonView,
    TransportRecordButtonView,
    TransportStopButtonView,
    UndoButtonView,
    SequencerStepEditScreenView,
    ChannelSelectedScreenView,
)
from script.model import Model
from util.command_dispatcher import CommandDispatcher


class Application:
    def __init__(
        self, pad_led_writer, button_led_writer, fl, action_dispatcher, screen_writer, device_manager, product_defs
    ):
        self.active_pad_layout_manager = None
        self.active_encoder_layout_manager = None
        self.active_fader_layout_manager = None
        self.pad_led_writer = pad_led_writer
        self.button_led_writer = button_led_writer
        self.fl = fl
        self.action_dispatcher = action_dispatcher
        self.command_dispatcher = CommandDispatcher()
        self.screen_writer = screen_writer
        self.product_defs = product_defs
        self.device_manager = device_manager
        self.model = None

        self.global_views = set()
        self.fl_window_manager = FLWindowManager(action_dispatcher, fl)

    def init(self):
        self.active_pad_layout_manager = None
        self.active_encoder_layout_manager = None
        self.active_fader_layout_manager = None
        self.model = Model()

        self.action_dispatcher.subscribe(self)

        self.global_views = {
            DumpScoreLogButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            MetronomeButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            QuantiseButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            ToggleLoopRecordButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            TransportPlayPauseButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            TransportRecordButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            TransportStopButtonView(self.action_dispatcher, self.fl, self.product_defs, self.button_led_writer),
            MixerBankScreenView(self.action_dispatcher, self.screen_writer, self.model),
            MixerMasterVolumeView(self.action_dispatcher, self.fl),
            MixerVolumeScreenView(self.action_dispatcher, self.screen_writer, self.fl),
            MixerTrackSelectView(
                self.action_dispatcher, self.product_defs, self.model, self.button_led_writer, self.fl
            ),
            MixerTrackSelectedScreenView(
                self.action_dispatcher, self.screen_writer, self.fl, show_index_in_primary_text=True
            ),
            UndoButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            RedoButtonView(self.action_dispatcher, self.button_led_writer, self.fl, self.product_defs),
            ShowHighlightsView(self.action_dispatcher, self.product_defs, self.model),
            SequencerStepEditScreenView(self.action_dispatcher, self.screen_writer, self.fl),
            ChannelSelectedScreenView(self.action_dispatcher, self.screen_writer, self.fl),
        }
        for view in self.global_views:
            view.show()

    def deinit(self):
        if self.active_encoder_layout_manager:
            self.active_encoder_layout_manager.hide()

        if self.active_pad_layout_manager:
            self.active_pad_layout_manager.hide()

        if self.active_fader_layout_manager:
            self.active_fader_layout_manager.hide()

        for view in self.global_views:
            view.hide()

        self.action_dispatcher.unsubscribe(self)

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("ShiftModifier"):
            self.button_led_writer.shift_modifier_pressed()

    def handle_ButtonReleasedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("ShiftModifier"):
            self.button_led_writer.shift_modifier_released()

    def handle_PadLayoutChangedAction(self, action):
        if self.active_pad_layout_manager:
            self.active_pad_layout_manager.hide()

        self.active_pad_layout_manager = self._create_pad_layout_manager(action.layout)
        if self.active_pad_layout_manager:
            self.active_pad_layout_manager.show()

    def handle_FaderLayoutChangedAction(self, action):
        if self.active_fader_layout_manager:
            self.active_fader_layout_manager.hide()

        self.active_fader_layout_manager = self._create_fader_layout_manager(action.layout)
        if self.active_fader_layout_manager:
            self.active_fader_layout_manager.show()
            self.active_fader_layout_manager.focus_windows()

    def handle_EncoderLayoutChangedAction(self, action):
        skip_window_focusing = isinstance(self.active_encoder_layout_manager, MomentaryEncoderLayoutManager)

        if self.active_encoder_layout_manager:
            self.active_encoder_layout_manager.hide()

        self.active_encoder_layout_manager = self._create_encoder_layout_manager(action.layout)
        if self.active_encoder_layout_manager:
            self.active_encoder_layout_manager.show()
            if not skip_window_focusing:
                self.active_encoder_layout_manager.focus_windows()

    def _create_pad_layout_manager(self, layout):
        if layout == self.product_defs.PadLayout.ChannelRack:
            return ChannelRackPadLayoutManager(
                self.action_dispatcher,
                self.pad_led_writer,
                self.button_led_writer,
                self.screen_writer,
                self.fl,
                self.product_defs,
                self.model,
                self.fl_window_manager,
            )
        if layout == self.product_defs.PadLayout.Sequencer:
            return SequencerPadLayoutManager(
                self.action_dispatcher,
                self.command_dispatcher,
                self.pad_led_writer,
                self.button_led_writer,
                self.screen_writer,
                self.fl,
                self.product_defs,
                self.model,
                self.device_manager,
                self.fl_window_manager,
            )
        if layout == self.product_defs.PadLayout.Drum:
            return DrumPadLayoutManager(self.action_dispatcher, self.pad_led_writer, self.product_defs, self.fl)
        return None

    def _create_fader_layout_manager(self, layout):
        if layout == self.product_defs.FaderLayout.Volume:
            return VolumeFaderLayoutManager(
                self.action_dispatcher,
                self.command_dispatcher,
                self.fl,
                self.model,
                self.fl_window_manager,
                self.product_defs,
                self.button_led_writer,
                self.screen_writer,
            )
        return None

    def _create_encoder_layout_manager(self, layout):
        if layout == self.product_defs.EncoderLayout.Plugin:
            return PluginEncoderLayoutManager(
                self.action_dispatcher, self.fl, self.product_defs, self.screen_writer, self.button_led_writer, self.device_manager
            )
        if layout == self.product_defs.EncoderLayout.Mixer:
            return MixerEncoderLayoutManager(
                self.action_dispatcher,
                self.fl,
                self.product_defs,
                self.model,
                self.fl_window_manager,
                self.screen_writer,
                self.button_led_writer,
                self.device_manager,
            )
        if layout == self.product_defs.EncoderLayout.Sends:
            return SendsEncoderLayoutManager(
                self.action_dispatcher, self.fl, self.screen_writer, self.device_manager, self.product_defs
            )
        if layout == self.product_defs.EncoderLayout.Transport:
            return TransportEncoderLayoutManager(
                self.action_dispatcher, self.fl, self.screen_writer, self.device_manager, self.product_defs
            )
        if layout == self.product_defs.EncoderLayout.Momentary:
            return MomentaryEncoderLayoutManager(
                self.action_dispatcher, self.fl, self.model
            )
        return GenericEncoderLayoutManager(self.action_dispatcher, self.screen_writer)
