from .calculate_add import calculate_add_spec
from .taco_tool import print_i_like_tacos_spec

tool_specs = {
    calculate_add_spec["name"]: calculate_add_spec,
    print_i_like_tacos_spec["name"]: print_i_like_tacos_spec,
}

available_tools = {
    name: spec["function"] for name, spec in tool_specs.items()
}

tools_schema = [spec["schema"] for spec in tool_specs.values()]


def get_tool_spec(tool_name: str):
    return tool_specs.get(tool_name)
