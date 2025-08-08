from script.actions import ChannelBankChangeAttemptedAction, ChannelBankChangedAction, ChannelSelectAction, ChannelSelectAttemptedAction
from script.device_independent.util_view import ScrollingArrowButtonView, View
from script.fl_constants import RefreshFlags


# This view allows for advanced channel selection, including bank switching
class ChannelSelectAdvancedView(View):
    def __init__(self, action_dispatcher, surface, fl, product_defs, model, *, bank_size=8):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.surface = surface
        self.model = model
        self.bank_size = bank_size
        self.arrow_button_view = ScrollingArrowButtonView(
            action_dispatcher,
            surface,
            product_defs,
            decrement_button="SelectPreviousChannel",
            increment_button="SelectNextChannel",
            on_page_changed=self._on_page_changed,
            on_page_change_attempted=self._on_page_change_attempted,
        )
        self.action_dispatcher = action_dispatcher

    def _on_show(self):
        self._handle_channel_selection_changed()
        self.arrow_button_view.show()

    def _on_hide(self):
        self.arrow_button_view.hide()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.ChannelSelection.value or action.flags & RefreshFlags.ChannelGroup.value:
            self._handle_channel_selection_changed()

    def handle_ChannelSelectionToggleAction(self, action):
        self._handle_channel_selection_changed()

    def _handle_channel_selection_changed(self):
        if self.fl.is_any_channel_selected():
            self.arrow_button_view.set_page_range(0, self.fl.channel_count() - 1)
            self.arrow_button_view.set_active_page(self.fl.selected_channel())
        else:
            self.arrow_button_view.set_page_range(-1, 0)
            self.arrow_button_view.set_active_page(-1)
        self._change_bank_if_needed()

    # Channel selection handling
    def _on_page_changed(self):
        new_channel_index = self.arrow_button_view.active_page
        self.fl.select_channel_exclusively(new_channel_index)
        self.action_dispatcher.dispatch(ChannelSelectAction())

    # Channel selection attempt handling
    def _on_page_change_attempted(self):
        self.action_dispatcher.dispatch(ChannelSelectAttemptedAction())
        self._on_bank_change_attempted()

    def _change_bank_if_needed(self):
        new_channel_index = self.arrow_button_view.active_page
        if (self._should_change_bank(new_channel_index)):
            self._change_bank(new_channel_index)
        self._on_bank_change_attempted()

    def _should_change_bank(self, new_channel_index):
        current_bank = self.model.channel_rack.active_bank
        new_bank = self._find_corresponding_bank(new_channel_index)
        return current_bank != new_bank

    def _find_corresponding_bank(self, new_channel_index):
        return new_channel_index // self.bank_size

    def _change_bank(self, new_channel_index):
        new_bank = self._find_corresponding_bank(new_channel_index)
        self.model.channel_rack.active_bank = new_bank
        self._on_bank_changed()

    def _on_bank_changed(self):
        self.action_dispatcher.dispatch(ChannelBankChangedAction())

    def _on_bank_change_attempted(self):
        self.action_dispatcher.dispatch(ChannelBankChangeAttemptedAction())
