from script.device_independent.util_view.view import View


class PluginIdleScreenView(View):
    def __init__(self, action_dispatcher, fl, screen_writer, plugin_parameters=None):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.screen_writer = screen_writer
        self.plugin_parameters = plugin_parameters
        self._refresh_plugin_names()

    def handle_ChannelSelectAction(self, action):
        self._refresh_plugin_names()
        self._on_show()

    def _refresh_plugin_names(self):
        self.plugin = self.fl.get_selected_plugin()
        if self.plugin_parameters and self.plugin in self.plugin_parameters:
            parameters = self.plugin_parameters[self.plugin]
            self.names = tuple(self._to_short_name(getattr(param, 'name', str(param))) for param in parameters) if parameters else None
        else:
            self.names = None

    def _on_show(self):
        if (self.plugin and self.names):
            self.screen_writer.display_idle(self.plugin, self.names)
        else:
            self.screen_writer.display_idle("Plugin")

    def _on_hide(self):
        self.screen_writer.display_idle("")

    def _to_short_name(self, name):
        """Truncate parameter name to 4 characters using smart rules."""
        if not name:
            return ""
        
        words = name.split()
        special_first_words = {"Filter", "Gate", "Sample", "LFO", "Master", "Osc"}

        if len(words) == 1:
            # Single word: take first 4 characters
            return words[0][:4]
        elif len(words) == 2:
            first_word, second_word = words[0], words[1]
            
            # Check if first word is special and should only contribute 1 character
            if first_word in special_first_words:
                # For special words, take 1 char from first + up to 3 from second
                if len(second_word) == 1:
                    # Special case: "Filter 1" -> "Fil1"
                    return first_word[:3] + second_word
                else:
                    # Normal case: "Filter Cutoff" -> "FCut"
                    return first_word[0] + second_word[:3]
            else:
                # Check if second word is single character
                if len(second_word) == 1:
                    # Take first 3 letters of first word + the character
                    return first_word[:3] + second_word
                else:
                    # Take first 2 characters of each word
                    return first_word[:2] + second_word[:2]
        else:
            # More than 2 words
            if words[0] in special_first_words:
                # Take 1 char from first word + 1 char from next 3 words
                result = words[0][0]
                result += "".join(word[0] for word in words[1:4] if word)
                return result
            else:
                # Take first character of each word up to 4 total
                return "".join(word[0] for word in words[:4] if word)