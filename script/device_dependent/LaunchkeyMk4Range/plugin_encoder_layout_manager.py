from script.constants import ChannelNavigationMode, Encoders
from script.device_dependent.LaunchkeyMk4Range.dynamic_paged_layout_manager import (
    DynamicPagedLayoutManager,
    PagedLayoutManager,
)
from script.device_independent.view import (
    PluginIdleScreenView,
    PluginParameterPreviewView,
    PluginParameterScreenView,
    PluginParameterView,
)
from script.plugin import plugin_parameter_mappings
from util.control_to_index import make_control_to_index


class PluginEncoderLayoutManager(DynamicPagedLayoutManager):
    def __init__(self, action_dispatcher, fl, product_defs, screen_writer, button_led_writer, device_manager):
        self.device_manager = device_manager
        self.screen_writer = screen_writer
        self.button_led_writer = button_led_writer
        control_to_index = make_control_to_index(Encoders.FirstControlIndex.value, Encoders.Num.value)

        layouts = [
            PagedLayoutManager.Layout(
                layout_id=0,
                notification_primary="Plugin",
                notification_secondary="Page 1",
                views=[
                    PluginIdleScreenView(action_dispatcher, fl, screen_writer, plugin_parameter_mappings),
                    PluginParameterView(action_dispatcher, fl, plugin_parameter_mappings, control_to_index=control_to_index),
                    PluginParameterScreenView(
                        action_dispatcher, fl, screen_writer, plugin_parameter_mappings, control_to_index=control_to_index
                    ),
                    PluginParameterPreviewView(
                        action_dispatcher,
                        fl,
                        product_defs,
                        plugin_parameter_mappings,
                        control_to_index=control_to_index,
                    )
                ],
            ),
            PagedLayoutManager.Layout(
                layout_id=1,
                notification_primary="Plugin",
                notification_secondary="Page 2",
                views=[
                    PluginIdleScreenView(action_dispatcher, fl, screen_writer, plugin_parameter_mappings),
                    PluginParameterView(action_dispatcher, fl, plugin_parameter_mappings, control_to_index=control_to_index),
                    PluginParameterScreenView(
                        action_dispatcher, fl, screen_writer, plugin_parameter_mappings, control_to_index=control_to_index
                    ),
                    PluginParameterPreviewView(
                        action_dispatcher,
                        fl,
                        product_defs,
                        plugin_parameter_mappings,
                        control_to_index=control_to_index,
                    )
                ],
            )
        ]

        super().__init__(
            action_dispatcher,
            product_defs,
            screen_writer,
            button_led_writer,
            layouts,
            "SelectNextPluginEncoderPage",
            "SelectPreviousPluginEncoderPage",
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
