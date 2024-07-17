import requests
from v3 import server

def generate_prompt(return_message):
    return """You are required to generate a sentence for the user as they have successfully executed a command, 
    incorporating a description of the command. COMMAND DESCRIPTION: """ + return_message


def control_lights(ip_address, data):
    print(f"Sending command to WLED API: {data}")
    url = f"http://{ip_address}/json/state"

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            action_description = " und ".join(
                [f"{key} {'on' if val else 'off'}" for key, val in data.items() if
                 isinstance(val, bool)])
            print(f"Action successfully executed: {action_description}.")
            return generate_prompt(f"Action successfully executed: {action_description}.")
        else:
            print(f"Failure by executing the Action: HTTP-Status {response.status_code}")
            return generate_prompt(f"Failure by executing the Action: HTTP-Status {response.status_code}")
    except Exception as e:
        print(f"A Execution has happened: {e}")
        return generate_prompt(f"A Execution has happened: {e}")


def lights_off(ip_address):
    return control_lights(ip_address, {'on': False})


def lights_on(ip_address):
    return control_lights(ip_address, {'on': True})


def set_brightness(ip_address, brightness):
    return control_lights(ip_address, {'bri': brightness})


def set_color(ip_address, r, g, b):
    return control_lights(ip_address, {'seg': [{'col': [[r, g, b], [0, 0, 0], [0, 0, 0]]}]})


def search_web(query):
    try:
        search_results = server.tavily_client.qna_search(query)
        print("Search Result:" + search_results)
        return search_results
    except Exception as e:
        print(f"Error during web search: {e}")
        return {"error": str(e)}
