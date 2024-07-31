import ipaddress

from v3.utilities import actions

context_actions = {
    "lights_off": actions.lights_off,
    "lights_on": actions.lights_on,
    "set_brightness": actions.set_brightness,
    "set_color": actions.set_color,
    "search_internet": actions.search_web,
    "get_weather": actions.get_weather,
    "get_date_time": actions.get_date_time,
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

    start = response_text.find("%")
    end = response_text.find("%", start + 1)

    if start != -1 and end != -1:
        function_call = response_text[start + 1:end]
        print("Extracted function call: ", function_call)

        function_parts = function_call.split(',')
        function_name = function_parts[0].strip()
        print("Function name: ", function_name)

        if function_name in context_actions:
            if function_name == "set_brightness":
                if len(function_parts) == 2:
                    try:
                        brightness = int(function_parts[1].strip())
                        print(f"Setting brightness to {brightness}")
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
                        print(f"Setting color to RGB({r}, {g}, {b})")
                        return function_name, context_actions[function_name](ipaddress, r, g, b)
                    except ValueError:
                        print(f"Invalid RGB values: {function_parts[1:4]}")
                elif len(function_parts) == 2:
                    color_name = function_parts[1].strip().lower()
                    if color_name in color_dict:
                        r, g, b = color_dict[color_name]
                        print(f"Setting color to {color_name} with RGB({r}, {g}, {b})")
                        return function_name, context_actions[function_name](ipaddress, r, g, b)
                    else:
                        print(f"Unknown color name: {color_name}")
                else:
                    print(f"Invalid parameters for {function_name}: {function_parts}")

            elif function_name == "search_internet":
                if len(function_parts) == 2:
                    search_query = function_parts[1].strip()
                    print(f"Searching the internet for: {search_query}")
                    return function_name, context_actions[function_name](search_query)
                else:
                    print(f"Invalid parameters for {function_name}: {function_parts}")

            elif function_name == "get_weather":
                if len(function_parts) == 2:
                    city_query = function_parts[1].strip()
                    print(f"Getting weather for: {city_query}")
                    return function_name, context_actions[function_name](city_query)

            elif function_name == "get_date_time":
                print("Getting current date and time")
                return function_name, context_actions[function_name]()

            else:
                print(f"Executing function: {function_name}")
                return function_name, context_actions[function_name](ipaddress)
        else:
            print(f"Function {function_name} not found in context actions")

        cleaned_response = response_text[:start] + response_text[end + 2:]
        print("Cleaned response text: ", cleaned_response.strip())
        return function_name, cleaned_response.strip()

    print("No function call found in response text")
    return None, response_text

