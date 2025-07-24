from script.device_independent.util_view.arrow_button_view import ArrowButtonView
from .paged_layout_manager import PagedLayoutManager


class DynamicPagedLayoutManager(PagedLayoutManager):
    def __init__(
        self,
        action_dispatcher,
        product_defs,
        screen_writer,
        button_led_writer,
        layouts,
        page_up_function,
        page_down_function,
    ):
        self.abv_parameters = {
            'action_dispatcher': action_dispatcher,
            'product_defs': product_defs,
            'button_led_writer': button_led_writer,
            'page_up_function': page_up_function,
            'page_down_function': page_down_function,
        }
        
        super().__init__(
            action_dispatcher,
            product_defs,
            screen_writer,
            button_led_writer,
            layouts,
            page_up_function,
            page_down_function,
        )

    def update_layouts(self, new_layouts):
        if not new_layouts:
            raise ValueError("Layouts list cannot be empty")
        
        # Store current layout_id if any is active
        current_layout_id = None
        if self.active_layout_index is not None:
            current_layout_id = self._active_layout.layout_id
        
        # Store current visibility state
        was_shown = self.active_layout_index is not None
        
        # Hide current views and arrow buttons before updating
        if was_shown:
            self._hide_layout_views()
            self.arrow_button_view.hide()
        
        # Atomically replace all layouts
        self.layouts = list(new_layouts)  # Create a copy to avoid external modifications
        
        # Recreate ArrowButtonView with new layout count
        self.arrow_button_view = ArrowButtonView(
            self.abv_parameters['action_dispatcher'],
            self.abv_parameters['button_led_writer'],
            self.abv_parameters['product_defs'],
            decrement_button=self.abv_parameters['page_up_function'],
            increment_button=self.abv_parameters['page_down_function'],
            last_page=len(self.layouts) - 1,
            on_page_changed=self._on_page_changed,
        )
        
        # Determine new active layout index
        new_active_index = 0  # Default to first layout
        if current_layout_id is not None:
            # Try to find the previously active layout in the new layouts
            for index, layout in enumerate(self.layouts):
                if layout.layout_id == current_layout_id:
                    new_active_index = index
                    break
        
        # Update active layout index
        if was_shown:
            self.active_layout_index = new_active_index
            self.arrow_button_view.set_active_page(new_active_index)
            
            # Restore visibility state
            self.arrow_button_view.show()
            self._show_layout_views()
            
            # Notify about layout selection
            self.on_layout_selected(self._active_layout.layout_id)
        else:
            self.active_layout_index = None

