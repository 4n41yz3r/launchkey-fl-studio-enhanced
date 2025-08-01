from script.device_independent.util_view.view import View
from script.plugin.plugin_parameter_pagination import get_page_parameters

class PluginIdleScreenView(View):
    def __init__(self, action_dispatcher, fl, screen_writer, plugin_parameters=None, parameter_page=0):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.screen_writer = screen_writer
        self.plugin_parameters = plugin_parameters
        self.plugin = None
        self.parameter_page = parameter_page
        self._refresh_plugin_names()

    def handle_OnRefreshAction(self, action):
        self._on_show()
        pass

    def _on_show(self):
        self._refresh_plugin_names()
        if self.plugin:
            title = self.plugin + " /" + str(self.parameter_page + 1)
            self.screen_writer.display_idle(title, self.names or [])
        else:
            self.screen_writer.display_idle("Plugin")

    def _on_hide(self):
        # Calling display_idle("") here causes a flicker when switching pages
        pass

    def _refresh_plugin_names(self):
        current_plugin = self.fl.get_selected_plugin()
        if self.plugin == current_plugin:
            return
            
        self.plugin = current_plugin
        page_parameters = get_page_parameters(self.plugin_parameters, current_plugin, self.parameter_page)
        self.names = tuple(self._to_short_name(getattr(param, 'name', None)) for param in page_parameters) if page_parameters else None

    def _to_short_name(self, name):
        """Truncate parameter name to 4 characters using smart rules."""
        if not name:
            return None
        
        words = name.split()
        special_first_words = {"Filter", "Gate", "Sample", "LFO", "Master", "Osc", "Unison", "303", "VCF", "Grain", "Wave", "Offset"}

        if len(words) == 1:
            # Single word: take first 4 characters
            return words[0][:4]
        elif len(words) == 2:
            first_word, second_word = words[0], words[1]
            
            # Special case for "Macro" - always abbreviated to "M"
            if first_word == "Macro":
                return "M" + second_word[:3]
            # Check if first word is special and should only contribute 1 character
            elif first_word in special_first_words:
                return first_word[0] + second_word[:3]
            # Check if second word is single character
            elif len(second_word) == 1:
                # Take first 3 letters of first word + the character
                return first_word[:3] + second_word
            else:
                # Take first 2 characters of each word
                return first_word[:2] + second_word[:2]
        else:
            # More than 2 words: take first character of each word up to 4 total
            return "".join(word[0] for word in words[:4] if word)