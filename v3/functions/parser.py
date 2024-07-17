import ipaddress

from v3.utilities import actions

context_actions = {
    "lights_off": actions.lights_off,
    "lights_on": actions.lights_on,
    "set_brightness": actions.set_brightness,
    "set_color": actions.set_color,
    "search_internet": actions.search_web
}

color_dict = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    # Add more colors as needed
}


def parse_and_execute_function(response_text):
    print("Response text: ", response_text)
    start = response_text.find("$%")
    end = response_text.find("$%", start + 2)
    if start != -1 and end != -1:
        function_call = response_text[start + 2:end]
        function_parts = function_call.split(',')
        function_name = function_parts[0].strip()
        if function_name in context_actions:
            if function_name == "set_brightness":
                if len(function_parts) == 2:
                    try:
                        brightness = int(function_parts[1].strip())
                        return function_name, context_actions[function_name](ipaddress, brightness)
                    except ValueError:
                        print(f"Invalid brightness value: {function_parts[1].strip()}")
                else:
                    print(f"Invalid parameters for {function_name}: {function_parts}")
            elif function_name == "set_color":
                if len(function_parts) == 4:
                    try:
                        r = int(function_parts[1].strip())
                        g = int(function_parts[2].strip())
                        b = int(function_parts[3].strip())
                        return function_name, context_actions[function_name](ipaddress, r, g, b)
                    except ValueError:
                        print(f"Invalid RGB values: {function_parts[1:4]}")
                elif len(function_parts) == 2:
                    color_name = function_parts[1].strip().lower()
                    if color_name in color_dict:
                        r, g, b = color_dict[color_name]
                        return function_name, context_actions[function_name](ipaddress, r, g, b)
                    else:
                        print(f"Unknown color name: {color_name}")
                else:
                    print(f"Invalid parameters for {function_name}: {function_parts}")
            elif function_name == "search_internet":
                if len(function_parts) == 2:
                    search_query = function_parts[1].strip()
                    return function_name, context_actions[function_name](search_query)
                else:
                    print(f"Invalid parameters for {function_name}: {function_parts}")
            else:
                return function_name, context_actions[function_name](ipaddress)
        cleaned_response = response_text[:start] + response_text[end + 2:]
        return function_name, cleaned_response.strip()
    return None, response_text

