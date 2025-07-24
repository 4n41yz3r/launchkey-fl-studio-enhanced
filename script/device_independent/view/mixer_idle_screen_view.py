from script.device_independent.util_view.view import View


class MixerIdleScreenView(View):
    def __init__(self, action_dispatcher, fl, screen_writer, page_name):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.screen_writer = screen_writer
        self.page_name = page_name

    def handle_OnRefreshAction(self, action):
        self._on_show()

    def _on_show(self):
        self.screen_writer.display_idle("Mixer", self.page_name)

    def _on_hide(self):
        self.screen_writer.display_idle("")
