from script.device_independent.util_view.view import View


class SendsIdleScreenView(View):
    def __init__(self, action_dispatcher, fl, screen_writer):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.screen_writer = screen_writer

    def handle_OnRefreshAction(self, action):
        # Refresh display when needed
        self._on_show()

    def _on_show(self):
        self.screen_writer.display_idle("Sends")

    def _on_hide(self):
        self.screen_writer.display_idle("")
