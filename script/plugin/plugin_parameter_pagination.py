from script.constants import Encoders


def get_page_parameters(plugin_parameters, plugin_name, parameter_page):
    """Get parameters for the specified page.
    
    Args:
        plugin_parameters: Dictionary mapping plugin names to parameter lists
        plugin_name: Name of the plugin to get parameters for
        parameter_page: Zero-based page index
        
    Returns:
        List of parameters for the specified page (up to 8 parameters)
    """
    if not plugin_parameters or plugin_name not in plugin_parameters:
        return []

    parameters = plugin_parameters[plugin_name]
    if not parameters:
        return []
    
    # Calculate page boundaries (page size = 8)
    page_size = Encoders.Num.value
    start_index = parameter_page * page_size
    end_index = start_index + page_size
    
    # Get parameters for this page
    return parameters[start_index:end_index]
