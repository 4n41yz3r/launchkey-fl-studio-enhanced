from script.constants import Encoders
from script.device_dependent.LaunchkeyMk4Range.paged_layout_manager import (
    PagedLayoutManager,
)
from script.device_independent.view import (
    PluginIdleScreenView,
    PluginParameterPreviewView,
    PluginParameterScreenView,
    PluginParameterView,
    PresetButtonScreenView,
    PresetButtonView
)
from script.plugin import plugin_parameter_mappings
from util.control_to_index import make_control_to_index


class PluginEncoderLayoutManager(PagedLayoutManager):
    def __init__(self, action_dispatcher, fl, product_defs, screen_writer, button_led_writer, device_manager, num_pages=3):
        self.device_manager = device_manager
        self.fl = fl
        self.screen_writer = screen_writer
        self.button_led_writer = button_led_writer
        self.control_to_index = make_control_to_index(Encoders.FirstControlIndex.value, Encoders.Num.value)

        layouts = [self._create_layout(action_dispatcher, product_defs, page) for page in range(num_pages)]

        super().__init__(
            action_dispatcher,
            product_defs,
            screen_writer,
            button_led_writer,
            layouts,
            "SelectNextPluginEncoderPage",
            "SelectPreviousPluginEncoderPage",
        )

    def _create_layout(self, action_dispatcher, product_defs, page):
        return PagedLayoutManager.Layout(
            layout_id=page,
            notification_primary="Plugin",
            notification_secondary=f"Page {page + 1}",
            views=[
                PluginIdleScreenView(action_dispatcher, self.fl, self.screen_writer, plugin_parameter_mappings, parameter_page=page),
                PluginParameterView(
                    action_dispatcher,
                    self.fl,
                    plugin_parameter_mappings,
                    control_to_index=self.control_to_index,
                    parameter_page=page
                ),
                PluginParameterScreenView(
                    action_dispatcher,
                    self.fl,
                    self.screen_writer,
                    plugin_parameter_mappings,
                    control_to_index=self.control_to_index,
                    parameter_page=page
                ),
                PluginParameterPreviewView(
                    action_dispatcher,
                    self.fl,
                    product_defs,
                    plugin_parameter_mappings,
                    control_to_index=self.control_to_index,
                    parameter_page=page
                ),
                PresetButtonScreenView(action_dispatcher, self.screen_writer, self.fl),
                PresetButtonView(action_dispatcher, self.button_led_writer, self.fl, product_defs),
            ],
        )

    def show(self):
        super().show()
        self.device_manager.enable_encoder_mode()

    def hide(self):
        super().hide()

    def focus_windows(self):
        pass

    def on_layout_selected(self, layout_id):
        self.focus_windows()
