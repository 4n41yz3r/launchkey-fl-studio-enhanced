from script.actions import ChannelRackNavigationModeChangedAction
from script.constants import ChannelNavigationMode
from script.device_independent.view import (
    ChannelBankNamesHighlightView,
    ChannelBankSelectedScreenView,
    ChannelBankView,
    ChannelRackDrumPadsView,
    MixerTrackPluginSelectView,
    MixerTrackPluginSelectedScreenView,
    MixerBankButtonView,
    MixerBankHighlightView,
)
from util.mapped_pad_led_writer import MappedPadLedWriter


class ChannelRackPadLayoutManager:
    def __init__(
        self,
        action_dispatcher,
        pad_led_writer,
        button_led_writer,
        screen_writer,
        fl,
        product_defs,
        model,
        fl_window_manager,
    ):
        self.fl = fl
        self.screen_writer = screen_writer
        self.action_dispatcher = action_dispatcher
        self.model = model
        self.fl_window_manager = fl_window_manager
        channel_rack_pad_led_writer = MappedPadLedWriter(
            pad_led_writer, product_defs.Constants.NotesForPadLayout.value[product_defs.PadLayout.ChannelRack]
        )
        self.views = {
            ChannelRackDrumPadsView(action_dispatcher, channel_rack_pad_led_writer, fl, model),
            ChannelBankView(action_dispatcher, button_led_writer, fl, product_defs, model),
            ChannelBankNamesHighlightView(action_dispatcher, fl, model),
            ChannelBankSelectedScreenView(action_dispatcher, screen_writer, fl, model),
            MixerTrackPluginSelectView(action_dispatcher, button_led_writer, fl, product_defs),
            MixerTrackPluginSelectedScreenView(action_dispatcher, screen_writer, fl),
            MixerBankButtonView(self.action_dispatcher, button_led_writer, self.fl, product_defs, self.model),
            MixerBankHighlightView(self.action_dispatcher, self.fl, self.model),
        }

    def show(self):
        self.model.channel_rack.navigation_mode = ChannelNavigationMode.Bank
        self.action_dispatcher.dispatch(ChannelRackNavigationModeChangedAction())
        self.action_dispatcher.subscribe(self)
        for view in self.views:
            view.show()
        self.fl_window_manager.focus_channel_window()

    def hide(self):
        for view in self.views:
            view.hide()
        self.action_dispatcher.unsubscribe(self)
