import requests


def generate_prompt(return_message):
    return """You are required to generate a sentence for the user as they have successfully executed a command, 
    incorporating a description of the command. COMMAND DESCRIPTION: """ + return_message


def control_lights(ip_address, data):
    print(f"Sending command to WLED API: {data}")
    """
    Sendet einen Befehl an die WLED-API.

    :param ip_address: Die IP-Adresse der WLED-Instanz.
    :param data: Ein Dictionary mit den Daten, die an die WLED-API gesendet werden sollen.
    """
    url = f"http://{ip_address}/json/state"

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            action_description = " und ".join(
                [f"{key} {'eingeschaltet' if val else 'ausgeschaltet'}" for key, val in data.items() if
                 isinstance(val, bool)])
            print(f"Aktion erfolgreich ausgeführt: {action_description}.")
            return generate_prompt(f"Aktion erfolgreich ausgeführt: {action_description}.")
        else:
            print(f"Fehler bei der Ausführung der Aktion: HTTP-Status {response.status_code}")
            return generate_prompt(f"Fehler bei der Ausführung der Aktion: HTTP-Status {response.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return generate_prompt(f"Ein Fehler ist aufgetreten: {e}")


def lights_off(ip_address):
    # Lichter ausschalten
    return control_lights(ip_address, {'on': False})


def lights_on(ip_address):
    # Lichter einschalten
    return control_lights(ip_address, {'on': True})


def set_brightness(ip_address, brightness):
    # Helligkeit einstellen
    return control_lights(ip_address, {'bri': brightness})


def set_color(ip_address, r, g, b):
    # Farbe einstellen (als Beispiel)
    return control_lights(ip_address, {'seg': [{'col': [[r, g, b], [0, 0, 0], [0, 0, 0]]}]})
