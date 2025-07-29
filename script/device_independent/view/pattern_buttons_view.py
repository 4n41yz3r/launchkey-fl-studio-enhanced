from script.device_independent.util_view.single_button_view import SingleButtonView
from script.device_independent.util_view.view import View


class SimplePatternSelectView(View):
    def __init__(
        self,
        action_dispatcher,
        screen_writer,
        button_led_writer,
        fl,
        product_defs,
        *,
        previous_button = "SelectPreviousPattern",
        next_button = "SelectNextPattern",
    ):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.screen_writer = screen_writer
        self.previous_button_view = SingleButtonView(
            button_led_writer, product_defs, previous_button
        )
        self.next_button_view = SingleButtonView(
            button_led_writer, product_defs, next_button
        )

    def handle_ButtonPressedAction(self, action):
        if action.button == self.next_button_view.button:
            self._press_next_button()
        elif action.button == self.previous_button_view.button:
            self._press_previous_button()

    def handle_ButtonReleasedAction(self, action):
        if action.button == self.next_button_view.button:
            self._release_next_button()
        elif action.button == self.previous_button_view.button:
            self._release_previous_button()

    def _on_show(self):
        self.previous_button_view.show()
        self.next_button_view.show()

    def _on_hide(self):
        self.previous_button_view.hide()
        self.next_button_view.hide()

    def _press_next_button(self):
        self.next_button_view.set_pressed()
        self._select_next_pattern()

    def _press_previous_button(self):
        self.previous_button_view.set_pressed()
        self._select_previous_pattern()

    def _release_next_button(self):
        self.next_button_view.set_not_pressed()

    def _release_previous_button(self):
        self.previous_button_view.set_not_pressed()

    def _select_next_pattern(self):
        current_pattern = self.fl.get_selected_pattern_index()
        self.fl.select_pattern(current_pattern + 1)
        # Get the actual selected pattern after the selection
        actual_pattern = self.fl.get_selected_pattern_index()
        self._display_pattern_notification(actual_pattern)

    def _select_previous_pattern(self):
        current_pattern = self.fl.get_selected_pattern_index()
        if current_pattern > 0:  # Prevent going below pattern 0
            self.fl.select_pattern(current_pattern - 1)
            # Get the actual selected pattern after the selection
            actual_pattern = self.fl.get_selected_pattern_index()
            self._display_pattern_notification(actual_pattern)

    def _display_pattern_notification(self, pattern_number):
        self.screen_writer.display_notification(primary_text=f"Pattern", secondary_text=f"#{pattern_number}")
